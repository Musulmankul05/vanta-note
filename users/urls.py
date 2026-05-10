from django.urls import path

from users import views

urlpatterns = [
    path('auth/', views.LoginUserView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.logout_view, name='logout'),
]