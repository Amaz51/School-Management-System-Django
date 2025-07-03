from django.urls import path
from . import views
urlpatterns = [
    path('', views.StudentCreateandListView.as_view(), name='student-list-create'),
    path('<int:id>/',views.StudentDeleteView.as_view(),name="Delete_view"), 
    # path('register',views.RegisterView.as_view(),name='Register_view'),
    # path('login',views.LoginView.as_view(),name='login_view'),
    path('csrf/', views.csrf_token_view),
    path('list/', views.show_student_names, name='show-students'),
    path('student/by-email/', views.StudentByEmailView.as_view(), name='student_by_email'),
    path('bulkcreateusers/',views.BulkCreateUsers.as_view(),name='bulkcreateusers'),
    path('user/<str:username>/',views.User_update_and_delete_view.as_view(),name='userupdateanddelete'),
    path('test-celery/', views.test_celery, name='test_celery'),
    path('test-chain/', views.test_chain, name='test_chain'),
    path('reorder/', views.ReorderStudentsView.as_view(), name='reorder_students'),
]