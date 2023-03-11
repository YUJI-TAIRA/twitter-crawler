# from sqlmodel import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import Depends
# from datetime import datetime
# from app.models.common_setting_model import CommonSetting
# from app.core.database import get_async_session


# class CRUDCommonSetting:
#     """
#     設定関連のCRUD操作を行うクラス
#     """

#     async def get_settings(
#         self, session: AsyncSession = Depends(get_async_session)
#     ) -> dict[str, str]:
#         """
#         common_settingsテーブルから設定を取得
#         """
#         results = await session.exec(select(CommonSetting)).all()

#         # key: value 形式の辞書に変換
#         return {result.key: result.value for result in results}

#     async def update_settings(
#         self,
#         new_settings: dict[str, str],
#         session: AsyncSession = Depends(get_async_session),
#     ) -> None:

#         # 対象データを取得
#         settings = await session.exec(
#             select(CommonSetting).where(CommonSetting.key.in_(new_settings.keys()))
#         ).all()

#         if settings:
#             for setting in settings:
#                 setting.value = new_settings[setting.key]
#             session.commit()
#         else:
#             raise ValueError("対象の設定が見つかりませんでした。")


# common_setting = CRUDCommonSetting()
