from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_user, name='register_user'),
    path('token', views.generate_token, name='generate_token'),
    path('data', views.store_data, name='store_data'),
    path('data/<str:key>', views.retrieve_data, name='retrieve_data'),
    path('data/<str:key>', views.update_data, name='update_data'),
    path('data/<str:key>', views.delete_data, name='delete_data'),
]
