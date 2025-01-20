import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news_app.utils import send_weekly_newsletters  # импортируем вашу функцию для отправки писем

logger = logging.getLogger(__name__)

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Добавляем задачу для отправки писем каждую неделю
        scheduler.add_job(
            send_weekly_newsletters,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"  # выполнение каждую неделю в понедельник в 00:00
            ),
            id="send_weekly_newsletters",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job 'send_weekly_newsletters'.")

        # Добавляем задачу для удаления старых записей о выполненных задачах
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
