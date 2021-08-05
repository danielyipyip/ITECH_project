from typing import DefaultDict
from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH=128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    TITLE_MAX_LENGTH=128
    TAG_MAX_LENGTH=24
    Description_MAX_LENGTH=200
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    likes = models.ManyToManyField(User, related_name='page_post')
    views = models.IntegerField(default=0)
    tag = models.CharField(max_length=TAG_MAX_LENGTH, blank=True)
    description = models.TextField(max_length=Description_MAX_LENGTH)
    image = models.ImageField(upload_to='page_images', blank=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    page = models.ForeignKey(Page, on_delete=CASCADE, related_name="comments",)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="comments",)
