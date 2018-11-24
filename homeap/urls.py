
from django.urls import path ,include
from . import views

urlpatterns = [
    path('', views.Home),
    path('getUserData',views.getUserData),

    path('signup/',views.signup),
    path('forgot/',views.forgot),   # pass the address in acrion as forgot then add / in back here
    path('follower',views.follower),
    path('following',views.following)
]