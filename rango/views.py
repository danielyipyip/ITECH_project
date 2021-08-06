from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from rango.models import Category, Comment
from rango.models import Page
from rango.forms import CategoryForm, CommentForm, PageForm
# from rango.forms import UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseRedirect
from rango.models import UserProfile
from rango.forms import UserProfileForm
from registration.backends.default.views import RegistrationView
from django.views.generic.base import RedirectView
from django.contrib.auth.models import User
from rango.models import UserProfile
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    try:
        context_dict['special_pages'] = Page.objects.order_by('-views')[4]
    except IndexError:  #add for unit test
        context_dict['special_pages'] = Page.objects.order_by('-views').first()

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
            pages = Page.objects.filter(category=category).order_by('-views')[:]
        else:
            pages = Page.objects.filter(category=category).order_by('-like')[:]
# Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
# We also add the category object from the database to the context dictionary.
# We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        comments={}
        for page in pages:
            comments[page.title]=Comment.objects.filter(page=page).order_by('-likecount').first()
        context_dict['comments']=comments
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
        context_dict['comments']=None
    return render(request, 'rango/category.html', context=context_dict)


def show_page(request, category_name_slug, page_title,):
    context_dict = {}
    page = Page.objects.get(title=page_title)
    #page.views = page.views + 1
    #page.save()

    comments = Comment.objects.filter(page=page)
    category = Category.objects.get(slug=category_name_slug)
    likes_count = page.likes.count()

    if page.likes.filter(id=request.user.id).exists():
        liked = True
    else:
        liked = False
    
    if page.bookmark.filter(id=request.user.id).exists():
        is_bookmarked = True
    else:
        is_bookmarked = False

    if request.method == 'POST':
        cmform = CommentForm(request.POST or None)
        if cmform.is_valid():
            input = request.POST.get('input')
            comment = Comment.objects.create(page=page, user=request.user, input=input)
            comment.save()
            return redirect(reverse('rango:show_page',kwargs={'category_name_slug':category_name_slug, 'page_title':page.title}))
    else:
        cmform = CommentForm()

    context_dict['page'] = page
    context_dict['likes_count'] = likes_count
    context_dict['liked'] = liked
    context_dict['category'] = category
    context_dict['comments'] = comments
    context_dict['form'] = cmform
    context_dict['is_bookmarked'] = is_bookmarked
    return render(request, 'rango/page.html', context=context_dict)

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
                user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
                page.tag = user_profile.level
                page.uploader = request.user.username
                if 'image' in request.FILES:
                    page.image = request.FILES['image']
                page.save()
                return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

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

def like(request, pk):
    page = get_object_or_404(Page, id=request.POST.get('page_id'))
    liked = False
    if page.likes.filter(id=request.user.id).exists():
        page.likes.remove(request.user)
        liked = False
    else:
        page.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('rango:show_page',kwargs={'category_name_slug':page.category.slug , 'page_title':page.title}))

def like_count(request):
    page = Page.objects.get(title=request.GET.get('page_title', None))
    likes_count = page.likes.count()
    data = {
        'likse': like_count
    }
    return JsonResponse(data)

def likecomment(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    page = comment.page

    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('rango:show_page',kwargs={'category_name_slug':page.category.slug , 'page_title':page.title}))

@login_required
def register_profile(request):

    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
        return redirect(reverse('rango:registration_completed'))
    else:
        print(form.errors)
        context_dict = {'form': form}
        return render(request, 'rango/optional_registration.html', context_dict)

class LinkRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        page = get_object_or_404(Page, pk=kwargs['pk'])
        page.update_count()
        return page.url


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        form = UserProfileForm({
                                'first_name':user_profile.first_name,
                                'last_name':user_profile.last_name,
                                'level' : user_profile.level,
                                'website': user_profile.website,
                                'picture': user_profile.picture})
        
        return (user, user_profile, form)
    
    @method_decorator (login_required)
    def get(self,request,username):

        context_dict = {}
        
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        context_dict ['message']=''
        context_dict ['user_profile'] = user_profile
        context_dict ['selected_user']= user
        context_dict ['form'] = form

        context_dict = {'message' : '',
                        'user_profile': user_profile,
                        'selected_user': user,
                        'form': form,
                        'bookmark_pages':user.bookmark.all()}

        return render(request, 'rango/userprofile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        context_dict = {}
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if form.is_valid():
            form.save(commit=True)
            context_dict ['message']='Your profile has been succuessfully updated!'
            context_dict ['user_profile'] = user_profile
            context_dict ['selected_user']= user
            context_dict ['form'] = form
            return render(request, 'rango/userprofile.html', context_dict)

        else:
            print(form.errors)
def registration_completed(request):
    context_dict={ 'message' : 'Congratulations! Your account is now successfully created.' }
    response = render(request, 'rango/registration_completed.html',context=context_dict)
    return response

def bookmark_page(request, id):
    page = get_object_or_404(Page, id=id)
    if page.bookmark.filter(id=request.user.id).exists():
       page.bookmark.remove(request.user)
    else:
        page.bookmark.add(request.user)
    return HttpResponseRedirect(reverse('rango:show_page',kwargs={'category_name_slug':page.category.slug , 'page_title':page.title}))

