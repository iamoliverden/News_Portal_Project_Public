import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime
from datetime import timedelta
from fake_news_app.models import Subscriber, Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def my_job():
    # Your job processing logic here...
    today = datetime.today()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    categories = set(posts.values_list('post_category__name', flat=True))
    subscribers = Subscriber.objects.filter(categories__name__in=categories).values_list('subscriber__email', flat=True)
    html_content = render_to_string(
        'weekly_digest_email.html',
        {'link': settings.SITE_URL,
         'posts': posts,
         'categories': categories}
    )
    msg = EmailMultiAlternatives(
        subject='Weekly Digest',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),  # Every Friday at 18:00
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=3,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=3,
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
