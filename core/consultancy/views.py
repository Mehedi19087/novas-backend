from .serializers import UpdateConsultancyServiceSerializer
from .services import update_consultancy_service
from core.content_views import ContentMutationMixin, ContentEditorPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import ConsultancyCategory, ConsultancyService
from .serializers import (
    CreateConsultancyCategorySerializer,
    ResponseConsultancyCategorySerializer,
    CreateConsultancyServiceSerializer,
    ResponseConsultancyServiceSerializer,
)
from .services import create_consultancy_category, create_consultancy_service


class ConsultancyCategoryListCreateAPIView(APIView):
    permission_classes = [ContentEditorPermission]

    def get(self, request):
        categories = ConsultancyCategory.objects.all().order_by('sort_order', 'name')
        serializer = ResponseConsultancyCategorySerializer(categories, many=True)
        return Response(
            {
                "message": "Consultancy categories retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CreateConsultancyCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category = create_consultancy_category(serializer.validated_data)
            response_serializer = ResponseConsultancyCategorySerializer(category)
            return Response(
                {
                    "message": "Consultancy category created successfully",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to create consultancy category due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ConsultancyCategoryDetailAPIView(APIView):
    def get(self, request, slug):
        category = get_object_or_404(
            ConsultancyCategory.objects.prefetch_related('services'),
            slug=slug
        )
        serializer = ResponseConsultancyCategorySerializer(category)
        services_serializer = ResponseConsultancyServiceSerializer(category.services.all(), many=True)
        return Response(
            {
                "message": "Consultancy category retrieved successfully",
                "data": {
                    **serializer.data,
                    "services": services_serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )


class ConsultancyServiceListCreateAPIView(APIView):
    permission_classes = [ContentEditorPermission]

    def get(self, request):
        queryset = ConsultancyService.objects.select_related('category').all()

        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__category_id=category) | queryset.filter(category__slug=category)

        featured = request.query_params.get('featured')
        if featured is not None:
            queryset = queryset.filter(featured=(featured.lower() in ['true', '1']))

        serializer = ResponseConsultancyServiceSerializer(queryset, many=True)
        return Response(
            {
                "message": "Consultancy services retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CreateConsultancyServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = create_consultancy_service(serializer.validated_data)
            response_serializer = ResponseConsultancyServiceSerializer(service)
            return Response(
                {
                    "message": "Consultancy service created successfully",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to create consultancy service due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ConsultancyServiceDetailAPIView(ContentMutationMixin, APIView):
    content_model = ConsultancyService
    update_serializer = UpdateConsultancyServiceSerializer
    response_serializer = ResponseConsultancyServiceSerializer
    update_service = staticmethod(update_consultancy_service)

    def get(self, request, slug):
        service = get_object_or_404(
            ConsultancyService.objects.select_related('category'),
            slug=slug
        )
        serializer = ResponseConsultancyServiceSerializer(service)
        return Response(
            {
                "message": "Consultancy service retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
