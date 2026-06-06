import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    due_date_before = django_filters.DateFilter(field_name="due_date", lookup_expr="lte")
    due_date_after = django_filters.DateFilter(field_name="due_date", lookup_expr="gte")
    search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ["status", "priority", "project", "assignee", "due_date_before", "due_date_after", "search"]
