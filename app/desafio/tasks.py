# from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .usecase import ObterTramitacoesUseCase


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ObterTramitacoesUseCase.handlerScheduled,
                      'interval', minutes=1)
    scheduler.start()
