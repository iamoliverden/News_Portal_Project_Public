from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task
from datetime import datetime, timedelta
from django.conf import settings

@shared_task
def send_post_notification(post_id):
    # Import the models here, not at the top of the file
    from .models import Post, Subscriber
    # Get the post
    post = Post.objects.get(id=post_id)

    # Get the subscribers of the post's category
    subscribers = Subscriber.objects.filter(categories=post.post_category)

    # Prepare the email
    subject = f"New post in {post.post_category.name}: {post.title}"
    html_message = render_to_string('post_notification_email.html', {'post': post})
    plain_message = strip_tags(html_message)

    # Send the email to all subscribers
    for subscriber in subscribers:
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [subscriber.subscriber.email], html_message=html_message)

@shared_task
def send_weekly_digest():
    # Import the models here, not at the top of the file
    from .models import Post, Subscriber
    # Get all posts from the past week
    one_week_ago = datetime.now() - timedelta(weeks=1)
    posts = Post.objects.filter(created_at__gte=one_week_ago)

    # Get all subscribers
    subscribers = Subscriber.objects.all()

    # Prepare the email
    subject = "Your weekly digest of news posts"
    html_message = render_to_string('weekly_digest_all_news_email.html', {'posts': posts})
    plain_message = strip_tags(html_message)

    # Send the email to all subscribers
    for subscriber in subscribers:
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [subscriber.subscriber.email], html_message=html_message)