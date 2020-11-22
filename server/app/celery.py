from celery import Celery


app = Celery('app', broker='amqp://', include=['app.tasks'])


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, app.tasks.test.s('hello'), name='test')
#     sender.add_periodic_task(5, app.tasks.sync.s(2), name='sync')

app.conf.beat_schedule = {
    "run-every-ten": {
        "task": "app.tasks.sync",
        "schedule": 10
    }
}


# if __name__ == 'main':
#     app.start()
