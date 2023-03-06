from sqlmodel import AsyncSession, select
from fastapi import Depends
from datetime import datetime
from app.models.incentive_model import IncentiveLog
from app.models.common_setting_model import CommonSetting
from app.core.database import get_async_session


class CRUDIncentive:
    """
    インセンティブ関連のCRUD操作を行うクラス
    """

    async def get_settings(self, session: AsyncSession = Depends(get_async_session)) -> dict:
        """
        incentive_settingsテーブルから設定を取得
        """
        query = select(CommonSetting)
        results = await session.exec(query).all()

        # key: value 形式の辞書に変換
        return {result.key: result.value for result in results}

    async def get_logs(
        self, month: str = None, session: AsyncSession = Depends(get_async_session)
    ) -> list[IncentiveLog]:
        """
        incentive_logsテーブルから、指定された月のログを取得

        Args:
            month (str, optional): 取得するログの月 YYYY-MM

        Returns:
            list[IncentiveLog]: 取得したIncentiveLogのリスト

        """
        query = select(IncentiveLog)
        if month is not None:
            query = query.where(IncentiveLog.month == month)
        return await session.exec(query).all()

    async def save_logs(self, incentive_logs: list[IncentiveLog]) -> None:
        """
        IncentiveLogを保存する。DB上に存在するログと突合し、upsertを実行する。

        Args:
            incentive_logs (list[IncentiveLog]): 保存するIncentiveLogのリスト。

        """
        if not incentive_logs:
            return

        existing_incentive_logs = await self.get_logs()
        existing_incentive_logs_dict = {incentive_log.twitter_id: incentive_log for incentive_log in existing_incentive_logs}
        upsert_incentive_logs = []

        for incentive_log in incentive_logs:
            # ログが存在する場合
            if incentive_log.twitter_id in existing_incentive_logs_dict:
                # ログが存在し、月が変更されている場合、ログを更新
                existing_incentive_log = existing_incentive_logs_dict[incentive_log.twitter_id]
                if existing_incentive_log.month != incentive_log.month:
                    upsert_incentive_logs.append(incentive_log)

                # ログを削除リストから削除し、DBから削除されないようにする
                del existing_incentive_logs_dict[incentive_log.twitter_id]
            else:
                # ログが存在しない場合は、upsertするリストに追加
                upsert_incentive_logs.append(incentive_log)


        # upsertを実行
        self.session.add_all(upsert_incentive_logs)
        await self.session.commit()

        # APIから取得されなかったログを削除
        if existing_incentive_logs_dict:
            delete_query = (
                IncentiveLog.__table__
                .update()
                .where(IncentiveLog.twitter_id.in_(existing_incentive_logs_dict.keys()))
                .values(deleted_at=datetime.utcnow())
            )
            # 実行
            await self.session.execute(delete_query)
            
incentive = CRUDIncentive()