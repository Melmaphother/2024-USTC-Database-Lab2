drop procedure if exists credit_account_add;
CREATE PROCEDURE credit_account_add(
    in c_id VARCHAR(18),
    in b_name VARCHAR(50),
    in rate DECIMAL(5, 4),
    in currency VARCHAR(3),
    in overdraft_limit DECIMAL(20, 2),
    in a_password VARCHAR(128)
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

    -- 在 account 表中插入新的账户
    insert into account(a_no, a_type, a_currency, a_balance, a_open_time, a_open_b_name, a_password_hash, a_total)
    value (new_a_no, 'Credit', currency, 0, now(), b_name, a_password, 0);

    -- 插入 credit_account 的特殊信息
    insert into credit_account(ca_no, ca_rate, ca_overdraft_limit, ca_current_overdraft_amount)
    value (new_a_no, rate, overdraft_limit, 0);

    -- 插入 account_hold_manage 表
    insert into account_hold_manage(ahm_a_no, ahm_c_id)
    value (new_a_no, c_id);

    commit; -- 提交事务
end