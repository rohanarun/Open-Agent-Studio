from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from datetime import datetime, timedelta
from apscheduler.schedulers.qt import QtScheduler
from apscheduler.schedulers.background import BackgroundScheduler

class CronSchedule():
  def __init__(self):
    self.cronjb = []
    self.jobstores = {
      'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    self.executors = {
      'default':{'type': 'threadpool', 'max_workers':20},
      'processpool':ProcessPoolExecutor(max_workers=5)
    }
    self.job_defaults = {
      'coalesce': False,
      'max_instances' : 3
    }
    self.scheduler = QtScheduler()
    self.scheduler.configure(jobstores=self.jobstores, executors=self.executors, job_defaults=self.job_defaults)

  def start(self):
    self.scheduler.start()

  def addJob(self, func, cronjb, args):
    self.cronjb = cronjb
    self.scheduler.add_job(func, trigger='cron',
      second = self.cronjb['seconds'],
      minute = self.cronjb['minute'],
      hour = self.cronjb['hour'],
      week = self.cronjb['week'],
      day = self.cronjb['day'],
      day_of_week = self.cronjb['weekday'],
      month = self.cronjb['month'],
      start_date = self.cronjb['startDate'],
      end_date = self.cronjb['endDate'],
      id = self.cronjb['id'], args=args)

  def view_job(self, id):
    return self.scheduler.get_job(id)

  def view_jobs(self):
    return self.scheduler.get_jobs()

  def removeJob(self, id):
    return self.scheduler.remove_job(id)

  def removeJobs(self, id):
    return self.scheduler.remove_all_job(id)
    