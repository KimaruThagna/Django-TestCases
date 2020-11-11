from django.contrib import admin
from .models import Transaction
from admin_auto_filters.filters import AutocompleteFilter

class SenderFilter(AutocompleteFilter):
    title = 'Digital Wallet Owner'
    field_name = 'sender'

class RecepientFilter(AutocompleteFilter):
    title = 'Digital Wallet Owner'
    field_name = 'recepient'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ('value', 'created', 'sender', 'recepient')
    list_display_links = ('created',)
    list_display = ('sender', 'recepient', 'value', 'created')
    list_per_page = 50
    search_fields = ('created',SenderFilter,RecepientFilter)
    list_select_related = ('sender', 'recepient')

# def queryset(self, request):
    #     return super(DigitalWalletAdmin, self).get_queryset(request).prefetch_related('owner')
