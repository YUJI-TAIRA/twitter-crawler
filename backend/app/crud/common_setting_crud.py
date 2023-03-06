from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from datetime import datetime
from app.models.common_setting_model import CommonSetting
from app.core.database import get_async_session


class CRUDCommonSetting:
    """
    設定関連のCRUD操作を行うクラス
    """
    
    async def get_settings(self, session: AsyncSession = Depends(get_async_session)) -> dict:
        """
        common_settingsテーブルから設定を取得
        """
        results = await session.exec(select(CommonSetting)).all()

        # key: value 形式の辞書に変換
        return {result.key: result.value for result in results}
      
common_setting = CRUDCommonSetting()