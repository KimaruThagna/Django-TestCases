from django.contrib import admin
from .models import WalletOwner, DigitalWallet
from admin_auto_filters.filters import AutocompleteFilter

class WalletOwnerFilter(AutocompleteFilter):
    title = 'Digital Wallet Owner'
    field_name = 'owner'

@admin.register(DigitalWallet)
class DigitalWalletAdmin(admin.ModelAdmin):
    list_display = ('owner', 'iban', 'balance')
    list_display_links = ('owner',)
    list_per_page = 25
    search_fields = ('iban','owner__email','owner__given_name','owner__family_name')
    list_filter = ('balance',WalletOwnerFilter)
    list_select_related = ('owner',)

    # def queryset(self, request):
    #     return super(DigitalWalletAdmin, self).get_queryset(request).prefetch_related('owner')


@admin.register(WalletOwner)
class WalletOwnerAdmin(admin.ModelAdmin):
    search_fields = ('email','given_name','family_name')
    list_per_page = 25
    list_display_links = ('email',)
    list_display = ('given_name','family_name','email')
    list_filter = ('email',)


