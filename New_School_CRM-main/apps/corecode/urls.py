   
from django.urls import path

from .views import (
    ClassCreateView,
    ClassDeleteView,
    ClassListView,
    ClassUpdateView,
    CurrentSessionAndTermView,
    IndexView,
    SessionCreateView,
    SessionDeleteView,
    SessionListView,
    SessionUpdateView,
    SiteConfigView,
    SubjectCreateView,
    SubjectDeleteView,
    SubjectListView,
    SubjectUpdateView,
    TermCreateView,
    TermDeleteView,
    TermListView,
    TermUpdateView,
)
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import profile_view
# from .views import CustomPasswordResetView
from .views import custom_password_reset
from .views import password_reset_confirm, password_reset_complete



urlpatterns = [
    path("", IndexView.as_view(), name="home"),

    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),

    # path('login/', auth_views.LoginView.as_view(), name='login'),

    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.custom_login_view, name='login'),

    path('principal/dashboard/', views.principal_index, name='principal_index'),
    path('staff/dashboard/', views.staff_index, name='staff_index'),
    path('student/dashboard/', views.student_index, name='student_index'),

    # path('login/', views.LoginView.as_view(), name='login'),
# path('dashboard/', views.dashboard_view, name='dashboard'),

    ####### for forgot password urls...
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='forgotpassword.html'), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


 ############## Old urls for forgot password

    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='corecode/password-reset.html'), 
        #  auth_views.PasswordResetView.as_view(template_name='forgotpassword.html'), 
         name='password_reset'),
    # path('password_reset/done/', 
    #      auth_views.PasswordResetDoneView.as_view(template_name='corecode/password-reset-done.html'), 
    #      name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='corecode/password-reset-confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='corecode/password-reset-complete.html'), 
         name='password_reset_complete'),


    ########## new urls for forgot password

    # path('password_reset/', 
    #      auth_views.PasswordResetView.as_view(template_name='corecode/password-reset.html'), 
    #      name='password_reset'),
    # path('password_reset/done/', 
    #      auth_views.PasswordResetDoneView.as_view(template_name='corecode/password-reset.html'), 
    #      name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', 
    #      auth_views.PasswordResetConfirmView.as_view(template_name='corecode/password-reset-confirm.html'), 
    #      name='password_reset_confirm'),
    # path('reset/done/', 
    #      auth_views.PasswordResetCompleteView.as_view(template_name='corecode/password-reset-complete.html'), 
    #      name='password_reset_complete'),


    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='corecode/password-reset.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='corecode/password-reset-confirm.html'), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password-reset-complete.html'), name='password_reset_complete'),


    # path('password_reset/', send_password_reset_email, name='password_reset'),
    # path('password_reset/done/', password_reset_done, name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', password_reset_complete, name='password_reset_complete'),





    # path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
 

    path("site-config", SiteConfigView.as_view(), name="configs"),
    path("current-session/", CurrentSessionAndTermView.as_view(), name="current-session"),
    path("session/list/", SessionListView.as_view(), name="sessions"),
    path("session/create/", SessionCreateView.as_view(), name="session-create"),
    path(
        "session/<int:pk>/update/",
        SessionUpdateView.as_view(),
        name="session-update",
    ),
    path(
        "session/<int:pk>/delete/",
        SessionDeleteView.as_view(),
        name="session-delete",
    ),
    path("term/list/", TermListView.as_view(), name="terms"),
    path("term/create/", TermCreateView.as_view(), name="term-create"),
    path("term/<int:pk>/update/", TermUpdateView.as_view(), name="term-update"),
    path("term/<int:pk>/delete/", TermDeleteView.as_view(), name="term-delete"),
    path("class/list/", ClassListView.as_view(), name="classes"),
    path("class/create/", ClassCreateView.as_view(), name="class-create"),
    path("class/<int:pk>/update/", ClassUpdateView.as_view(), name="class-update"),
    path("class/<int:pk>/delete/", ClassDeleteView.as_view(), name="class-delete"),
    path("subject/list/", SubjectListView.as_view(), name="subjects"),
    path("subject/create/", SubjectCreateView.as_view(), name="subject-create"),
    path(
        "subject/<int:pk>/update/",
        SubjectUpdateView.as_view(),
        name="subject-update",
    ),
    path(
        "subject/<int:pk>/delete/",
        SubjectDeleteView.as_view(),
        name="subject-delete",
    ),
]
