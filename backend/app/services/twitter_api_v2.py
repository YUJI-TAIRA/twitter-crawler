from typing import Any, Dict, List, Optional, NoReturn
from app.core.config import settings

# from app.models.tweet_model import Tweet
# from app.models.user_model import User
from app.core.enum import Fields, Type
import logging
import inspect
import tweepy


class TwitterApiServiceV2:
    """TwitterAPI v2のサービスクラス"""

    def __init__(self) -> None:
        self.api = tweepy.Client(settings.TWITTER_BEARER_TOKEN)

        try:
            self.api.raise_for_status()
        except tweepy.TweepyException as e:
            logging.error(f"Twitter APIに接続出来ませんでした: {e}")

    def get_public_list_users(self, list_id: str, max_results: int = 100) -> list[dict]:
        members = []
        pagination_token = None
        try:
            for _ in range(10):
                # get_list_members()を使用して公開リストのメンバー情報を取得
                response = self.api.get_list_members(
                    id=list_id,
                    max_results=max_results,
                    user_fields=Fields.USER.value,
                    pagination_token=pagination_token,
                )

                response.raise_for_status()
                members += response.data
                if "next_token" in response.meta:
                    pagination_token = response.meta["next_token"]
                else:
                    break

        except tweepy.TweepyException as e:
            logging.error(f"{self.__class__.__name__}@get_public_list_users: {e}")
            raise

        # 不要なデータを除外して整形
        result = self.extract_tweet_data(members)

        return result

    def get_public_list_timeline(
        self, list_id: str, max_results: int = 100
    ) -> list[dict]:
        tweets = []
        pagination_token = None
        try:
            for _ in range(max_results // 100):
                response = self.api.get_list_tweets(
                    list_id=list_id,
                    max_results=max_results,
                    tweet_fields=Fields.TWEET.value,
                    pagination_token=pagination_token,
                )

                response.raise_for_status()
                tweets += response.data
                if "next_token" in response.meta:
                    pagination_token = response.meta["next_token"]
                else:
                    break

        except tweepy.TweepyException as e:
            logging.error(f"{self.__class__.__name__}@get_public_list_timeline: {e}")
            raise

        # 不要なデータを除外して整形
        result = self.extract_tweet_data(tweets)

        return result

    def extract_tweet_data(tweets: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """ツイート情報を受取り、必要な情報のみを抽出する"""

        def match_referenced_tweets(referenced_tweets):
            match referenced_tweets:
                case [{"type": "retweeted"}]:
                    return {"type": Type.RETWEET.value}
                case [{"type": "quoted"}, _]:
                    return {"type": Type.QUOTE.value}
                case _:
                    return None

        for tweet in tweets:

            # リツイート、引用ツイートの場合はsource_tweet_idを追加
            if (referenced_tweets := tweet.get("referenced_tweets")) is not None:
                source_tweet_id = referenced_tweets[0].get("id")

                if (
                    new_tweet_type := match_referenced_tweets(referenced_tweets)
                ) is not None:
                    tweet.update({"source_tweet_id": source_tweet_id, **new_tweet_type})
                    del tweet["referenced_tweets"]

            # 返信ツイートの場合はis_replyを追加
            if tweet.get("in_reply_to_user_id") is not None:
                tweet.update({"is_reply": 1})
                del tweet["in_reply_to_user_id"]

            # edit_history_tweet_idsは不要なため削除
            tweet.pop("edit_history_tweet_ids", None)
            # public_metricsをtweetの直下に移動
            tweet.update(tweet.pop("public_metrics", {}))

        return tweet
