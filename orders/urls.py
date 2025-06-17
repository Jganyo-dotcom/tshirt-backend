from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = 'index'),
    path('submit_order/', views.submit_order, name='submit_order'),
    path('test-message/', views.test_message, name='test_message'),
    path('test-email/', views.test_email, name='test_email'),

]
