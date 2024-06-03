from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Customer, AccountHoldManage, Account
from collections import defaultdict


@login_required
def credit(request):
    return render(
        request,
        'dashboard/credit.html'
    )
