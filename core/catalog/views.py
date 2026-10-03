from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Category, Product, Vessel
from .serializers import (
    CreateCategorySerializer,
    ResponseCategorySerializer,
    CreateProductSerializer,
    ResponseProductSerializer,
    CreateVesselSerializer,
    ResponseVesselSerializer,
)
from .services import create_category, create_product, create_vessel


class CategoryListCreateAPIView(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_active=True).order_by('sort_order', 'name')
        serializer = ResponseCategorySerializer(categories, many=True)
        return Response(
            {
                "message": "Categories retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CreateCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category = create_category(serializer.validated_data)
            response_serializer = ResponseCategorySerializer(category)
            return Response(
                {
                    "message": "Category created successfully",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to create category due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CategoryDetailAPIView(APIView):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        serializer = ResponseCategorySerializer(category)
        return Response(
            {
                "message": "Category retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ProductListCreateAPIView(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('category').prefetch_related('specs').all()

        category_slug = request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        sector_id = request.query_params.get('sector')
        if sector_id:
            queryset = queryset.filter(sector_id=sector_id)

        featured = request.query_params.get('featured')
        if featured is not None:
            queryset = queryset.filter(featured=(featured.lower() in ['true', '1']))

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        serializer = ResponseProductSerializer(queryset, many=True)
        return Response(
            {
                "message": "Products retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            product = create_product(serializer.validated_data)
            response_serializer = ResponseProductSerializer(product)
            return Response(
                {
                    "message": "Product created successfully",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to create product due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductDetailAPIView(APIView):
    def get(self, request, slug):
        product = get_object_or_404(
            Product.objects.select_related('category').prefetch_related('specs'),
            slug=slug
        )
        serializer = ResponseProductSerializer(product)
        return Response(
            {
                "message": "Product retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class VesselListCreateAPIView(APIView):
    def get(self, request):
        vessels = Vessel.objects.all().order_by('name')
        serializer = ResponseVesselSerializer(vessels, many=True)
        return Response(
            {
                "message": "Vessels retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CreateVesselSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            vessel = create_vessel(serializer.validated_data)
            response_serializer = ResponseVesselSerializer(vessel)
            return Response(
                {
                    "message": "Vessel created successfully",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to create vessel due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VesselDetailAPIView(APIView):
    def get(self, request, slug):
        vessel = get_object_or_404(Vessel, slug=slug)
        serializer = ResponseVesselSerializer(vessel)
        return Response(
            {
                "message": "Vessel retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
