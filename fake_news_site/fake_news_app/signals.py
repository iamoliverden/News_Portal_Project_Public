from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from .models import *
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_notification(preview, pk, title, _subscribers):
    html_context = render_to_string('post_created_email.html',
                                    {'text': preview, 'link': f'{settings.SITE_URL}/fake_news_app/posts/{pk}',
                                     'title': title})
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=_subscribers,
    )
    msg.attach_alternative(html_context, "text/html")
    msg.send()


from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, Subscriber


@receiver(m2m_changed, sender=Post.post_category.through)
def notify_on_new_post_in_category(sender, instance, action, **kwargs):
    if action == "post_add":
        # instance here is a Post
        post = instance

        # Get all categories of the post
        categories = post.post_category.all()

        # For each category, get all subscribers
        for category in categories:
            subscribers = Subscriber.objects.filter(categories=category)

            # Get the email addresses of the subscribers
            subscriber_emails = [subscriber.subscriber.email for subscriber in subscribers]

            # Send the email notifications
            send_notification(post.preview_124(), post.pk, post.title, subscriber_emails)
