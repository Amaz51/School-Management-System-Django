from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserStudentOrderView.as_view(), name='student-order'),
    path('reorder/', views.ReorderStudentsView.as_view(), name='reorder-students'),
]
