drop procedure if exists savings_account_transfer;
CREATE PROCEDURE savings_account_transfer(
    in account_no INT,
    in other_account_no INT,
    in amount DECIMAL(20, 2)
)
begin
    declare our_new_balance DECIMAL(20, 2);
    declare our_curr_balance DECIMAL(20, 2);
    declare other_new_balance DECIMAL(20, 2);
    declare other_curr_balance DECIMAL(20, 2);
    declare withdraw_limit DECIMAL(20, 2);
    declare is_other_account_exist INT;
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
    into our_curr_balance
    from account
    where a_no = account_no;

    -- 计算该账户的取款限制
    select sa_withdraw_limit
    into withdraw_limit
    from savings_account
    where sa_no = account_no;

    -- 计算新的余额
    set our_new_balance = our_curr_balance - amount;

    -- 检查余额是否足够
    if our_new_balance < 0 then
        rollback;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '余额不足';
    end if;

    -- 检查取款限制
    if amount > withdraw_limit then
        rollback;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '转账超过限制';
    end if;

    -- 检查对方账户是否存在
    select count(*)
    into is_other_account_exist
    from account
    where a_no = other_account_no;

    if is_other_account_exist = 0 then
        rollback;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '对方账户不存在';
    end if;

    -- 计算对方账户当前余额
    select a_balance
    into other_curr_balance
    from account
    where a_no = other_account_no;

    -- 计算对方账户新的余额
    set other_new_balance = other_curr_balance + amount;

    -- 更新账户余额
    update account
    set a_balance = our_new_balance
    where a_no = account_no;

    -- 更新对方账户余额
    update account
    set a_balance = other_new_balance
    where a_no = other_account_no;

    -- 插入两方交易记录
    insert into savings_account_record(sar_a_no, sar_other_a_no, sar_after_balance, sar_amount, sar_time, sar_type)
        value (account_no, other_account_no, our_new_balance, amount, now(), 'transfer_out');

    insert into savings_account_record(sar_a_no, sar_other_a_no, sar_after_balance, sar_amount, sar_time, sar_type)
        value (other_account_no, account_no, other_new_balance, amount, now(), 'transfer_in');

    -- 提交事务
    commit;
end;