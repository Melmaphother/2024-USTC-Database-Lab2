drop procedure if exists loan_grant;
create procedure loan_grant(
    in account_no int,
    in loan_amount decimal(20, 2),
    in loan_repay_deadline date
)
begin
    declare new_l_no int;
    declare loan_limit decimal(20, 2);
    declare new_balance decimal(20, 2);
    begin
        GET DIAGNOSTICS CONDITION 1
            @p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
        SELECT @p1 AS RETURNED_SQLSTATE, @p2 AS MESSAGE_TEXT;
        rollback;
    end;
    start transaction;
    -- 开启事务

    -- 从 loan_account 表中查询贷款额度，检查是否超过额度
    select la_loan_limit
    into loan_limit
    from loan_account
    where la_no = account_no;

    if loan_amount > loan_limit then
        signal sqlstate '45000'
            set message_text = 'Loan amount exceeds the limit';
    end if;

    -- 检查是否存在贷款号，不存在则从1开始，存在则找当前最大值+1
    select coalesce(max(l_no) + 1, 1)
    into new_l_no
    from loan;

    -- 在 loan 表中插入新的贷款信息
    insert into loan(l_no, l_amount, l_grant_time, l_repay_deadline, l_repay_amount_total,
                     l_status)
        value (new_l_no, loan_amount, now(), loan_repay_deadline, 0.0, 'disbursed');

    -- 在 loan_grant 表中插入新的对应关系
    insert into loan_grant(lg_l_no, lg_la_no)
        value (new_l_no, account_no);

    -- 从 account 表中获取账户余额
    select a_balance
    into new_balance
    from account
    where a_no = account_no;

    -- 将贷款金额加到账户余额上
    set new_balance = new_balance + loan_amount;

    -- 更新账户余额
    update account
    set a_balance = new_balance
    where a_no = account_no;

    -- 写入 loan_account_record 表，类型为："grant_in"
    insert into loan_account_record(lar_a_no, lar_other_a_no, lar_after_balance, lar_amount, lar_time, lar_type)
        value (account_no, account_no, new_balance, loan_amount, now(), 'grant_in');

    -- 提交事务
    commit;
end;

-- 将 28 账户贷款 10000 元
call loan_grant(28, 10000, '2024-07-02');