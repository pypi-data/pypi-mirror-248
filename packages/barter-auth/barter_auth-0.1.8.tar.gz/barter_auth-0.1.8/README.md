# Barter authentication package

This package allows you to authorize users through a shared redis

## Install package
```shell
pip install barter-auth
```

## Define env variables

- `REDIS_AUTH_URL` default 'redis://localhost:6378/1' # depracated
- `REDIS_AUTH_HOST` default '127.0.0.1'
- `REDIS_AUTH_PORT` default 6379
- `REDIS_AUTH_PASSWORD` default None
- `REDIS_AUTH_DB` default 0
- `REDIS_AUTH_ACCESS_PREFIX` default = 'access'
- `REDIS_AUTH_REFRESH_PREFIX` default = 'refresh'
- `REDIS_AUTH_TOTP_PREFIX` default = 'totp'
- `REDIS_AUTH_PROFILE_PREFIX` default = 'profile'
- `REDIS_AUTH_TOKEN_STORAGE` default = 'headers'

## Use in view

```python
# in django 
from rest_framework.permissions import AllowAny, IsAuthenticated
from barter_auth.auth import ApiTokenRedisAuthentication
class SomeView(APIView):
    authentication_classes = [ApiTokenRedisAuthentication]
    permission_classes = [IsAuthenticated]
    
# barter_auth BaseUser() is available in request.user  in DRF APIView 

```
## Use in AppConfig   for   request.profie
```python
# you can add request user or profile in apps django config  <app_name>.apps.py

from django.apps import AppConfig
from django.http import HttpRequest

def get_profile(self):
    from barter_auth.providers import RedisProfileClient
    from barter_auth.models import AnonymousProfile
    if self.user.is_authenticated:
        try:
            return RedisProfileClient().get_profile(uuid=self.headers.get('Profile'))
        except:
            pass
    return AnonymousProfile()

class ProfilesConfig(AppConfig):
    name = "apps.<appp_name>"

    def ready(self):
        HttpRequest.profile = property(get_profile)

```


## in the same way  for  request.extuser
```python
# you can add request user or profile in apps django config  <app_name>.apps.py

from django.apps import AppConfig
from django.http import HttpRequest

def get_user(self):
    from barter_auth.providers import RedisAccessClient
    from barter_auth.auth import (
        get_token_from_header, get_token_from_cookies,
    )
    from django.contrib.auth.models import AnonymousUser

    token = get_token_from_header(self)
    if not token:
        token = get_token_from_cookies(self)
    if token:
        token_service = RedisAccessClient()
        user = token_service.get_user(token)
        return user or AnonymousUser()
    return AnonymousUser()

class ProfilesConfig(AppConfig):
    name = "apps.<appp_name>"

    def ready(self):
        HttpRequest.extuser = property(get_user)
    
    

```
