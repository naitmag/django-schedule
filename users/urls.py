from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name="login"),
    # path('registration/', views.UserRegistrationView.as_view(), name="registration"),
    path('profile/<int:user_id>', views.UserProfileView.as_view(), name="profile"),
    path('profile/', views.UserProfileView.as_view(), name="profile"),
    path('logout/', views.logout, name='logout'),

]
