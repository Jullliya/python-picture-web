from django.urls import path
from . import views

urlpatterns = [
    path('cnn_table/<str:key>/add', views.cnn_result_post),
    path('cnn_table/<str:key>/get', views.get_result),
    path('cnn_table/<str:key>/delete', views.delete_row),
    path('cnn_table/<str:key>/delete_all', views.delete_all),
    path('cnn_table/<str:key>/update', views.update_analyse, name='update_analyse'),
    path('classification-image/<str:key>', views.classification_image, name="classification_image")
]