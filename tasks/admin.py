from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "task_count", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "owner__username"]

    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = "Tasks"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "priority", "project", "owner", "due_date", "created_at"]
    list_filter = ["status", "priority", "project"]
    search_fields = ["title", "owner__username"]
