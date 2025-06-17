from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = 'index'),
    path('submit_order/', views.submit_order, name='submit_order'),
    

]
