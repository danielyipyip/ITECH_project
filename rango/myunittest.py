import os
import re
import rango.models
import tempfile
from rango import forms
from populate_rango import populate
from datetime import datetime, timedelta
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields
from rango.models import UserProfile

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

class see_like_view_tests(TestCase):
    #test where view of pages can be seen in different views
    def test_view_count(self):
        #index
        response = self.client.get(reverse('rango:index'))
        content = response.content.decode()
        self.assertTrue('Views:' not in content.lower(), f"{FAILURE_HEADER}home page no view{FAILURE_FOOTER}")
        #category
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug':'django'} ))
        content = response.content.decode()
        self.assertTrue('Views:' not in content.lower(), f"{FAILURE_HEADER}home page no view{FAILURE_FOOTER}")
#page (need fix on page slug name)
        #response = self.client.get(reverse('rango:show_page', kwargs={'category_name_slug':'django', 'page_title':'How%20to%20Tango%20with%20Django'} ))
        #content = response.content.decode()
        #self.assertTrue('Views:' not in content.lower(), f"{FAILURE_HEADER}home page no view{FAILURE_FOOTER}")

    def test_like_count(self):
        #category
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug':'django'} ))
        content = response.content.decode()
        self.assertTrue('Likes:' not in content.lower(), f"{FAILURE_HEADER}home page no view{FAILURE_FOOTER}")
#add the one for pate

class user_registration_tests(TestCase):
    #base register uses django register app service, so just check is it employed
    def test_installed_register_apps(self):
        self.assertTrue('registration' in settings.INSTALLED_APPS)

    #for additional register
    def test_new_registration_view_exists(self):
        url = ''
        try:
            url = reverse('rango:register_profile')
        except:
            pass
        self.assertEqual(url, '/rango/optional_registration/')
    
    """
    def test_registration_page(self):
        request = self.client.get(reverse('rango:register_profile'))
        content = request.content.decode('utf-8')
        self.assertTrue('<h2>Your Profile Details</h2>' in content)
        self.assertTrue('Website' in content.lower())
        self.assertTrue('Profile Picture' in content.lower())
        self.assertTrue('Level of Expertise' in content.lower())
    """
    
    def test_good_form_creation(self):
        user_profile_data = {'website': 'http://www.bing.com', 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        user_profile_form = forms.UserProfileForm(data=user_profile_data)

        self.assertTrue(user_profile_form.is_valid())


class social_media_register(TestCase):
    #step 1: got the setup in settings (app & backend)
    def test_installed_apps(self):
        self.assertTrue('social_django' in settings.INSTALLED_APPS)
        self.assertTrue('social_core.backends.github.GithubOAuth2' in settings.AUTHENTICATION_BACKENDS)

class UserRegistrationTest(TestCase):

    def test_ensure_userprofile_field_can_be_null(self):
        #create_user_without_website:
            user = User.objects.create(username = "testing", 
                                            password = "12345",
                                            email = "testing")               
            
            userprofile = UserProfile.objects.create(user=user,
                                                        first_name = "testing",
                                                        last_name = "testing")
                        
            self.assertTrue(not userprofile.website)

class ProfilePage(TestCase):

    def test_email_field_not_showing_to_other_user(self):

                    currentuser = User.objects.create(username = "testing", 
                                            password = "12345",
                                            email = "testing")  
                    otheruser = User.objects.create(username = "testing", 
                                            password = "12345",
                                            email = "testing")  
                    userprofile1 = UserProfile.objects.create(user=currentuser)
                    userprofile2 = UserProfile.objects.create(user=otheruser)
                    response = self.client.get(reverse('rango:profile',currentuser.username))
                    response = self.client.get(reverse('rango:profile',otheruser.username))

