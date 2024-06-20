from django.db import models


class Bank(models.Model):
    b_name = models.CharField(max_length=50, primary_key=True)
    b_addr = models.CharField(max_length=200, blank=True, default='')
    b_phone = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        db_table = 'bank'


class Department(models.Model):
    d_no = models.IntegerField(primary_key=True)
    d_b_name = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='departments',
                                 db_column='d_b_name')
    d_name = models.CharField(max_length=50, blank=True, default='')
    d_phone = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        db_table = 'department'


class Employee(models.Model):
    e_no = models.IntegerField(primary_key=True)
    e_b_name = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='employees',
                                 db_column='e_b_name')
    e_d_no = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees',
                               db_column='e_d_no')
    e_id = models.CharField(max_length=18, blank=True, default='')
    e_name = models.CharField(max_length=50, blank=True, default='')
    e_age = models.IntegerField(null=True)
    e_phone = models.CharField(max_length=20, blank=True, default='')
    e_addr = models.CharField(max_length=200, blank=True, default='')
    e_avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        db_table = 'employee'


class Customer(models.Model):
    c_id = models.CharField(max_length=18, primary_key=True)
    c_name = models.CharField(max_length=50, blank=True, default='')
    c_gender = models.CharField(max_length=1, blank=True, default='')
    c_age = models.IntegerField(null=True)
    c_phone = models.CharField(max_length=20, blank=True, default='')
    c_addr = models.CharField(max_length=200, blank=True, default='')
    c_avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        db_table = 'customer'


class Account(models.Model):
    a_no = models.IntegerField(primary_key=True)
    a_type = models.CharField(max_length=20, blank=True, default='')
    a_currency = models.CharField(max_length=3, blank=True, default='')
    a_balance = models.DecimalField(max_digits=20, decimal_places=2)
    a_open_time = models.DateTimeField()
    a_open_b_name = models.ForeignKey(Bank, on_delete=models.CASCADE,
                                      related_name='accounts', db_column='a_open_b_name',
                                      default='')
    a_password_hash = models.CharField(max_length=128, blank=True, default='')
    a_total = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'account'


class SavingsAccount(models.Model):
    sa_no = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True,
                                 related_name='savings_account', db_column='sa_no')
    sa_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.0)
    sa_withdraw_limit = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = 'savings_account'


class CreditAccount(models.Model):
    ca_no = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True,
                                 related_name='credit_account', db_column='ca_no')
    ca_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.0)
    ca_overdraft_limit = models.DecimalField(max_digits=20, decimal_places=2)
    ca_current_overdraft_amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = 'credit_account'


class LoanAccount(models.Model):
    la_no = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True,
                                 related_name='loan_account', db_column='la_no')
    la_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.0)
    la_loan_limit = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = 'loan_account'


class AccountHoldManage(models.Model):
    ahm_a_no = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True,
                                    related_name='account_hold_manage', db_column='ahm_a_no')
    ahm_e_no = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 related_name='managed_accounts', db_column='ahm_e_no',
                                 null=True)
    ahm_c_id = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 related_name='managed_accounts', db_column='ahm_c_id')

    class Meta:
        db_table = 'account_hold_manage'


class SavingsAccountRecord(models.Model):
    sar_a_no = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE,
                                 related_name='records', db_column='sar_a_no')
    sar_time = models.DateTimeField()
    sar_other_a_no = models.IntegerField(null=True)
    sar_after_balance = models.DecimalField(max_digits=20, decimal_places=2)
    sar_amount = models.DecimalField(max_digits=20, decimal_places=2)
    sar_type = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        db_table = 'savings_account_record'
        unique_together = (('sar_a_no', 'sar_time'),)


class CreditAccountRecord(models.Model):
    car_a_no = models.ForeignKey(CreditAccount, on_delete=models.CASCADE,
                                 related_name='records', db_column='car_a_no')
    car_time = models.DateTimeField()
    car_other_a_no = models.IntegerField(null=True)
    car_after_balance = models.DecimalField(max_digits=20, decimal_places=2)
    car_after_overdraft_amount = models.DecimalField(max_digits=20, decimal_places=2)
    car_amount = models.DecimalField(max_digits=20, decimal_places=2)
    car_type = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        db_table = 'credit_account_record'
        unique_together = (('car_a_no', 'car_time'),)


class LoanAccountRecord(models.Model):
    lar_a_no = models.ForeignKey(LoanAccount, on_delete=models.CASCADE,
                                 related_name='records', db_column='lar_a_no')
    lar_time = models.DateTimeField()
    lar_other_a_no = models.IntegerField(null=True)
    lar_after_balance = models.DecimalField(max_digits=20, decimal_places=2)
    lar_amount = models.DecimalField(max_digits=20, decimal_places=2)
    lar_type = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        db_table = 'loan_account_record'
        unique_together = (('lar_a_no', 'lar_time'),)


class Loan(models.Model):
    l_no = models.IntegerField(primary_key=True)
    l_amount = models.DecimalField(max_digits=20, decimal_places=2)
    l_time = models.DateTimeField(blank=True, null=True)
    l_deadline = models.DateTimeField(blank=True, null=True)
    l_current_amount_period = models.IntegerField(null=True)
    l_current_amount_total = models.DecimalField(max_digits=20, decimal_places=2)
    l_status = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        db_table = 'loan'


class LoanGrant(models.Model):
    lg_l_no = models.OneToOneField(Loan, on_delete=models.CASCADE, primary_key=True,
                                   related_name='loan_grants', db_column='lg_l_no')
    lg_a_no = models.ForeignKey(LoanAccount, on_delete=models.CASCADE,
                                related_name='grants', db_column='lg_a_no')

    class Meta:
        db_table = 'loan_grant'


class LoanRepay(models.Model):
    lr_l_no = models.ForeignKey(Loan, on_delete=models.CASCADE,
                                related_name='repays', db_column='lr_l_no')
    lr_time = models.DateTimeField()
    lr_amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = 'loan_repay'
        unique_together = (('lr_l_no', 'lr_time'),)
