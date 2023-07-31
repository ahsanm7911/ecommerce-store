from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .import views

# add url patterns here

urlpatterns = [
    path('addresses/', views.addresses, name='addresses'),
    path('addresses/add-address/', views.add_address, name='add_address'),
    path('addresses/edit-address/', views.edit_address, name='edit_address'),    
    path('addresses/edit-address/done', views.edit_address_done, name='edit_address_done'),    
    path('addresses/delete-address/', views.delete_address, name='delete_address'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('reset-password/', views.reset_password, name='reset_password'),
    path('signup/', views.signup, name='signup'),
    path('account/', views.myaccount, name='myaccount'),

    # password reset urls
    path(
        "password_change/", auth_views.PasswordChangeView.as_view(template_name='accounts/password_reset/password_change.html'), name="password_change"
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_reset/password_change_done.html'),
        name="password_change_done",
    ),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset/password_reset.html',
        email_template_name='accounts/password_reset/password_reset_email.html',
        subject_template_name='accounts/password_reset/password_reset_subject.txt'),
        name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset/password_reset_done.html'),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset/password_reset_form.html'),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]   

