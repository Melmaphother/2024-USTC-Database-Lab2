drop procedure if exists loan_account_transfer;
CREATE PROCEDURE loan_account_transfer(
    in account_no INT,
    in other_account_no INT,
    in amount DECIMAL(20, 2)
)
begin
    declare our_new_balance DECIMAL(20, 2);
    declare our_curr_balance DECIMAL(20, 2);
    declare other_new_balance DECIMAL(20, 2);
    declare other_curr_balance DECIMAL(20, 2);
    declare other_account_type VARCHAR(20);
    declare other_curr_overdraft_amount DECIMAL(20, 2);
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
    select la_withdraw_limit
    into withdraw_limit
    from loan_account
    where la_no = account_no;

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

    -- 更新账户余额
    update account
    set a_balance = our_new_balance
    where a_no = account_no;

    -- 插入自己的交易记录
    insert into loan_account_record(lar_a_no, lar_other_a_no, lar_after_balance, lar_amount, lar_time, lar_type)
        value (account_no, other_account_no, our_new_balance, amount, now(), 'transfer_out');

    -- 计算对方账户当前余额和类型
    select a_balance, a_type
    into other_curr_balance, other_account_type
    from account
    where a_no = other_account_no;

    if other_account_type = 'Savings' then
        -- 计算对方账户新余额
        set other_new_balance = other_curr_balance + amount;

        -- 更新对方账户余额
        update account
        set a_balance = other_new_balance
        where a_no = other_account_no;

        -- 插入对方的交易记录
        insert into savings_account_record(sar_a_no, sar_other_a_no, sar_after_balance, sar_amount, sar_time, sar_type)
            value (other_account_no, account_no, other_new_balance, amount, now(), 'transfer_in');

    elseif other_account_type = 'Credit' then
        -- 计算对方账户当前透支
        select ca_current_overdraft_amount
        into other_curr_overdraft_amount
        from credit_account
        where ca_no = other_account_no;

        -- 如果对方当前透支为 0，直接存，更新余额
        if other_curr_overdraft_amount = 0 then
            set other_new_balance = other_curr_balance + amount;
            update account
            set a_balance = other_new_balance
            where a_no = other_account_no;
        else
            -- 如果对方当前透支不为 0，先还清透支，再存
            if amount <= other_curr_overdraft_amount then
                set other_new_balance = other_curr_balance;
                set other_curr_overdraft_amount = other_curr_overdraft_amount - amount;
            else
                set other_new_balance = other_curr_balance + amount - other_curr_overdraft_amount;
                set other_curr_overdraft_amount = 0;
            end if;

            update account
            set a_balance = other_new_balance
            where a_no = other_account_no;

            update credit_account
            set ca_current_overdraft_amount = other_curr_overdraft_amount
            where ca_no = other_account_no;
        end if;

        -- 插入对方的交易记录
        insert into credit_account_record(car_a_no, car_other_a_no, car_after_balance, car_after_overdraft_amount,
                                          car_amount, car_time, car_type)
            value (other_account_no, account_no, other_new_balance, other_curr_overdraft_amount, amount, now(),
                   'transfer_in');

    elseif other_account_type = 'Loan' then
        -- 与储蓄账户行为相同
        set other_new_balance = other_curr_balance + amount;

        update account
        set a_balance = other_new_balance
        where a_no = other_account_no;

        insert into loan_account_record(lar_a_no, lar_other_a_no, lar_after_balance, lar_amount, lar_time,
                                        lar_type)
            value (other_account_no, account_no, other_new_balance, amount, now(), 'transfer_in');

    else
        rollback;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '对方账户类型错误';
    end if;


    -- 提交事务
    commit;
end;