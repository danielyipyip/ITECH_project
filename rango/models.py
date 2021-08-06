from typing import DefaultDict
from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.encoding import python_2_unicode_compatible

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
    likes = models.ManyToManyField(User, related_name='page_post', blank=True)
    views = models.IntegerField(default=0)
    tag = models.CharField(max_length=TAG_MAX_LENGTH, blank=True)
    description = models.TextField(max_length=Description_MAX_LENGTH)
    image = models.ImageField(upload_to='page_images', blank=True)
    bookmark = models.ManyToManyField(User, related_name="bookmark", blank=True)
    uploader = models.CharField(max_length=128, blank=True)

    def update_count(self):
        self.views = self.views + 1
        self.save()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    LEVEL_CHOICES =(
    ("",''),   
    ("Beginner",'beginner'),
    ("Junior Developer",'junior'),
    ("Senior Developer",'senior'),
    ("Professional",'professional'),
    )
    level = models.CharField(choices = LEVEL_CHOICES,max_length=200, blank=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    page = models.ForeignKey(Page, on_delete=CASCADE, related_name="comment",)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="comment",)
    input = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_like')
    likecount = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s - %s' %(self.user.username, self.page.title, self.time)

class Bookmark(models.Model):
    page = models.ForeignKey(Page, on_delete=CASCADE, related_name="bookmark_page")
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="bookmark_user")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.page.title
