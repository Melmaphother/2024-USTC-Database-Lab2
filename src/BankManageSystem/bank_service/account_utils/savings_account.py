import time
from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth.hashers import make_password, check_password
from ..models import Account


@login_required
def savings_account_add(request):
    c_id = request.user.username
    if request.method == 'GET':
        return redirect('savings')
    elif request.method == 'POST':
        open_b_name = request.POST.get('open_b_name')
        rate = request.POST.get('rate')
        currency = request.POST.get('currency')
        withdraw_limit = request.POST.get('withdraw_limit')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if len(password) != 6:
            messages.error(request, '密码长度必须为6位')
            return redirect('savings')

        if password != confirm_password:
            messages.error(request, '两次密码不一致')
            return redirect('savings')

        password = make_password(password)  # 对密码进行加密

        rate = Decimal(rate) / 100
        withdraw_limit = Decimal(withdraw_limit)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('savings_account_add', [c_id, open_b_name, rate, currency, withdraw_limit, password])
        except:
            messages.error(request, '创建账户失败')

        return redirect('savings')


@login_required
def savings_account_deposit(request):
    if request.method == 'GET':
        return redirect('savings')
    elif request.method == 'POST':
        a_no = request.POST.get('a_no')
        amount = request.POST.get('amount')
        password = request.POST.get('password')

        # 检查 amount 是否为数字
        try:
            amount = Decimal(amount)
        except:
            messages.error(request, '存款金额必须为数字')
            return redirect('savings')

        # 检查密码是否正确
        account = Account.objects.get(a_no=a_no)
        if not check_password(password, account.a_password_hash):
            messages.error(request, '密码错误')
            return redirect('savings')

        try:
            with connection.cursor() as cursor:
                cursor.callproc('savings_account_deposit', [a_no, amount])
        except:
            messages.error(request, '存款失败')

        return redirect('savings')
