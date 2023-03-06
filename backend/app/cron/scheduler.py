from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

class Scheduler:
    def __init__(self, app: FastAPI):
        self.app = app
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

    def add_job(self, *args, **kwargs):
        self.scheduler.add_job(*args, **kwargs)

    def remove_job(self, *args, **kwargs):
        self.scheduler.remove_job(*args, **kwargs)

    def get_jobs(self, *args, **kwargs):
        return self.scheduler.get_jobs(*args, **kwargs)

    def shutdown(self, *args, **kwargs):
        self.scheduler.shutdown(*args, **kwargs)