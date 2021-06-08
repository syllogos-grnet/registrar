from django.contrib import admin

from syndromes.models import NotificationLog, Registar

# Register your models here.
# admin.site.register(Registar)


@admin.register(Registar)
class RegistarAdmin(admin.ModelAdmin):
    list_display = (
        'registar_id', 'name', 'dept', 'email', 'subscription_date')
    list_editable = ('dept', )


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'timestamp', 'registar', 'description', )
