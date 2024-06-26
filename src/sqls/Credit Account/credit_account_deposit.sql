drop procedure if exists credit_account_deposit;
create procedure credit_account_deposit(
    in account_no INT,
    in amount DECIMAL(20, 2)
)
begin
    declare curr_overdraft_amount DECIMAL(20, 2);
    declare curr_balance DECIMAL(20, 2);
    declare new_balance DECIMAL(20, 2);
    begin
        GET DIAGNOSTICS CONDITION 1
            @p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
        SELECT @p1 AS RETURNED_SQLSTATE, @p2 AS MESSAGE_TEXT;
        rollback;
    end;
    start transaction;
    -- 开启事务

    -- 计算该账户当前余额和当前透支
    select a_balance, ca_current_overdraft_amount
    into curr_balance, curr_overdraft_amount
    from account
             join credit_account on a_no = ca_no
    where a_no = account_no;

    if curr_overdraft_amount = 0 then
        -- 如果当前透支额度为 0，直接存，更新余额
        set new_balance = curr_balance + amount;
        update account
        set a_balance = new_balance
        where a_no = account_no;
    else
        -- 如果当前透支额度不为 0，先还清透支额度，再存
        if amount <= curr_overdraft_amount then
            set new_balance = curr_balance;
            set curr_overdraft_amount = curr_overdraft_amount - amount;
        else
            set new_balance = curr_balance + amount - curr_overdraft_amount;
            set curr_overdraft_amount = 0;
        end if;

        update account
        set a_balance = new_balance
        where a_no = account_no;

        update credit_account
        set ca_current_overdraft_amount = curr_overdraft_amount
        where ca_no = account_no;
    end if;
    -- 插入交易记录
    insert into credit_account_record(car_a_no, car_other_a_no, car_after_balance, car_after_overdraft_amount,
                                      car_amount, car_time, car_type)
        value (account_no, account_no, new_balance, curr_overdraft_amount, amount, now(), 'deposit');

    -- 提交事务
    commit;
end;