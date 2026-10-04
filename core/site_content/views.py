from core.content_views import ContentEditorPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import CompanyProfile, CompanyPillar, BlueprintStep, HeroBannerSlide
from .serializers import (
    ResponseCompanyProfileSerializer,
    ResponseCompanyPillarSerializer,
    ResponseBlueprintStepSerializer,
    CreateHeroBannerSlideSerializer,
    ResponseHeroBannerSlideSerializer,
)
from .services import create_hero_banner_slide


class CompanyOverviewAPIView(APIView):
    def get(self, request):
        profile = CompanyProfile.objects.first()
        pillars = CompanyPillar.objects.all().order_by('sort_order', 'id')
        blueprints = BlueprintStep.objects.all().order_by('sort_order', 'step')

        return Response(
            {
                "message": "Company overview retrieved successfully",
                "data": {
                    "profile": ResponseCompanyProfileSerializer(profile).data if profile else None,
                    "pillars": ResponseCompanyPillarSerializer(pillars, many=True).data,
                    "blueprints": ResponseBlueprintStepSerializer(blueprints, many=True).data,
                },
            },
            status=status.HTTP_200_OK,
        )


class HeroBannerSlideListCreateAPIView(APIView):
    permission_classes = [ContentEditorPermission]

    def get(self, request):
        queryset = HeroBannerSlide.objects.filter(is_active=True).order_by('sort_order', 'id')

        page = request.query_params.get('page')
        if page:
            queryset = queryset.filter(page_identifier=page)

        serializer = ResponseHeroBannerSlideSerializer(queryset, many=True)
        return Response(
            {
                "message": "Hero banner slides retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CreateHeroBannerSlideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            slide = create_hero_banner_slide(serializer.validated_data)
            response_serializer = ResponseHeroBannerSlideSerializer(slide)
            return Response(
                {
                    "message": "Hero banner slide created successfully",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to create hero banner slide due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
