DROP TABLE IF EXISTS bank;
CREATE TABLE bank(
    `b_name` VARCHAR(50) NOT NULL  COMMENT '银行名称' ,
    `b_addr` VARCHAR(200)   COMMENT '银行地址' ,
    `b_phone` VARCHAR(20)   COMMENT '银行电话' ,
    PRIMARY KEY (b_name)
)  COMMENT = '银行';

DROP TABLE IF EXISTS department;
CREATE TABLE department(
    `b_name` VARCHAR(50) NOT NULL  COMMENT '银行名称' ,
    `d_no` VARCHAR(4) NOT NULL  COMMENT '部门号' ,
    `d_name` VARCHAR(50)   COMMENT '部门名称' ,
    `d_phone` VARCHAR(20)   COMMENT '部门电话' ,
    PRIMARY KEY (b_name,d_no)
)  COMMENT = '部门';

DROP TABLE IF EXISTS employee;
CREATE TABLE employee(
    `b_name` VARCHAR(50) NOT NULL  COMMENT '银行名称' ,
    `e_no` VARCHAR(9) NOT NULL  COMMENT '员工号' ,
    `e_id` VARCHAR(18)   COMMENT '员工身份证号' ,
    `e_name` VARCHAR(50)   COMMENT '员工姓名' ,
    `e_age` INT(3)   COMMENT '员工年龄' ,
    `e_phone` VARCHAR(20)   COMMENT '员工电话' ,
    `e_addr` VARCHAR(200)   COMMENT '员工地址' ,
    `d_no` VARCHAR(4)   COMMENT '员工部门号' ,
    `e_avatar` VARCHAR(200)   COMMENT '员工头像' ,
    PRIMARY KEY (b_name,e_no)
)  COMMENT = '员工';

DROP TABLE IF EXISTS customer;
CREATE TABLE customer(
    `c_id` VARCHAR(18) NOT NULL  COMMENT '身份证号' ,
    `c_name` VARCHAR(50)   COMMENT '客户姓名' ,
    `c_gender` VARCHAR(1)   COMMENT '客户性别' ,
    `c_age` INT(3)   COMMENT '客户年龄' ,
    `c_phone` VARCHAR(20)   COMMENT '客户电话' ,
    `c_addr` VARCHAR(200)   COMMENT '客户地址' ,
    `c_avatar` VARCHAR(200)   COMMENT '客户头像' ,
    PRIMARY KEY (c_id)
)  COMMENT = '客户';

DROP TABLE IF EXISTS account;
CREATE TABLE account(
    `a_no` INT AUTO_INCREMENT COMMENT '账户号' ,
    `a_type` VARCHAR(20)   COMMENT '账号类型;Savings, Credit, Loan' ,
    `a_currency` VARCHAR(3)   COMMENT '账号货币属性;USD, CHY, EUR, JPY, GBP' ,
    `a_balance` DECIMAL(20,2)   COMMENT '账户余额' ,
    `a_open_time` DATETIME   COMMENT '账户开户时间' ,
    PRIMARY KEY (a_no)
)  COMMENT = '账户';

DROP TABLE IF EXISTS savings_account;
CREATE TABLE savings_account(
    `a_no` INT AUTO_INCREMENT COMMENT '账户号' ,
    `sa_rate` DECIMAL(5,4)   COMMENT '储蓄利率' ,
    `sa_withdraw_limit` DECIMAL(20,2)   COMMENT '储蓄提款额度' ,
    PRIMARY KEY (a_no)
)  COMMENT = '储蓄账户';

DROP TABLE IF EXISTS credit_account;
CREATE TABLE credit_account(
    `a_no` INT AUTO_INCREMENT COMMENT '账户号' ,
    `ca_overdraft_limit` DECIMAL(20,2)   COMMENT '信用卡透支额度' ,
    `ca_current_overdraft_amount` DECIMAL(20,2)   COMMENT '当前透支金额' ,
    PRIMARY KEY (a_no)
)  COMMENT = '信用卡账户';

DROP TABLE IF EXISTS loan_account;
CREATE TABLE loan_account(
    `a_no` INT AUTO_INCREMENT COMMENT '账户号' ,
    `a_type` VARCHAR(20)   COMMENT '账号类型;Savings, Credit, Loan' ,
    `la_rate` DECIMAL(5,4)   COMMENT '贷款利率' ,
    `la_loan_limit` DECIMAL(20,2)   COMMENT '贷款额度' ,
    PRIMARY KEY (a_no)
)  COMMENT = '贷款账户';

DROP TABLE IF EXISTS account_hold_manage;
CREATE TABLE account_hold_manage(
    `a_no` VARCHAR(18) NOT NULL  COMMENT '账户号' ,
    `b_name` VARCHAR(50)   COMMENT '银行名称' ,
    `e_no` VARCHAR(9)   COMMENT '员工号' ,
    `c_id` VARCHAR(18)   COMMENT '身份证号' ,
    PRIMARY KEY (a_no)
)  COMMENT = '账户持有和管理记录';

DROP TABLE IF EXISTS savings_account_record;
CREATE TABLE savings_account_record(
    `a_no` VARCHAR(18) NOT NULL  COMMENT '账户号' ,
    `sar_time` DATETIME NOT NULL  COMMENT '操作时间' ,
    `sar_other_a_no` VARCHAR(18)   COMMENT '对方账户号' ,
    `sar_after_balance` DECIMAL(20,2)   COMMENT '操作后余额' ,
    `sar_amount` DECIMAL(20,2)   COMMENT '操作金额' ,
    `sar_type` VARCHAR(20)   COMMENT '操作类型;deposit, withdraw, transfer_in, transfer_out' ,
    PRIMARY KEY (a_no,sar_time)
)  COMMENT = '储蓄账户记录';

DROP TABLE IF EXISTS credit_account_record;
CREATE TABLE credit_account_record(
    `a_no` VARCHAR(18) NOT NULL  COMMENT '账户号' ,
    `car_time` DATETIME NOT NULL  COMMENT '操作时间' ,
    `car_other_a_no` VARCHAR(18)   COMMENT '对方账户号' ,
    `car_after_balance` DECIMAL(20,2)   COMMENT '操作后余额' ,
    `car_after_overdraft_amount` DECIMAL(20,2)   COMMENT '操作后透支金额' ,
    `car_amount` DECIMAL(20,2)   COMMENT '操作金额' ,
    `car_type` VARCHAR(20)   COMMENT '操作类型;deposit, withdraw, transfer_in, transfer_out' ,
    PRIMARY KEY (a_no,car_time)
)  COMMENT = '信用卡账户记录';

DROP TABLE IF EXISTS loan_account_record;
CREATE TABLE loan_account_record(
    `a_no` VARCHAR(18) NOT NULL  COMMENT '账户号' ,
    `lar_time` DATETIME NOT NULL  COMMENT '操作时间' ,
    `lar_other_a_no` VARCHAR(18)   COMMENT '对方账户号' ,
    `lar_after_balance` DECIMAL(20,2)   COMMENT '操作后余额' ,
    `lar_amount` DECIMAL(20,2)   COMMENT '操作金额' ,
    `lar_type` VARCHAR(20)   COMMENT '操作类型;deposit, withdraw, transfer_in, transfer_out' ,
    PRIMARY KEY (a_no,lar_time)
)  COMMENT = '贷款账户记录';

DROP TABLE IF EXISTS loan_grant;
CREATE TABLE loan_grant(
    `l_no` VARCHAR(11) NOT NULL  COMMENT '贷款号' ,
    `a_no` VARCHAR(18)   COMMENT '贷款账户号' ,
    PRIMARY KEY (l_no)
)  COMMENT = '贷款发放记录';

DROP TABLE IF EXISTS loan_repay;
CREATE TABLE loan_repay(
    `l_no` VARCHAR(11) NOT NULL  COMMENT '贷款号' ,
    `lr_time` DATETIME NOT NULL  COMMENT '还款时间' ,
    `lr_amount` DECIMAL(20,2)   COMMENT '还款金额' ,
    PRIMARY KEY (l_no,lr_time)
)  COMMENT = '还贷记录';

DROP TABLE IF EXISTS loan;
CREATE TABLE loan(
    `l_no` VARCHAR(11) NOT NULL  COMMENT '贷款号' ,
    `l_amount` DECIMAL(20,2)   COMMENT '贷款金额' ,
    `l_time` DATETIME   COMMENT '贷款时间' ,
    `l_deadline` DATETIME   COMMENT '贷款期限' ,
    `l_current_amount_period` INT   COMMENT '当前还款期数' ,
    `l_current_amount_total` DECIMAL(20,2)   COMMENT '当前总还款金额' ,
    `l_status` VARCHAR(20)   COMMENT '贷款状态;ungranted, granted_unrepaid, repaid, canceled' ,
    PRIMARY KEY (l_no)
)  COMMENT = '贷款信息';

