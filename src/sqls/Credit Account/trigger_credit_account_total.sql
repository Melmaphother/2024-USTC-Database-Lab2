drop trigger if exists update_credit_account_total;
create trigger update_credit_account_total
    after insert
    on credit_account_record
    for each row
begin
    -- 更新账户表中的交易总额字段
    update account
    set a_total = a_total + new.car_amount
    where a_no = new.car_a_no;
end;