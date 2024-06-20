from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth.hashers import make_password, check_password
from ..models import Account, CreditAccount, CreditAccountRecord
from django.http import JsonResponse


@login_required
def credit_account_add(request):
    c_id = request.user.username
    if request.method == 'GET':
        return redirect('credit')
    elif request.method == 'POST':
        open_b_name = request.POST.get('open_b_name')
        rate = request.POST.get('rate')
        currency = request.POST.get('currency')
        overdraft_limit = request.POST.get('overdraft_limit')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if len(password) != 6:
            messages.error(request, '密码长度必须为6位')
            return redirect('credit')

        if password != confirm_password:
            messages.error(request, '两次密码不一致')
            return redirect('credit')

        password = make_password(password)

        rate = Decimal(rate) / 100
        overdraft_limit = Decimal(overdraft_limit)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('credit_account_add', [c_id, open_b_name, rate, currency, overdraft_limit, password])
            messages.success(request, '创建账户成功')
        except:
            messages.error(request, '创建账户失败')

        return redirect('credit')


@login_required
def credit_account_deposit(request):
    pass


@login_required
def credit_account_withdraw(request):
    pass


@login_required
def credit_account_transfer(request):
    pass


@login_required
def credit_account_details(request):
    pass
