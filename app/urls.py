from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('user', views.UserResponse.as_view()),
    path('user/token', views.UserTokenResponse.as_view()),
])
