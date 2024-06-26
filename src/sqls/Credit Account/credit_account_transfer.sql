drop procedure if exists credit_account_transfer;
CREATE PROCEDURE credit_account_transfer(
    in account_no INT,
    in other_account_no INT,
    in amount DECIMAL(20, 2)
)
begin
    declare our_new_balance DECIMAL(20, 2);
    declare our_curr_balance DECIMAL(20, 2);
    declare our_overdraft_limit DECIMAL(20, 2);
    declare our_curr_overdraft_amount DECIMAL(20, 2);
    declare other_new_balance DECIMAL(20, 2);
    declare other_curr_balance DECIMAL(20, 2);
    declare other_account_type VARCHAR(20);
    declare other_curr_overdraft_amount DECIMAL(20, 2);
    declare is_other_account_exist INT;
    begin
        GET DIAGNOSTICS CONDITION 1
            @p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
        SELECT @p1 AS RETURNED_SQLSTATE, @p2 AS MESSAGE_TEXT;
        rollback;
    end;
    start transaction;
    -- 开启事务

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

    -- 计算该账户当前余额、当前透支、透支额度
    select a_balance, ca_current_overdraft_amount, ca_overdraft_limit
    into our_curr_balance, our_curr_overdraft_amount, our_overdraft_limit
    from account
             join credit_account on a_no = ca_no
    where a_no = account_no;

    -- 若取的钱小于等于余额，直接取
    if amount <= our_curr_balance then
        set our_new_balance = our_curr_balance - amount;
        update account
        set a_balance = our_new_balance
        where a_no = account_no;
    else
        -- 若取的钱大于余额，计算余额部分之外的剩余支出与剩余额度
        -- 若剩余支出小于等于剩余额度，直接取
        if amount - our_curr_balance <= our_overdraft_limit - our_curr_overdraft_amount then
            set our_new_balance = 0;
            set our_curr_overdraft_amount = our_curr_overdraft_amount + amount - our_curr_balance;
        else
            rollback;
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '透支额度不足';
        end if;
        -- 更新账户余额
        update account
        set a_balance = our_new_balance
        where a_no = account_no;

        -- 更新透支额度
        update credit_account
        set ca_current_overdraft_amount = our_curr_overdraft_amount
        where ca_no = account_no;
    end if;

    -- 插入交易记录
    insert into credit_account_record(car_a_no, car_other_a_no, car_after_balance, car_after_overdraft_amount,
                                      car_amount, car_time, car_type)
        value (account_no, account_no, our_new_balance, our_curr_overdraft_amount, amount, now(), 'transfer_out');


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