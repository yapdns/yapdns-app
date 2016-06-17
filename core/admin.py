from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'secret_key')
    list_display = ('id', 'name', 'secret_key')

admin.site.register(Client, ClientAdmin)
