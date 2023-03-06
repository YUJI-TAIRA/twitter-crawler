import asyncio
import logging
from datetime import datetime

from fastapi import Depends
from typing import NoReturn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.crud import common_setting, twitter, user
from app.core.database import get_async_session
from app.services.twitter_api_v2 import TwitterApiServiceV2


class SavePublicListTimeline:
    """公開リストのデータを取得し、保存するクラス"""
    
    def __init__(self):
        # 設定を取得
        self.config = common_setting.get_settings()
        # TODO: v1.1のサポート
        if self.config['twitter_api_version'] == 'v1.1':
            raise ValueError('v1.1 is not supported')
        else:
            self.twitter_api = TwitterApiServiceV2()

    async def __call__(
        self, session: AsyncSession = Depends(get_async_session)
    ) -> None | NoReturn:
        """公開リストのデータを取得し、保存する"""
        
        users_data = self.twitter_api.get_public_list_users(
            list_id=self.config['twitter_list_id']
        )
        timelines_data = self.twitter_api.get_public_list_timeline(
            list_id=self.config['twitter_list_id']
        )

        try:
            # 並行処理でDBに保存
            await asyncio.gather(
                user.save_users(users=users_data, session=session),
                twitter.save_tweets(tweets=timelines_data, session=session),
            )
            await session.commit()
        except Exception as e:
            await session.rollback()
            logging.error('failed to save public list timeline: ' + str(e))
