# Django Rest Framework
from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet

# Third Party
from django_filters.rest_framework import DjangoFilterBackend

# App
from creta import pagination
from creta.models import ApiHistory
from creta.serializers import ApiHistorySerializer

# Variables
name_search_fields = ['name', 'name_en', 'name_ja', 'name_ko']


# Classes
class BaseGenericViewSet(GenericViewSet):
    search_fields = name_search_fields
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    pagination_class = pagination.DefaultPagination


class ApiHistoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseGenericViewSet
):
    queryset = ApiHistory.objects.all()
    serializer_class = ApiHistorySerializer

    search_fields = ('title',)
    ordering_fields = ('id', 'created',)
    filterset_fields = []

