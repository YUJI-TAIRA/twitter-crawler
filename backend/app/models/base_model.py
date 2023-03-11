# from sqlalchemy.orm import Session
# from sqlalchemy import event, orm

# from sqlmodel import SQLModel, Field, DateTime
# import datetime


# class SoftDeletableModel(SQLModel):
#     """論理削除用のベースモデル"""

#     deleted_at: datetime = Field(default=None)


# @event.listens_for(Session, "do_orm_execute")
# def _add_filtering_deleted_at(execute_state):
#     """
#     論理削除用のフィルタを追加する
#     以下のようにすると論理削除済のデータも含めて取得可能
#     query(...).where(...).execution_options(include_deleted=True)
#     """
#     if (
#         execute_state.is_select
#         and not execute_state.is_column_load
#         and not execute_state.is_relationship_load
#         and not execute_state.execution_options.get("include_deleted", False)
#     ):
#         execute_state.statement = execute_state.statement.options(
#             orm.with_loader_criteria(
#                 SoftDeletableModel,
#                 lambda cls: cls.deleted_at.is_(None),
#                 include_aliases=True,
#             )
#         )
