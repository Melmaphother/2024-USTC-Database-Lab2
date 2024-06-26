from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bank_service.models import Customer, AccountHoldManage, Account
from collections import defaultdict

@login_required
def loan(request):
    return render(
        request,
        'dashboard/loan.html'
    )