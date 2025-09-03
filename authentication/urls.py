# Importing path function from django.urls
from django.urls import path
# Importing all views from authentication_view
from .views.authentication_view import *
# Importing views from rest_framework_simplejwt for JWT authentication
from rest_framework_simplejwt import views as jwt_views

# Defining the URL patterns
urlpatterns = [

    # URL pattern for logout
    path('logout', Logout.as_view(), name='logout'),
    
    # URL pattern for login
    path('login', Login.as_view(), name='login'),
    
    # URL pattern for token refresh
    path('token/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'),
]
