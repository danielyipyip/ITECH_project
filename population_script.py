import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page, Comment

def populate():
    #dictionary of pages
    python_pages = [
    {'title': 'Official Python Tutorial',
     'url':'http://docs.python.org/3/tutorial/', 
     'views':24,
     'tag': 'Junior Developer',
     'description': 'A very good webpage for learning python!!~',},

    {'title':'How to Think like a Computer Scientist',
     'url':'http://www.greenteapress.com/thinkpython/',
     'views':36, 
     'tag': 'Beginner',
     'description': 'Check these books~'},

    {'title':'Learn Python in 10 Minutes',
     'url':'http://www.korokithakis.net/tutorials/python/',
     'views':20, 
     'tag': 'Beginner',
     'description': 'If you do not have much time, this is the best page for you to learn python.'} ]

    django_pages = [
    {'title':'Official Django Tutorial',
     'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
     'views':19,
     'tag': 'Junior Developer',
     'description': 'Official tutorial for Django'},

    {'title':'Django Rocks',
     'url':'http://www.djangorocks.com/',
     'views':36,
     'tag': 'Senior Developer',
     'description': 'A Blog for django developer'},

    {'title':'How to Tango with Django',
     'url':'http://www.tangowithdjango.com/',
     'views':27,
     'tag': 'Junior Developer',
     'description': 'Good book for junior dev to learn Django'} ]

    other_pages = [
    {'title':'Bottle',
     'url':'http://bottlepy.org/docs/dev/',
     'views':33,
     'tag':'Professional',
     'description': 'Bottle page'},

    {'title':'Flask',
     'url':'http://flask.pocoo.org',
     'views':10, 
     'tag':'Senior Developer',
     'description': 'Flask page'} ]

    leisure_pages = [
    {'title':'Snake',
     'url':'http://snake.googlemaps.com/',
     'views':80,
     'tag':'Beginner',
     'description': 'Fun game to play~'},
    ]

    #dictionary of dictionaries
    cats = {'Python': {'pages': python_pages, 'views': 84, 'likes': 55},
    'Django': {'pages': django_pages, 'views': 85, 'likes': 64},
    'Other Frameworks': {'pages': other_pages, 'views': 20, 'likes': 10}, 
    'Leisure': {'pages': leisure_pages ,'views': 122, 'likes': 88}
    }

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['tag'], p['description'], p['views'],)

 # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, tag, description, views=0):
    #get_or_create return 2 elem tuple, so [0] to get 1st elem
    p = Page.objects.get_or_create(category=cat, title=title)[0] 
    p.url=url
    p.views=views
    p.tag=tag
    p.description=description
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

def add_cm(page, user, input, likes, likecount):
    cm = Comment.objects.get_or_create(page=page, user=user, input=input)[0]
    cm.page=page
    cm.user=user
    cm.input=input
    cm.likes.add(likes)
    cm.likecount=likecount
    return cm

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()