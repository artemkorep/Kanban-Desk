from functools import partialmethod
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import TaskLog


class TaskLogService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _save_log(self, task_id: int, user_id: int, message: str) -> TaskLog:
        log = TaskLog(task_id=task_id, user_id=user_id, message=message)
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log

    @staticmethod
    def _make_log_method(template: str):
        async def method(self, task_id: int, user_id: int, **kwargs):
            message = template.format(**kwargs)
            return await self._save_log(task_id, user_id, message)

        return method

    log_title_change = partialmethod(
        _make_log_method("Changed title: {old_title} → {new_title}")
    )
    log_description_change = partialmethod(
        _make_log_method("Changed description: {old_description} → {new_description}")
    )
    log_order_change = partialmethod(
        _make_log_method("Changed order: {old_order} → {new_order}")
    )
    log_column_change = partialmethod(
        _make_log_method("Changed column: {old_column_id} → {new_column_id}")
    )
    log_creation = partialmethod(_make_log_method("Task created: '{title}'"))
    log_change_due_date = partialmethod(
        _make_log_method("Task changed due date: {old_due_date} -> {new_due_date}")
    )
