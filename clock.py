from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minute1.')
    #python julbem_weekly.py

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=23)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()