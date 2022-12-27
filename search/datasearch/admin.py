from django.contrib import admin

from datasearch.models import Decision, LegalBody

# Register your models here.


class DecisionAdmin(admin.ModelAdmin):
    list_display = ("file_number", "legal_body")


class LegalBodyAdmin(admin.ModelAdmin):
    list_display = ("legal_name", "legal_code")


admin.site.register(Decision, DecisionAdmin)
admin.site.register(LegalBody, LegalBodyAdmin)
