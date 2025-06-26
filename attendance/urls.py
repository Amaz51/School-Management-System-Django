from django.urls import path
from . import views

urlpatterns = [
    path('', views.List_and_Create_View.as_view(), name='attendance_view'),
    path('<int:id>/', views.update_and_delete_view.as_view(),name='attendance_operations'),
    path('bulk-create/', views.BulkCreateView.as_view(), name='bulk_create'),
    path('bulk-update/', views.BulkUpdateView.as_view(), name='bulk_update'),
    #path('by-username/<str:username>', views.Attendance_by_username.as_view(), name='Attendance_by_username'),
    path('download', views.download_attendance_by_email, name='download_view'),
]


# urlpatterns = [
#     path('', views.List_and_Create_View.as_view(), name='attendance_view'),
#     path('<int:id>/', views.update_and_delete_view.as_view(),name='attendance_operations'),
#     path('register',views.RegisterView.as_view(),name='Register_view'),
#     path('login',views.LoginView.as_view(),name='login_view'),
#     path('csrf/', views.csrf_token_view),
#     path('bulk-create/', views.BulkCreateView.as_view(), name='bulk_create'),
#     path('bulk-update/', views.BulkUpdateView.as_view(), name='bulk_update'),
#     path('students/', views.show_student_names, name='show-students'),
#     #path('bulk-delete/', views.BulkDeleteView.as_view(), name='bulk_delete'),
# ]

