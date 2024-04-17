# Create your models here.
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.shortcuts import reverse
from .tasks import send_post_notification


# Model Author create
class Author(models.Model):
    a_user = models.OneToOneField(User, on_delete=models.CASCADE)  # one-to-one relationship with User model
    a_rating = models.IntegerField(default=0)  # user rating

    def __str__(self):
        return self.a_user

    def update_rating(self):  # method that updates the author rating
        # the total rating of each article
        pr_0 = self.post_set.all().aggregate(post_rating=Sum('rating_post'))
        # the total rating of all comments by the author
        cr_0 = self.a_user.comment_set.all().aggregate(comment_rating=Sum('rating_comment'))
        # total rating of comments to the author's articles
        dr_0 = self.post_set.all().aggregate(comment_rating=Sum('comment__rating_comment'))

        if pr_0.get('post_rating') is None:
            pr_1 = int(0)

        else:
            pr_1 = int(pr_0.get('post_rating'))

        if cr_0.get('comment_rating') is None:
            cr_1 = int(0)

        else:
            cr_1 = int(cr_0.get('comment_rating'))

        if dr_0.get('comment_rating') is None:
            dr_1 = int(0)

        else:
            dr_1 = int(dr_0.get('comment_rating'))

        # update the author rating
        self.a_rating = pr_1 * 3 + cr_1 + dr_1
        self.save()


# Model Category
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)  # category name, unique

    def __str__(self):
        return self.name

    def post_count(self):
        return Post.objects.filter(post_category=self).count()

# Model Post
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # one-to-many relationship with Author model
    post_type = models.CharField(max_length=16, choices=[('A', 'article'), ('N', 'news')],
                                 default='A')  # field with choice - 'article' or 'news'
    created_at = models.DateTimeField(auto_now_add=True)  # date and time of creation
    post_category = models.ManyToManyField(Category,
                                           through='PostCategory')  # many-to-many relationship with Category model
    title = models.CharField(max_length=256)  # article/news title
    content = models.TextField()  # article/news text
    rating_post = models.IntegerField(default=0)  # article/news rating

    def like(self):  # method that increases the rating by one
        self.rating_post += 1
        self.save()

    def dislike(self):  # method that decreases the rating by one
        self.rating_post -= 1
        self.save()

    def preview_124(
            self):  # method that returns the beginning of the article (preview) with 124 characters and adds an ellipsis at the end
        return self.content[:124] + '...'

    def preview_20(
            self):  # method that returns the beginning of the article (preview) with 124 characters and adds an ellipsis at the end
        return self.content[:21] + '...'

    def return_date(self):
        return self.created_at.strftime("%d.%m.%Y")

    def get_absolute_url(self):
        return reverse('detail_function', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        # If it's a new post (i.e., doesn't have an ID yet), send a notification after saving
        new_post = self.id is None

        super().save(*args, **kwargs)

        if new_post:
            send_post_notification.delay(self.id)


# Model PostCategory
class PostCategory(models.Model):
    post_key = models.ForeignKey(Post, on_delete=models.CASCADE)  # one-to-many relationship with Post model
    category_key = models.ForeignKey(Category, on_delete=models.CASCADE)  # one-to-many relationship with Category model


# Model Comment
class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)  # one-to-many relationship with Post model
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)  # one-to-many relationship with User model
    text = models.TextField()  # comment text
    created_at = models.DateTimeField(auto_now_add=True)  # date and time of creation
    rating_comment = models.IntegerField(default=0)  # comment rating

    def like(self):  # method that increases the rating by one
        self.rating_comment += 1
        self.save()

    def dislike(self):  # method that decreases the rating by one
        self.rating_comment -= 1
        self.save()


class Subscriber(models.Model):
    subscriber = models.OneToOneField(User, on_delete=models.CASCADE)  # one-to-one relationship with User model
    categories = models.ManyToManyField(Category)  # many-to-many relationship with Category model

    def __str__(self):
        return self.subscriber