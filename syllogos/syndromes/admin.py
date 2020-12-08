from django.contrib import admin

from syndromes.models import Registar

# Register your models here.
# admin.site.register(Registar)


@admin.register(Registar)
class RegistarAdmin(admin.ModelAdmin):
    list_display = (
        'registar_id', 'name', 'dept', 'email', 'subscription_date')
    list_editable = ('dept', )
