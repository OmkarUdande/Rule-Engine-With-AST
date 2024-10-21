from django.urls import path
from . import views

urlpatterns = [
    path('create_rule/', views.create_rule, name='create_rule'),  # Create rule URL
    path('evaluate/<int:user_id>/', views.evaluate, name='evaluate'),  # Evaluate URL
]
