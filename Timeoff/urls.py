from django.urls import path
from .views import (
    timeoff_create_view, 
    dynamic_lookup_view,
    timeoff_delete_view,
    timeoff_list_view,
)

app_name = 'timeoff'

urlpatterns = [
    path('<int:myid>/', dynamic_lookup_view, name='timeoff-detail'),
    path('create/', timeoff_create_view, name='timeoff-create'),
    path('<int:myid>/delete/', timeoff_delete_view, name='timeoff-delete'),
    path('', timeoff_list_view, name='timeoff-list'),
]