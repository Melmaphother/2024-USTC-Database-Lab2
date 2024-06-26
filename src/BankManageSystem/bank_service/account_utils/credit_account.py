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
    if request.method == 'GET':
        return redirect('credit')
    elif request.method == 'POST':
        a_no = request.POST.get('a_no')
        amount = request.POST.get('amount')
        password = request.POST.get('password')

        # 检查 amount 是否为数字
        try:
            amount = Decimal(amount)
            # 检查 amount 是否大于 0
            if amount <= 0:
                messages.error(request, f'账户号：{a_no}，存款金额必须大于0')
                return redirect('savings')
        except:
            messages.error(request, f'账户号：{a_no}，存款金额必须为数字')
            return redirect('credit')

        # 检查密码是否正确
        account = Account.objects.get(a_no=a_no)
        if not check_password(password, account.a_password_hash):
            messages.error(request, f'账户号：{a_no}，密码错误')
            return redirect('credit')

        try:
            with connection.cursor() as cursor:
                cursor.callproc('credit_account_deposit', [a_no, amount])
            account = Account.objects.get(a_no=a_no)
            messages.success(request, f'账户号：{a_no}，存款成功，当前余额：{account.a_currency} {account.a_balance}')
        except:
            messages.error(request, f'账户号：{a_no}，存款失败')

        return redirect('credit')


@login_required
def credit_account_withdraw(request):
    if request.method == 'GET':
        return redirect('credit')
    elif request.method == 'POST':
        a_no = request.POST.get('a_no')
        amount = request.POST.get('amount')
        password = request.POST.get('password')

        # 检查 amount 是否为数字
        try:
            amount = Decimal(amount)
            # 检查 amount 是否大于 0
            if amount <= 0:
                messages.error(request, f'账户号：{a_no}，存款金额必须大于0')
                return redirect('savings')
        except:
            messages.error(request, f'账户号：{a_no}，存款金额必须为数字')
            return redirect('credit')

        # 检查密码是否正确
        account = Account.objects.get(a_no=a_no)
        if not check_password(password, account.a_password_hash):
            messages.error(request, f'账户号：{a_no}，密码错误')
            return redirect('credit')

        # 获取透支额度
        credit_account = CreditAccount.objects.get(ca_no=a_no)
        overdraft_limit = credit_account.ca_overdraft_limit
        # 获取当前透支金额
        current_overdraft = credit_account.ca_current_overdraft_amount

        # 若取的金额大于余额：计算余额部分之外的剩余支出 A 与剩余额度 B（总额度 - 当前透支金额）
        # 若 A 大于 B 则取钱失败
        if amount > account.a_balance:
            if amount - account.a_balance > overdraft_limit - current_overdraft:
                messages.error(request, f'账户号：{a_no}，取款失败，透支额度不足')
                return redirect('credit')

        try:
            with connection.cursor() as cursor:
                cursor.callproc('credit_account_withdraw', [a_no, amount])
            account = Account.objects.get(a_no=a_no)
            messages.success(request, f'账户号：{a_no}，取款成功，当前余额：{account.a_currency} {account.a_balance}')
        except:
            messages.error(request, f'账户号：{a_no}，取款失败')

        return redirect('credit')


@login_required
def credit_account_transfer(request):
    if request.method == 'GET':
        return redirect('credit')
    elif request.method == 'POST':
        a_no = request.POST.get('a_no')
        amount = request.POST.get('amount')
        password = request.POST.get('password')
        target_a_no = request.POST.get('target')

        # 检查 target_a_no 是否与 a_no 相同
        if a_no == target_a_no:
            messages.error(request, f'账户号：{a_no}，无法为自己转账')
            return redirect('credit')

        # 检查 amount 是否为数字
        try:
            amount = Decimal(amount)
            # 检查 amount 是否大于 0
            if amount <= 0:
                messages.error(request, f'账户号：{a_no}，存款金额必须大于0')
                return redirect('credit')
        except:
            messages.error(request, f'账户号：{a_no}，转账金额必须为数字')
            return redirect('credit')

        # 检查密码是否正确
        account = Account.objects.get(a_no=a_no)
        if not check_password(password, account.a_password_hash):
            messages.error(request, f'账户号：{a_no}，密码错误')
            return redirect('credit')

        # 获取透支额度
        credit_account = CreditAccount.objects.get(ca_no=a_no)
        overdraft_limit = credit_account.ca_overdraft_limit
        # 获取当前透支金额
        current_overdraft = credit_account.ca_current_overdraft_amount

        # 若取的金额大于余额：计算余额部分之外的剩余支出 A 与剩余额度 B（总额度 - 当前透支金额）
        # 若 A 大于 B 则取钱失败
        if amount > account.a_balance:
            if amount - account.a_balance > overdraft_limit - current_overdraft:
                messages.error(request, f'账户号：{a_no}，转账失败，透支额度不足')
                return redirect('credit')

        try:
            with connection.cursor() as cursor:
                cursor.callproc('credit_account_transfer', [a_no, target_a_no, amount])
            account = Account.objects.get(a_no=a_no)
            messages.success(request, f'账户号：{a_no}，转账成功，当前余额：{account.a_currency} {account.a_balance}')
        except:
            messages.error(request, f'账户号：{a_no}，转账失败')

        return redirect('credit')


@login_required
def credit_account_details(request):
    account_number = request.GET.get('account_number')

    if account_number:
        details = CreditAccountRecord.objects.filter(
            car_a_no=account_number
        ).order_by('-car_time').values(
            'car_a_no', 'car_time', 'car_other_a_no', 'car_after_balance',
            'car_after_overdraft_amount', 'car_amount', 'car_type'
        )

        account_info = Account.objects.filter(
            a_no=account_number
        ).values('a_currency').first()

        if account_info:
            currency = account_info['a_currency']
        else:
            currency = 'CNY'

        # 转化交易记录数据
        formatted_details = []
        for detail in details:
            formatted_balance = f"{currency} {detail['car_after_balance']}"
            formatted_overdraft_amount = f"{currency} {detail['car_after_overdraft_amount']}"
            formatted_amount = f"{currency} {detail['car_amount']}"

            # 时间格式化
            formatted_time = detail['car_time'].strftime('%Y-%m-%d %H:%M:%S')

            # 类型转化为中文
            type_mapping = {
                'deposit': '存款',
                'withdraw': '取款',
                'transfer_in': '转入',
                'transfer_out': '转出'
            }
            formatted_type = type_mapping.get(detail['car_type'], detail['car_type'])

            # 如果 other_a_no 是自己，说明为存款取款，那么把对方账户号设为空
            formatted_other_a_no = detail['car_other_a_no']
            if detail['car_type'] in ['deposit', 'withdraw']:
                formatted_other_a_no = ''

            formatted_details.append({
                'd_time': formatted_time,
                'd_type': formatted_type,
                'd_other_a_no': formatted_other_a_no,
                'd_amount': formatted_amount,
                'd_balance': formatted_balance,
                'd_overdraft_amount': formatted_overdraft_amount
            })

        return JsonResponse({"details": formatted_details}, safe=False)
    else:
        return JsonResponse({"error": "No account number provided"}, status=400)
