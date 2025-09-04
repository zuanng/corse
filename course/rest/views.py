from rest.models import Breed, Cat
from rest_framework import viewsets, filters
from .pagination import CustomPageNumberPagination
from rest.serializers import BreedSerializer, CatSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CatFilter

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BreedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows breeds to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CatFilter
    search_fields = ['nickname', 'breed__name', 'foods']
    ordering_fields = ['nickname', 'weight']
    ordering = ['nickname']  # default ordering

class CatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cats to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = CustomPageNumberPagination