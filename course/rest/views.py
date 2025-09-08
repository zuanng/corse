from rest.models import Breed, Cat
from rest_framework import viewsets, filters, status
from rest_framework.pagination import PageNumberPagination
from rest.serializers import BreedSerializer, CatSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CatFilter

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

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
    
    # Ghi đè các phương thức để xử lý lỗi và trả về status codes
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response(response.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {"error": "Breed with this name already exists"}, 
                status=status.HTTP_409_CONFLICT
            )

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response(response.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Breed not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.cat_set.exists():
                return Response(
                    {"error": "Cannot delete breed with associated cats"},
                    status=status.HTTP_409_CONFLICT
                )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response(
                {"error": "Breed not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
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
    
    
    # Ghi đè các phương thức để xử lý lỗi và trả về status codes
    def create(self, request, *args, **kwargs):
        try:
            # Validate breed exists
            breed_id = request.data.get('breed')
            try:
                Breed.objects.get(pk=breed_id)
            except ObjectDoesNotExist:
                return Response(
                    {"error": "Specified breed does not exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            response = super().create(request, *args, **kwargs)
            return Response(response.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            # Validate breed exists if being updated
            breed_id = request.data.get('breed')
            if breed_id:
                try:
                    Breed.objects.get(pk=breed_id)
                except ObjectDoesNotExist:
                    return Response(
                        {"error": "Specified breed does not exist"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
            response = super().update(request, *args, **kwargs)
            return Response(response.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Cat not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response(
                {"error": "Cat not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        