drop procedure if exists loan_account_deposit;
CREATE PROCEDURE loan_account_deposit(
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
    insert into loan_account_record(lar_a_no, lar_other_a_no, lar_after_balance, lar_amount, lar_time, lar_type)
        value (account_no, account_no, new_balance, amount, now(), 'deposit');

    -- 提交事务
    commit;
end;
