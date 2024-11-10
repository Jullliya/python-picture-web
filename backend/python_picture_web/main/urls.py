from django.urls import path
from . import views

urlpatterns = [
    path('cnn_table/result', views.cnn_result_post),
    path('cnn_table/get', views.get_result),
    path('cnn_table/delete', views.delete_row)
]