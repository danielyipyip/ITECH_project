from django.shortcuts import render
# from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm
# from rango.forms import UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    context_dict['special_pages'] = Page.objects.order_by('-views')[6]

    visitor_cookie_handler(request)
    # Obtain our Response object early so we can add cookie information.
    return render(request, 'rango/index.html', context=context_dict)
    #return response

def about(request):
    context_dict={'boldmessage': 'This tutorial has been put together by Daniel'}
    visitor_cookie_handler(request)
    context_dict['visits']=request.session['visits']
    response = render(request, 'rango/about.html', context=context_dict)
    return response

def show_category(request, category_name_slug, sort_method='views'):
# Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    try:
# The .get() method returns one model instance or raises an DoesNotExist exception.
        category = Category.objects.get(slug=category_name_slug)
# Retrieve all page; filter() will return a list of page objects/ empty list.
        if (sort_method=='views'):
            pages = Page.objects.filter(category=category).order_by('-views')
        else:
            pages = Page.objects.filter(category=category).order_by('-like')
# Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
# We also add the category object from the database to the context dictionary.
# We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
    # Have we been provided with a valid form?
    if form.is_valid():
    # Save the new category to the database.
        cat = form.save(commit=True)
        return redirect('/rango/')
    else:
        print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request,category_name_slug):
    #need to test is category exist first
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    # cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')

    form = PageForm() #place holder?
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save() #will this leak pw??
#             user.set_password(user.password) #hash pw
#             user.save()

#             profile = profile_form.save(commit=False) #delay save, no user yet
#             profile.user = user
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture'] #if uploaded pic, add
#             profile.save()
#             registered=True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else: #NOT HTTP POST-> render 2 model form instance (empty form)
#         #so 1st start is get-> will generate empty form??
#         user_form=UserForm()
#         profile_form=UserProfileForm()

#     return render(request, 'rango/register.html', context={'user_form': user_form, 
#         'profile_form': profile_form, 'registered': registered})
    
# def user_login(request):
#     if request.method == 'POST':
# # use request.POST.get('<variable>') as opposed to request.POST['<variable>'], 
# # request.POST.get('<variable>') returns None , while request.POST['<variable>'] raise a KeyError exception.
#         username = request.POST.get('username')
#         password = request.POST.get('password')
# # Use Django's machinery to see if the username/password combination is valid - a User object is returned if it is.
#         user = authenticate(username=username, password=password)
# # If we have a User object, the details are correct, otherwise None (Python's way of representing the absence of a value)
#         if user:
#             if user.is_active:
# # if account valid and active, log the user in, send user back to the homepage.
#                 login(request, user)
#                 return redirect(reverse('rango:index'))
#             else:
#                 return HttpResponse("Your Rango account is disabled.")
#         else: # Bad login details, can't log the user in.
#             print(f"Invalid login details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")
#     else:# request not HTTP POST -> display login form (most likely be a HTTP GET.)
#         return render(request, 'rango/login.html') #blank dictionary object

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

# @login_required #only loged in can log out
# def user_logout(request):
#     logout(request)
#     return redirect(reverse('rango:index')) #return to home page

#helper method: 
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits