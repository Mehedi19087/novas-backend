from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import CreateProjectSerializer, ResponseProjectSerializer
from .services import create_project


class ProjectListCreateAPIView(APIView):
    def get(self, request):
        queryset = Project.objects.prefetch_related('specs').all()

        category = request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(category=category)

        status_param = request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        featured = request.query_params.get('featured')
        if featured is not None:
            queryset = queryset.filter(is_featured=(featured.lower() in ['true', '1']))

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        serializer = ResponseProjectSerializer(queryset, many=True)
        return Response(
            {
                "message": "Projects retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CreateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            project = create_project(serializer.validated_data)
            response_serializer = ResponseProjectSerializer(project)
            return Response(
                {
                    "message": "Project created successfully",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to create project due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProjectDetailAPIView(APIView):
    def get(self, request, slug):
        project = get_object_or_404(
            Project.objects.prefetch_related('specs'),
            slug=slug
        )
        serializer = ResponseProjectSerializer(project)
        return Response(
            {
                "message": "Project retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
