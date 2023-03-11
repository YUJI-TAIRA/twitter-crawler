from enum import Enum, IntEnum

# 取得するフィールド
class Fields(Enum):
    USER = "id,created_at,description,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
    TWEET = (
        "created_at,public_metrics,lang,author_id,referenced_tweets,in_reply_to_user_id"
    )


# リツイート、引用ツイートの種類
class Type(IntEnum):
    RETWEET = 1
    QUOTE = 2
