drop procedure if exists loan_account_add;
create procedure loan_account_add(
    IN c_id varchar(18),
    IN b_name varchar(50),
    IN rate decimal(5, 4),
    IN currency varchar(3),
    IN withdraw_limit decimal(20, 2),
    IN loan_limit decimal(20, 2),
    IN a_password varchar(128)
)
begin
    declare new_a_no INT;
    begin
		GET DIAGNOSTICS CONDITION 1
		@p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
		SELECT @p1 AS RETURNED_SQLSTATE , @p2 AS MESSAGE_TEXT;
		rollback ;
	end;
    start transaction; -- 开启事务

    -- 检查是否存在账户，不存在则从1开始，存在则找当前最大值+1
    select coalesce(max(a_no) + 1, 1)
    into new_a_no
    from account;

    -- 打印新的账户号
    select new_a_no as new_a_no;

    -- 在 account 表中插入新的账户
    insert into account(a_no, a_type, a_currency, a_balance, a_open_time, a_open_b_name, a_password_hash, a_total)
    value (new_a_no, 'Loan', currency, 0, now(), b_name, a_password, 0);


    -- 插入 loan_account 的特殊信息
    insert into loan_account(la_no, la_rate, la_withdraw_limit, la_loan_limit)
    value (new_a_no, rate, withdraw_limit, loan_limit);

    -- 插入 account_hold_manage 表
    insert into account_hold_manage(ahm_a_no, ahm_c_id)
    value (new_a_no, c_id);

    commit; -- 提交事务
end;

