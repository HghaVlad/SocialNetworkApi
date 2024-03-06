import re
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.utils import timezone

# Create your models here.


class Country(models.Model):
    name = models.TextField(blank=True, null=True)
    alpha2 = models.TextField(blank=True, null=True, unique=True)
    alpha3 = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    username_validator = UnicodeUsernameValidator()

    login = models.CharField(max_length=30, unique=True, validators=[username_validator],
                             error_messages={"unique": "A user with that username already exists"})
    email = models.EmailField(max_length=50, unique=True, blank=False, null=False)
    countryCode = models.CharField(max_length=2, blank=False, null=False)
    isPublic = models.BooleanField(blank=False, null=False)
    phone = models.TextField(unique=True, max_length=20, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'password', 'countryCode', 'isPublic']

    def set_password(self, raw_password):
        if len(raw_password) >= 6 and re.search(r'[A-Z]', raw_password) \
                and re.search(r'[a-z]', raw_password) and re.search(r'\d', raw_password):
            super().set_password(raw_password)
            self.save()
            return True

        return False

    def add_friend(self, friend):
        if not Follow.objects.filter(follower=self, following_user=friend).exists()\
                and self != friend:
            following = Follow()
            following.add(self, friend)

    def remove_friend(self, friend):
        if Follow.objects.filter(follower=self, following_user=friend).exists():
            Follow.objects.filter(follower=self, following_user=friend).delete()


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_relations')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_relations')
    addedAt = models.DateTimeField()

    class Meta:
        unique_together = ('follower', 'following_user',)

    def add(self, user, friend):
        self.follower = user
        self.following_user = friend
        self.addedAt = timezone.now()
        self.save()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    content = models.TextField(max_length=1000, blank=True, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = ArrayField(models.CharField(max_length=20, blank=True), size=1000, blank=True)
    createdAt = models.DateTimeField(default=timezone.now)
    likesCount = models.IntegerField(default=0)
    dislikesCount = models.IntegerField(default=0)

    def like(self, user):
        if not Like.objects.filter(author=user, post=self).exists():
            new_like = Like(author=user, post=self)
            new_like.save()
            self.likesCount += 1

        if Dislike.objects.filter(author=user, post=self).exists():
            Dislike.objects.filter(author=user, post=self).delete()
            self.dislikesCount -= 1
        self.save()

    def dislike(self, user):
        if not Dislike.objects.filter(author=user, post=self).exists():
            new_like = Dislike(author=user, post=self)
            new_like.save()
            self.dislikesCount += 1

        if Like.objects.filter(author=user, post=self).exists():
            Like.objects.filter(author=user, post=self).delete()
            self.likesCount -= 1
        self.save()


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Dislike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
