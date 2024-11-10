from django.urls import path
from . import views

urlpatterns = [
    path('cnn_table/<str:key>/add', views.cnn_result_post),
    path('cnn_table/<str:key>/get', views.get_result),
    path('cnn_table/<str:key>/delete', views.delete_row),
    path('classification-image', views.classification_image, name="classification_image")
]