from django.contrib import admin
from django.urls import path
from accounts.views import RegisterView
from tasks.views import TaskListCreateView, TaskDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Tasks
    path('api/tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
]
