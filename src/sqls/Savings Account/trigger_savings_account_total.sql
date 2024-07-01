drop trigger if exists update_savings_account_total;
CREATE TRIGGER update_savings_account_total
    AFTER INSERT
    ON savings_account_record
    FOR EACH ROW
BEGIN
    -- 更新账户表中的交易总额字段
    UPDATE account
    SET a_total = a_total + NEW.sar_amount
    WHERE a_no = NEW.sar_a_no;
END