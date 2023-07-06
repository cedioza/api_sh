from django.urls import path
from shell_runner.views import execute_shell_command

urlpatterns = [
    path('shell/', execute_shell_command),
]
