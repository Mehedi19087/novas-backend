from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Sector
from .serializers import CreateSectorSerializer, ResponseSectorSerializer
from .services import create_sector


class SectorListCreateAPIView(APIView):
    def get(self, request):
        sectors = Sector.objects.all().order_by('sort_order', 'name')
        serializer = ResponseSectorSerializer(sectors, many=True)
        return Response(
            {
                "message": "Sectors retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CreateSectorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sector = create_sector(serializer.validated_data)
            response_serializer = ResponseSectorSerializer(sector)
            return Response(
                {
                    "message": "Sector created successfully",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to create sector due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SectorDetailAPIView(APIView):
    def get(self, request, slug):
        sector = get_object_or_404(
            Sector.objects.filter(slug=slug) | Sector.objects.filter(sector_id=slug)
        )
        serializer = ResponseSectorSerializer(sector)
        return Response(
            {
                "message": "Sector retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
