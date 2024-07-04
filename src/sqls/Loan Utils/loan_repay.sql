drop procedure if exists loan_repay;
create procedure loan_repay(
    in loan_no int,
    in repay_amount decimal(20, 2)
)
begin
    declare after_repay_amount_total DECIMAL(20, 2);
    declare after_balance DECIMAL(20, 2);
    declare overpayment DECIMAL(20, 2);
    declare account_no INT;
    declare loan_amount DECIMAL(20, 2);
    declare new_repay_period INT;
    begin
        GET DIAGNOSTICS CONDITION 1
            @p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
        SELECT @p1 AS RETURNED_SQLSTATE, @p2 AS MESSAGE_TEXT;
        rollback;
    end;
    start transaction;
    -- 开启事务

    -- 从 loan_grant 表中获取账户号
    select lg_la_no
    into account_no
    from loan_grant
    where lg_l_no = loan_no;

    -- 获取账户号对应的账户余额
    select a_balance
    into after_balance
    from account
    where a_no = account_no;

    -- 检查 loan_repay 表中是否存在 loan_no 的记录，不存在 lr_repay_period 从 1 开始，存在则找当前最大值+1
    select coalesce(max(lr_repay_period) + 1, 1)
    into new_repay_period
    from loan_repay
    where lr_l_no = loan_no;

    -- 从 loan 表中获取当前已还总额 l_repay_amount_total
    select l_repay_amount_total
    into after_repay_amount_total
    from loan
    where l_no = loan_no;

    -- 将还款金额加到 l_repay_amount_total 上
    set after_repay_amount_total = after_repay_amount_total + repay_amount;

    -- 若交易后还款总额额大于等于贷款金额，则将还款总额设为贷款金额，并将多余的钱加到账户余额上
    select l_amount
    into loan_amount
    from loan
    where l_no = loan_no;

    if after_repay_amount_total >= loan_amount then
        set overpayment = after_repay_amount_total - loan_amount;
        set repay_amount = repay_amount - overpayment;
        set after_balance = after_balance + overpayment;
        set after_repay_amount_total = loan_amount;

        -- 更新 loan 表的 l_status 为 'settled'，更新 l_repay_amount_total 字段
        update loan
        set l_status             = 'settled',
            l_repay_amount_total = after_repay_amount_total
        where l_no = loan_no;

        -- 更新账户余额
        update account
        set a_balance = after_balance
        where a_no = account_no;

        -- 写入 loan_account_record 表，类型为："repay_in"
        insert into loan_account_record(lar_a_no, lar_other_a_no, lar_after_balance, lar_amount, lar_time, lar_type)
            value (account_no, account_no, after_balance, overpayment, now(), 'repay_in');

        -- 插入 loan_repay 表
        insert into loan_repay(lr_time, lr_amount, lr_l_no, lr_repay_period, lr_after_repay_amount_total,
                               lr_overpayment)
            value (now(), repay_amount, loan_no, new_repay_period, after_repay_amount_total, overpayment);

    else
        -- 更新 loan 表的 l_status 为 'repaying'，更新 l_repay_amount_total 字段
        update loan
        set l_status             = 'repaying',
            l_repay_amount_total = after_repay_amount_total
        where l_no = loan_no;

        -- 插入 loan_repay 表
        insert into loan_repay(lr_time, lr_amount, lr_l_no, lr_repay_period, lr_after_repay_amount_total,
                               lr_overpayment)
            value (now(), repay_amount, loan_no, new_repay_period, after_repay_amount_total, 0);
    end if;
    commit;
end;