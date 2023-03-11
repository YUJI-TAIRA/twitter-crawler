# from typing import List, Optional, Any, NoReturn
# from datetime import datetime, timedelta
# from zoneinfo import ZoneInfo
# from fastapi import Depends
# from sqlmodel import select, func
# from sqlmodel.ext.asyncio.session import AsyncSession
# from app.core.database import get_async_session
# from app.models import User, Tweet


# class CRUDUser:
#     """
#     ユーザー関連のCRUD操作を行うクラス
#     """

#     @staticmethod
#     async def get_incentive_tweets(
#         self, limit_like_count: int, session: AsyncSession = Depends(get_async_session)
#     ) -> list:
#         """
#         Description of my_function.

#         Args:
#             limit_like_count (int): インセンティブ上限いいね数

#         Returns:
#             list: ユーザーのツイート情報
#         """

#         today = datetime.today(ZoneInfo("Asia/Tokyo"))
#         # 前月の1日
#         first_day = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
#         # 前月の最終日
#         last_day = today.replace(day=1) - timedelta(days=1)

#         query = (
#             select(
#                 User,
#                 func.sum(
#                     func.coalesce(
#                         func.nullif(Tweet.tweet_like_count < limit_like_count, True),
#                         limit_like_count,
#                     )
#                 ).label("likes_count"),
#                 func.sum(Tweet.tweet_retweet_count).label("retweets_count"),
#                 func.count(Tweet.tweet_id).label("tweets_count"),
#             )
#             .join(Tweet, Tweet.tweet_author_id == User.id)
#             .where(
#                 (Tweet.tweet_created_at.between(first_day, last_day))
#                 & (Tweet.is_incentive_tweet == True)
#                 & (User.is_incentive_user == True)
#             )
#             .group_by(User.id)
#             .order_by(Tweet.tweet_created_at.desc())
#         )

#         result = await session.exec(query)

#         return result.scalars().all()

#     async def save_users(
#         self,
#         users: list[dict[str, Any]],
#         session: AsyncSession = Depends(get_async_session),
#     ) -> None:
#         """
#         リストで渡されたユーザー情報を保存する

#         Args:
#             users (list[dict[str, Any]]): usersテーブルに保存する情報の入ったdict
#         """
#         prefix = "user_"
#         users = {prefix + k: v for k, v in users.items()}

#         for user in users:
#             # 実行 ユーザー情報が存在しない場合は追加
#             session.merge(User(**user))

#         await session.flush()


# user = CRUDUser()
