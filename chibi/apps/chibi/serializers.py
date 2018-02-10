from rest_framework import serializers

from apps.chibi.models import Url


class ShortenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('url', 'slug')
