from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.chibi.models import Url


class ShortenSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(max_length=100, required=False, write_only=True, validators=[UniqueValidator(queryset=Url.objects.all())])
    short_address = serializers.CharField(read_only=True, source='get_domain_url')

    class Meta:
        model = Url
        fields = ('url', 'slug', 'short_address')
