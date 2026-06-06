from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .filters import TaskFilter


@extend_schema_view(
    list=extend_schema(summary="List all projects", tags=["Projects"]),
    create=extend_schema(summary="Create a project", tags=["Projects"]),
    retrieve=extend_schema(summary="Get a project", tags=["Projects"]),
    update=extend_schema(summary="Update a project", tags=["Projects"]),
    partial_update=extend_schema(summary="Partially update a project", tags=["Projects"]),
    destroy=extend_schema(summary="Delete a project", tags=["Projects"]),
)
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user).prefetch_related("tasks")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(summary="List tasks for a project", tags=["Projects"])
    @action(detail=True, methods=["get"], url_path="tasks")
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List all tasks",
        tags=["Tasks"],
        parameters=[
            OpenApiParameter("status", OpenApiTypes.STR, description="Filter by status (todo, in_progress, done)"),
            OpenApiParameter("priority", OpenApiTypes.STR, description="Filter by priority (low, medium, high)"),
            OpenApiParameter("project", OpenApiTypes.INT, description="Filter by project ID"),
            OpenApiParameter("search", OpenApiTypes.STR, description="Search by title"),
            OpenApiParameter("due_date_before", OpenApiTypes.DATE, description="Filter tasks due before date"),
            OpenApiParameter("due_date_after", OpenApiTypes.DATE, description="Filter tasks due after date"),
        ],
    ),
    create=extend_schema(summary="Create a task", tags=["Tasks"]),
    retrieve=extend_schema(summary="Get a task", tags=["Tasks"]),
    update=extend_schema(summary="Update a task", tags=["Tasks"]),
    partial_update=extend_schema(summary="Partially update a task", tags=["Tasks"]),
    destroy=extend_schema(summary="Delete a task", tags=["Tasks"]),
)
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ["created_at", "due_date", "priority", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).select_related("project", "assignee", "owner")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
