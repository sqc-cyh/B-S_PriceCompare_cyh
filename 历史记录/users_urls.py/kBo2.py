from django.urls import path
from . import users_views

urlpatterns = [
    path('create-user/', users_views.create_user, name = 'create-user'),
    path('send-captcha/', users_views.send_captcha, name='send-captcha'),  # 添加发送验证码的视图
    path('verify-captcha/', users_views.verify_captcha, name='verify-captcha'),  # 添加验证验证码的视图
    path('register/', users_views.register, name='register'),
    path('login/', users_views.login, name='login'),
    path('search_suning/', users_views.search_suning, name='search_suning'),
    path('search_jd/', users_views.search_jd, name='search_jd'),
    path('history/',users_views.history, name='history')
    path('set_price_alert/',users_views.set_price_alert, name='set_price_alert')
]