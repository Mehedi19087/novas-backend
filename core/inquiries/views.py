from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .serializers import (
    CreateRFQSerializer,
    ResponseRFQSerializer,
    CreateContactMessageSerializer,
    ResponseContactMessageSerializer,
    CreateNewsletterSerializer,
    ResponseNewsletterSerializer,
)
from .services import create_rfq, create_contact_message, subscribe_newsletter


class RFQCreateAPIView(APIView):
    def post(self, request):
        serializer = CreateRFQSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            rfq = create_rfq(serializer.validated_data)
            response_serializer = ResponseRFQSerializer(rfq)
            return Response(
                {
                    "message": "RFQ submitted successfully. Our defense procurement team will contact you shortly.",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to submit RFQ due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ContactMessageCreateAPIView(APIView):
    def post(self, request):
        serializer = CreateContactMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            message = create_contact_message(serializer.validated_data)
            response_serializer = ResponseContactMessageSerializer(message)
            return Response(
                {
                    "message": "Your message has been sent successfully. We will be in touch shortly.",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to submit message due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NewsletterSubscribeAPIView(APIView):
    def post(self, request):
        serializer = CreateNewsletterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sub = subscribe_newsletter(serializer.validated_data)
            response_serializer = ResponseNewsletterSerializer(sub)
            return Response(
                {
                    "message": "Subscribed to newsletter successfully.",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {
                    "message": "Failed to subscribe due to an internal server error.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
