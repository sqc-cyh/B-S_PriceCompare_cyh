from django.urls import path
from . import users_views

urlpatterns = [
    path('create-user/', users_views.create_user, name = 'create-user'),
    path('send-captcha/', users_views.send_captcha, name='send-captcha'),  # 添加发送验证码的视图
    path('verify-captcha/', users_views.verify_captcha, name='verify-captcha'),  # 添加验证验证码的视图
    path('register/', users_views.register, name='register'),
    path('login/', users_views.login, name='login'),
]