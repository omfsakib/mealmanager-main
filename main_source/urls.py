from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('token/',views.token_send,name="token_send"),
    path('success/',views.success,name="success"),
    path('verify/<auth_token>',views.verify,name="verify"),
    path('error/',views.error_page,name='error'),
    path('join/mess/',views.joinMess,name='join_mess'),
    path('create/mess/',views.createMess,name='create_mess'),
]