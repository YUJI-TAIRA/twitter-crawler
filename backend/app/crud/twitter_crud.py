# from typing import List, Any
# from fastapi import Depends, Query
# from sqlmodel import select, update
# from datetime import datetime
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.models.tweet_model import Tweet
# from app.core.database import get_async_session
# from app.crud import twitter, user, public_list

# class CRUDTwitter():
#     """ツイート関連の操作を行うクラス"""

#     async def get_tweets(
#         self,
#         first_tweet_created_at: datetime = Query(default=None),
#         session: AsyncSession = Depends(get_async_session)
#     ) -> list[Tweet]:
#         """ツイートを取得する"""

#         query = select(Tweet)
#         if first_tweet_created_at is not None:
#             query = query.where(Tweet.tweet_created_at >= first_tweet_created_at)

#         query = (query.order_by(Tweet.tweet_created_at.desc()).limit(1000))

#         return await session.exec(query).all()


#     async def save_tweets(
#         self, tweets: dict[str, Any], session: AsyncSession = Depends(get_async_session)
#     ) -> None:
#         """ツイートを保存する"""

#         try:
#             # 全てのキーにtweet_のプレフィックスをつける
#             tweets = [{f"tweet_{k}": v for k, v in tweet.items()} for tweet in tweets]
#             # Twitterオブジェクトに変換
#             tweets = [Tweet(**tweet) for tweet in tweets]
#             # tweet_idを取得して辞書に変換
#             tweet_id_set = set([tweet.tweet_id for tweet in tweets])
#             # tweetsの中から最も古いツイートの作成日時を取得
#             first_tweet_created_at = min([tweet.tweet_created_at for tweet in tweets])

#             # 既存のデータを取得
#             tweets_in_database = await self.get_tweets(
#                 first_tweet_created_at=first_tweet_created_at, session=session
#             )
#             tweet_ids_in_database = set([tweet.tweet_id for tweet in tweets_in_database])
#             tweets_in_database_dict = {tweet.tweet_id: tweet for tweet in tweets_in_database}

#             # 更新、追加、削除するデータを分類
#             to_insert = [tweet for tweet in tweets
#                             if tweet.tweet_id not in tweet_ids_in_database
#                         ]
#             to_update = [tweet for tweet in tweets
#                             if tweet.tweet_id in tweet_ids_in_database
#                             and tweets_in_database_dict[tweet.tweet_id] != tweet
#                         ]
#             to_delete = [tweet for tweet in tweets_in_database
#                             if tweet.tweet_id not in tweet_id_set
#                         ]

#             # bulk insert
#             if to_insert:
#                 await session.bulk_save_objects(to_insert)
#             # bulk update
#             if to_update:
#                 await session.bulk_update_mappings(Tweet, [tweet.dict() for tweet in to_update])
#             # logical delete
#             if to_delete:
#                 for tweet in to_delete:
#                     tweet.deleted_at = datetime.utcnow()
#                 await session.bulk_update_mappings(Tweet, [tweet.dict() for tweet in to_delete])

#             await session.flush()
#         except:


#         # # tweetsの中から最も古いツイートの作成日時を取得
#         # first_tweet_created_at = min([tweet.tweet_created_at for tweet in tweets])
#         # # DBに保存されているツイートを取得
#         # tweets_in_database = await get_tweets(
#         #     first_tweet_created_at=first_tweet_created_at, session=session
#         # )
#         # # DBに保存されているツイートをツイートIDをキーにした辞書に変換
#         # tweets_in_database_dict = {tweet.tweet_id: tweet for tweet in tweets_in_database}
#         # update_tweets = []
#         # insert_tweets = []

#         # for tweet in tweets:
#         #     # ツイートが存在する場合
#         #     if tweet.tweet_id in tweets_in_database_dict:
#         #         existing_tweet = tweets_in_database_dict[tweet.tweet_id]
#         #         if existing_tweet != tweet:
#         #             # ツイートが存在するが内容が異なる場合は、upsertするリストに追加
#         #             update_tweets.append(tweet)
#         #         # ツイートを削除リストから削除し、DBから削除されないようにする
#         #         del tweets_in_database_dict[tweet.tweet_id]
#         #     else:
#         #         # ツイートが存在しない場合は、upsertするリストに追加
#         #         insert_tweets.append(tweet)

#         # # updateを実行
#         # for tweet in update_tweets:
#         #     await session.add(tweet)

#         # # insertを実行
#         # for tweet in insert_tweets:
#         #     await session.add(tweet)

#         # # APIから取得されなかったツイートを削除
#         # if tweets_in_database_dict:
#         #     delete_query = (
#         #         update(Tweet)
#         #         .where(Tweet.tweet_id.in_(tweets_in_database_dict.keys()))
#         #         .values(deleted_at=datetime.utcnow())
#         #     )
#         #     # 実行
#         #     await session.exec(delete_query)

# # witter = CRUDTwitter()
