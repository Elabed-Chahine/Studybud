from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name= 'home'),
    path('room/<int:pk>/',views.room,name= 'room'),
    path('room-form/', views.create_room, name='room-form'),
    path('update-room/<int:pk>/', views.update_room, name='update-room'),
    path('deleteRoom/<int:pk>/', views.deleteRoom, name='deleteRoom'),
    path('user_login/', views.login_user, name="user_login"),
    path('register_user/', views.register_user, name="register_user"),
    path('user_logout/', views.logoutUser, name="user_logout"),
    path('delete_comment/<int:pk>', views.deleteComment, name="delete_comment"),
    path('user_profile/<int:pk>', views.userProfile, name="user_profile"),
    path('update_user/', views.update_user, name="update_user"),
]