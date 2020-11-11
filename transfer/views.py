from django.views.generic.base import TemplateView
from django.views.generic import ListView

from wallets.models import WalletOwner
from .models import Transaction

from django.contrib.auth.mixins import LoginRequiredMixin


class WelcomeView(TemplateView):
    template_name = "transfer/welcome.html"


class TransactionsListView(LoginRequiredMixin, ListView):
    template_name = "transfer/transactions.html"
    paginate_by = 25
    model = Transaction
    ordering = '-created'

    def dispatch(self, request, *args, **kwargs):
        """
        For convenience and ease of use in this scenario,
        we use the first existing account owner.
        A real online banking application would provide the
        authenticated account owner
        """
        request.account_owner = WalletOwner.objects.all().first()
        return super().dispatch(request=request, *args, **kwargs)
