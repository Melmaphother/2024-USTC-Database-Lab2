from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import (
    login,
    customer_register,
    dashboard,
    profile,
    savings,
    credit,
    loan,
    home,
    terms
)
from .account_utils import (
    savings_account,
    credit_account
)

urlpatterns = ([
                   path('', home.home, name='home'),
                   path('login/', login.auth_login, name='login'),
                   path('terms/', terms.terms, name='terms'),
                   path('privacy/', terms.privacy, name='privacy'),
                   path('customer_register/', customer_register.customer_register, name='customer_register'),
                   path('edit_profile/', customer_register.edit_profile, name='edit_profile'),
                   path('dashboard/', dashboard.dashboard, name='dashboard'),
                   path('dashboard/profile/', profile.profile, name='profile'),
                   path('dashboard/savings/', savings.savings, name='savings'),
                   path('dashboard/credit/', credit.credit, name='credit'),
                   path('dashboard/loan/', loan.loan, name='loan'),
                   path('savings_account_add/', savings_account.savings_account_add,
                        name='savings_account_add'),
                   path('savings_account_deposit/', savings_account.savings_account_deposit,
                        name='savings_account_deposit'),
                   path('savings_account_withdraw/', savings_account.savings_account_withdraw,
                        name='savings_account_withdraw'),
                   path('savings_account_transfer/', savings_account.savings_account_transfer,
                        name='savings_account_transfer'),
                   path('savings_account_details/', savings_account.savings_account_details,
                        name='savings_account_details'),
                   path('credit_account_add/', credit_account.credit_account_add,
                        name='credit_account_add'),
                   path('credit_account_deposit/', credit_account.credit_account_deposit,
                        name='credit_account_deposit'),
                   path('credit_account_withdraw/', credit_account.credit_account_withdraw,
                        name='credit_account_withdraw'),
                   path('credit_account_transfer/', credit_account.credit_account_transfer,
                        name='credit_account_transfer'),
                   path('credit_account_details/', credit_account.credit_account_details,
                        name='credit_account_details'),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
               )
