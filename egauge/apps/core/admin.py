from django.contrib import admin
from egauge.apps.core.models import OfficeType, Office, Party, Election, Candidate

class OfficeTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(OfficeType, OfficeTypeAdmin)