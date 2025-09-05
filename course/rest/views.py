from rest.models import Breed, Cat
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest.serializers import BreedSerializer, CatSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CatFilter

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BreedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows breeds to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly)
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    queryset = Breed.objects.all()      
    serializer_class = BreedSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'cat_count']
    ordering = ['name']

    @method_decorator(cache_page(60 * 15))  # Cache trong 15 phút
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def get_queryset(self):
        """
        Tối ưu query bằng prefetch_related để lấy thông tin cats
        liên quan cho việc tính cat_count
        """
        return Breed.objects.prefetch_related('cat_set').all()
    
class CatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cats to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly)
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'cats' 

    serializer_class = CatSerializer
    pagination_class = CustomPageNumberPagination
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CatFilter
    search_fields = ['nickname', 'breed__name', 'foods']
    ordering_fields = ['nickname', 'weight']
    ordering = ['nickname']

    @method_decorator(cache_page(60 * 5))  # Cache trong 5 phút
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 5))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)   
        
    def get_queryset(self):
        """
        Tối ưu query bằng select_related để lấy thông tin breed
        liên quan trong cùng một query
        """
        return Cat.objects.select_related('breed').all()
        