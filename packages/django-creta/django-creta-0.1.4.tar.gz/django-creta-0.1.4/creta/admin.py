# vim: set fileencoding=utf-8 :
from django.contrib import admin, messages

# App
from creta import models


# Main Section
class BaseModelAdmin(admin.ModelAdmin):
    actions = []


class NFTAdmin(BaseModelAdmin):
    list_filter = ()


class NFTHistoryAdmin(BaseModelAdmin):
    list_filter = ()


class ApiHistoryAdmin(BaseModelAdmin):
    list_filter = ()


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.NFT, NFTAdmin)
_register(models.NFTHistory, NFTHistoryAdmin)
_register(models.ApiHistory, ApiHistoryAdmin)
