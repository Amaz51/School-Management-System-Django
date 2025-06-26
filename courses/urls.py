from django.urls import path
from . import views
urlpatterns = [
    path('', views.StudentCreateandListView.as_view(), name='student-list-create'),
]