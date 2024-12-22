from django.urls import path
from . import views as v

app_name = 'accounts'
urlpatterns = [
    path('register',v.register,name='register'),
    path('login/',v.loginpage,name='login'),
    path('logout',v.logoutpage,name='logout'),
    
]
