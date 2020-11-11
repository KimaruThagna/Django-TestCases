from django.contrib import admin
from .models import WalletOwner, DigitalWallet


@admin.register(DigitalWallet)
class DigitalWalletAdmin(admin.ModelAdmin):
    list_display = ('owner', 'iban', 'balance')
    list_display_links = ('owner',)
    list_per_page = 25
    search_fields = ('iban','owner')
    list_filter = ('balance',)


@admin.register(WalletOwner)
class WalletOwnerAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    list_per_page = 25
    list_display_links = ('email',)
    list_display = ('given_name','family_name','email')
    list_filter = ('family_name','given_name','email')


