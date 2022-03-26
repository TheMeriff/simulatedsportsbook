"""simulated_sportsbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from simulated_sportsbook.rest_api.rest_views import UserViewSet, AccountViewSet, EventViewSet, BetslipViewSet
from users import views as user_views

from simulated_sportsbook import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'events', EventViewSet)
router.register(r'betslips', BetslipViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('refresh_odds/', views.refresh_odds, name='refresh_odds'),
    path('about_us/', views.about_us, name='about_us'),
    path('account/', views.account, name='account'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('register/login', user_views.login, name='register_redirect'),
    path('login/', user_views.login_request, name='login'),
    path('logout/', user_views.logout_request, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.index, name='login_redirect'),
    path('api-auth/', include('rest_framework.urls')),
    path('rest_api/', include(router.urls))
]
