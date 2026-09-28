from django.contrib import admin

from characters.models import CharacterRecord


# Register your models here.

@admin.register(CharacterRecord)
class CharacterRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'character_type', 'health', 'attack_power', 'special', 'is_alive', 'created_at')
    list_filter = ('character_type',)
    search_fields = ('name',)
    readonly_fields = ('created_at',)

    @admin.display(boolean=True, description='Sağdır')
    def is_alive(self, record):
        return bool(record.to_object())     # __bool__
