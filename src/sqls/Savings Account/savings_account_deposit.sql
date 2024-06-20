drop procedure if exists savings_account_deposit;
CREATE PROCEDURE savings_account_deposit(
    in account_no INT,
    in amount DECIMAL(20, 2)
)
begin
    declare new_balance DECIMAL(20, 2);
    declare curr_balance DECIMAL(20, 2);
    begin
        GET DIAGNOSTICS CONDITION 1
            @p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
        SELECT @p1 AS RETURNED_SQLSTATE, @p2 AS MESSAGE_TEXT;
        rollback;
    end;
    start transaction;
    -- 开启事务

    -- 计算该账户当前余额
    select a_balance
    into curr_balance
    from account
    where a_no = account_no;

    -- 计算新的余额
    set new_balance = curr_balance + amount;

    -- 更新账户余额
    update account
    set a_balance = new_balance
    where a_no = account_no;

    -- 插入交易记录
    insert into savings_account_record(sar_a_no, sar_other_a_no, sar_after_balance, sar_amount, sar_time, sar_type)
        value (account_no, account_no, new_balance, amount, now(), 'deposit');

    -- 提交事务
    commit;
end;

-- 将 6 账户存入 1000 元
call savings_account_deposit(5, 1000);
call savings_account_deposit(6, 100);