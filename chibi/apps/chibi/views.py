from django.db import transaction
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from apps.chibi.auth import AuthorizedAPIView
from apps.chibi.models import Url
from apps.chibi.serializers import ShortenSerializer


def redirect_view(request, slug):
    """
    Redirects any HTTP request to long_url or returns 404
    """
    redirect = get_object_or_404(Url, slug=slug)
    return HttpResponsePermanentRedirect(redirect.url)


class AlarmSegmentView(AuthorizedAPIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = ShortenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
