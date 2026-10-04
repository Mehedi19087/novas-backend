import logging
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from .content_services import delete_content

logger = logging.getLogger(__name__)


class ContentEditorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )


class ContentMutationMixin:
    permission_classes = [ContentEditorPermission]

    def patch(self, request, slug):
        instance = get_object_or_404(self.content_model, slug=slug)
        serializer = self.update_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            instance = self.update_service(instance, serializer.validated_data)
            return Response({'message': 'Entry updated successfully', 'data': self.response_serializer(instance).data})
        except ValidationError:
            raise
        except Exception:
            logger.exception('Content update failed')
            return Response({'message': 'Could not update this entry. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, slug):
        instance = get_object_or_404(self.content_model, slug=slug)
        try:
            delete_content(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError:
            raise
        except Exception:
            logger.exception('Content deletion failed')
            return Response({'message': 'Could not delete this entry. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
