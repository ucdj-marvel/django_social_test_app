# DjangoSNS認証テストAPP

[参考記事](https://hironsan.hatenablog.com/entry/django-rest-framework-social-oauth)

### 作成手順

```
$ mkdir django-social-auth && cd django-social-auth
$ pipenv install django djangorestframework django-allauth django-rest-auth
$ pipenv shell
(django-social-auth) $ django-admin startproject auth .
(django-social-auth) $ python manage.py startapp src
(django-social-auth) $ python manage.py migrate
(django-social-auth) $ python manage.py runserver
```

`auth/settings.py`
~~~python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # new
    'rest_framework.authtoken',  # new
    'rest_auth',  # new
    'django.contrib.sites',  # new
    'allauth',  # new
    'allauth.account',  # new
    'allauth.socialaccount',  # new
    'allauth.socialaccount.providers.twitter',  # new
]

SITE_ID = 1
~~~

```
$ python manage.py migrate
```

`src/views.py`
~~~python
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer

class TwitterLoginVew(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter
~~~

`auth/urls.py`
~~~python
from django.contrib import admin
from django.urls import path
from src.views import TwitterLoginVew

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/twitter/', TwitterLoginVew.as_view(), name='twitter_login')
]
~~~

```
$ python manage.py runserver
```

[http://127.0.0.1:8000/rest-auth/twitter/](http://127.0.0.1:8000/rest-auth/twitter/)を確認

![restframework](https://cdn-ak.f.st-hatena.com/images/fotolife/H/Hironsan/20190423/20190423083113.png)

1. [twitterdeveloper](https://developer.twitter.com/en/apps)へ移動
1. アプリケーションを作成
1. `Consumer Key` と `Access Token` を取得
    - ![Consumer Key & Access Token](https://cdn-ak.f.st-hatena.com/images/fotolife/H/Hironsan/20190423/20190423093744.png)
1. 取得したトークンはDjangoのadminページから設定する
    ```
    $ python manage.py createsuperuser
    $ python manage.py runserver
    ```
    - `http://127.0.0.1:8000/admin`へアクセス
    - ![admin](https://cdn-ak.f.st-hatena.com/images/fotolife/H/Hironsan/20190423/20190423095820.png)
1. siteを選択
    - ![site](https://cdn-ak.f.st-hatena.com/images/fotolife/H/Hironsan/20190423/20190423100022.png)
1. adminページから`Social Applications`を選択
    - Provider=Twitter、`Client ID`と`Secret key`に取得した`Consumer key`と`Consumer Secret`を入力
1. [http://127.0.0.1:8000/rest-auth/twitter/](http://127.0.0.1:8000/rest-auth/twitter/)へアクセス
    - 取得したTwitterの`Access Token`と`Access Token Secret`を入力してPOST

```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "key": "key~~~~~~~~~~~~~~~~~~~~~"
}
```
となっていれば認証に成功している