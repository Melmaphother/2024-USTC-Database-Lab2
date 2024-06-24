drop procedure if exists credit_account_withdraw;
create procedure credit_account_withdraw(
    in account_no INT,
    in amount DECIMAL(20, 2)
)
begin
    declare overdraw_limit DECIMAL(20, 2);
    declare curr_overdraft_amount DECIMAL(20, 2);
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

    -- 计算该账户当前余额、当然透支、透支额度
    select a_balance, ca_current_overdraft_amount, ca_overdraft_limit
    into curr_balance, curr_overdraft_amount, overdraw_limit
    from account
    join credit_account on a_no = ca_no
    where a_no = account_no;


    -- 若取的钱小于等于余额，直接取
    if amount <= curr_balance then
        set new_balance = curr_balance - amount;
        update account
        set a_balance = new_balance
        where a_no = account_no;
    else
        -- 若取的钱大于余额，计算余额部分之外的剩余支出与剩余额度
        -- 若剩余支出小于等于剩余额度，直接取
        if amount - curr_balance <= overdraw_limit - curr_overdraft_amount then
            set new_balance = 0;
            set curr_overdraft_amount = curr_overdraft_amount + amount - curr_balance;
        else
            rollback;
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '透支额度不足';
        end if;
        -- 更新账户余额
        update account
        set a_balance = new_balance
        where a_no = account_no;

        -- 更新透支额度
        update credit_account
        set ca_current_overdraft_amount = curr_overdraft_amount
        where ca_no = account_no;
    end if;

    -- 插入交易记录
    insert into credit_account_record(car_a_no, car_other_a_no, car_after_balance, car_after_overdraft_amount, car_amount, car_time, car_type)
    value (account_no, account_no, new_balance, curr_overdraft_amount, amount, now(), 'withdraw');

    -- 提交事务
    commit;
end;

-- 向 18 号账户取款 1000 元
call credit_account_withdraw(18, 1000);