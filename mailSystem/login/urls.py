from django.urls import path
from login import views


app_name = 'login'


urlpatterns = [
    path('readmail/<int:rmail_id>/', views.readmail, name='readmail'),
]