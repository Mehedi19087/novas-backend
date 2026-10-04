import logging
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from .models import RFQInquiry, ContactMessage, NewsletterSubscription
from .serializers import (ResponseRFQSerializer, ResponseContactMessageSerializer, ResponseNewsletterSerializer,
                          UpdateRFQStatusSerializer, UpdateContactReadSerializer, UpdateSubscriptionSerializer)
from .services import update_inquiry_state, delete_inquiry

logger = logging.getLogger(__name__)
CONFIG = {
    'rfq': (RFQInquiry, ResponseRFQSerializer, UpdateRFQStatusSerializer, 'status', ['reference_id', 'organization_name', 'contact_name', 'email', 'phone', 'tender_ref_number']),
    'contact': (ContactMessage, ResponseContactMessageSerializer, UpdateContactReadSerializer, 'is_read', ['full_name', 'email', 'company', 'subject', 'message']),
    'newsletter': (NewsletterSubscription, ResponseNewsletterSerializer, UpdateSubscriptionSerializer, 'is_active', ['email']),
}


def get_config(kind):
    if kind not in CONFIG:
        raise NotFound('Unknown inquiry type.')
    return CONFIG[kind]


class InquiryAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, kind):
        model, response_serializer, _, state_field, search_fields = get_config(kind)
        queryset = model.objects.all()
        if kind == 'rfq':
            queryset = queryset.prefetch_related('items')
        search = request.query_params.get('search', '').strip()
        if search:
            query = Q()
            for field in search_fields:
                query |= Q(**{f'{field}__icontains': search})
            if kind == 'contact' and search.upper().startswith('INQ-') and search[4:].isdigit():
                query |= Q(pk=int(search[4:]))
            queryset = queryset.filter(query)
        state = request.query_params.get('status', '')
        if state:
            if kind == 'rfq':
                if state not in dict(RFQInquiry.STATUS_CHOICES):
                    raise ValidationError({'status': 'Invalid RFQ status.'})
            else:
                if state not in ('true', 'false'):
                    raise ValidationError({'status': 'Use true or false.'})
                state = state == 'true'
            queryset = queryset.filter(**{state_field: state})
        date_field = 'subscribed_at' if kind == 'newsletter' else 'created_at'
        page = Paginator(queryset.order_by(f'-{date_field}', '-id'), 25).get_page(request.query_params.get('page', 1))
        return Response({'data': {'results': response_serializer(page.object_list, many=True).data, 'count': page.paginator.count, 'page': page.number, 'pages': page.paginator.num_pages}})


class InquiryAdminDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, kind, pk):
        model, response_serializer, *_ = get_config(kind)
        return Response({'data': response_serializer(get_object_or_404(model, pk=pk)).data})

    def patch(self, request, kind, pk):
        model, response_serializer, update_serializer, state_field, _ = get_config(kind)
        instance = get_object_or_404(model, pk=pk)
        if set(request.data) != {state_field}:
            raise ValidationError({'detail': f'Only {state_field} can be updated.'})
        serializer = update_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            instance = update_inquiry_state(instance, serializer.validated_data)
            return Response({'data': response_serializer(instance).data, 'message': 'Submission updated.'})
        except ValidationError:
            raise
        except Exception:
            logger.exception('Inquiry update failed')
            return Response({'message': 'Could not update this submission.'}, status=500)

    def delete(self, request, kind, pk):
        model, *_ = get_config(kind)
        instance = get_object_or_404(model, pk=pk)
        try:
            delete_inquiry(instance)
            return Response(status=204)
        except ValidationError:
            raise
        except Exception:
            logger.exception('Inquiry deletion failed')
            return Response({'message': 'Could not delete this submission.'}, status=500)
