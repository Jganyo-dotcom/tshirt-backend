from django.urls import path
from . import views

urlpatterns = [
    
    path('submit_order/', views.submit_order, name='submit_order'),
    

]
