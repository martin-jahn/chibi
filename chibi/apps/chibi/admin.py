from django.contrib import admin

from apps.chibi.models import ApiToken

from .models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    search_fields = ('url', 'slug')
    list_display = ('slug', 'url', 'date_created')
    readonly_fields = ('date_created',)
    date_hierarchy = 'date_created'

    fields = ('url', 'slug', 'date_created')


@admin.register(ApiToken)
class ApiTokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date_created',)
    readonly_fields = ('key', 'date_created')
    raw_id_fields = ('user',)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['user'] = request.user
        return initial
