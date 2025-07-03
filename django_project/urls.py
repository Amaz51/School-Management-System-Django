from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('', lambda request: HttpResponse("Welcome to the API")),
    path('admin/', admin.site.urls),
    path('api/attendance/', include('attendance.urls')), 
    path('api/students/', include('students.urls')),
    path('api/ordering/', include('studentorder.urls')),
    # path('api/courses',include('courses.urls')),
    # path('api/classes',include('classes.urls')),
    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]