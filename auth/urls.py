from django.contrib import admin
from django.urls import path
from src.views import TwitterLoginVew

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/twitter/', TwitterLoginVew.as_view(), name='twitter_login')
]
