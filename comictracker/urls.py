from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

app_name = 'comictracker'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.sign_in, name='login'),
    path('add', views.add_view, name='add'),
    path('create_record', views.record_view, name='create_record'),
    path('remove_record', views.remove_view, name='remove_record'),
]