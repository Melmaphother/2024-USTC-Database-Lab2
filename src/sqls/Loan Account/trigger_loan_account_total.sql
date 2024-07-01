drop trigger if exists update_loan_account_total;
create trigger update_loan_account_total
    after insert
    on loan_account_record
    for each row
begin
    -- 更新账户表中的交易总额字段
    update account
    set a_total = a_total + new.lar_amount
    where a_no = new.lar_a_no;
end;