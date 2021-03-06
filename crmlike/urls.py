"""osla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from crmlike.views import BasePage, LoginView, LogoutView, RegistrationView, ChangeView, TaskListView


urlpatterns = [
    path('', BasePage.as_view(), name='base_page'),
    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),
    path('registrations/', RegistrationView.as_view(), name='registration_page'),
    path('change/', ChangeView.as_view(), name='change_page'),
    path('tasklist/', TaskListView.as_view(), name='tasklist_page'),
]
