#from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .UseCase import ObterTramitacaoDocumentoUseCase

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ObterTramitacaoDocumentoUseCase.handlerScheduled, 'interval', seconds=10)
    scheduler.start()
    