# 银行管理系统需求分析

## 命名规范

> 考虑到 MySQL 大小写不敏感，并且 Datagrip 会自动将表名转为小写，因此以下命名规范均为全小写

1. 数据库表中的表名均为全小写，如 `bank` 代表银行，多个单词之间使用下划线 `_` 分隔
2. 数据库属性名为表名各个单词首字母 + 下划线 + 属性名，如 `b_name` 代表银行名称

## 数据需求

1. 银行信息
   - 主属性：银行名称 `VARCHAR(50)`
   - 其他属性：
     - 银行地址 `VARCHAR(200)`：考虑到银行地址可能很长
     - 银行电话 `VARCHAR(20)`：考虑海外电话
2. 客户信息
   - 主属性：身份证号，全部为 18 位字符串 `VARCHAR(18)`
   - 其他属性：
     - 姓名 `VARCHAR(50)`：考虑到外国人名可能很长
     - 性别 `VARCHAR(1)`：M 代表男性，F 代表女性，U 表示未知，这里不考虑无性别者
     - 年龄 `INT`
     - 电话 `VARCHAR(20)`，与银行电话保持一致
     - 地址 `VARCHAR(200)`，与银行地址保持一致
3. 账户信息
   - 主属性：账户号 `VARCHAR(6)`，两个字母加 6 个数字
   - 其他属性：
     - 账户类型 `VARCHAR(20)`：Savings, Credit, Loan, 分别代表储蓄、信用卡、贷款
     - 货币属性 `VARCHAR(3)`：USD, CHY, EUR, JPY, GBP，分别代表美元、人民币、欧元、日元、英镑，目前只考虑这五种货币
     - 账户余额 `DECIMAL(20, 2)`：保留两位小数
     - 开户时间 `DATETIME`：YYYY-MM-DD HH:MM:SS，精确到秒
   - 储蓄账户是账户的子类，继承账户的所有属性，还有：
     - 储蓄账户号 `VARCHAR(8)`：以 SA 开头，后面为 6 位数字（Savings Account）
     - 储蓄利率 `DECIMAL(5, 4)`：保留四位小数
     - 提款额度 `DECIMAL(20, 2)`：保留两位小数，与账户余额保持一致
   - 信用卡账户是账户的子类，继承账户的所有属性，还有：
     - 信用卡账户号 `VARCHAR(8)`：以 CA 开头，后面为 6 位数字（Credit Account）
     - 透支额度 `DECIMAL(20, 2)`：保留两位小数
     - 当前透支金额 `DECIMAL(20, 2)`：保留两位小数
   - 贷款账户是账户的子类，继承账户的所有属性，还有：
     - 贷款账户号 `VARCHAR(8)`：以 LA 开头，后面为 6 位数字（Loan Account）
     - 贷款利率 `DECIMAL(5, 4)`：保留四位小数
     - 贷款额度 `DECIMAL(20, 2)`：保留两位小数
4. 账户操作
   - 储蓄账户操作类型 `VARCHAR(20)`：deposit, withdraw, transfer_in, transfer_out, 表示存款、取款、转入、转出
   - 信用卡账户操作类型 `VARCHAR(20)`：deposit, withdraw, transfer_in, transfer_out, 表示存款、取款、转入、转出
   - 贷款账户操作类型：申请贷款、还款，用两个表保存，不需要设置操作类型
   - 注意：存款、取款的对方账户号直接设置为 NULL，转账的对方账户号必须存在
   - 注意：为了方便起见，认为信用卡账户的透支是一种 **状态，不属于一个具体行为，归类于取款或转出行为**，是否透支由其他字段判断（取款后透支金额大于 0 即可）
5. 贷款信息
   - 主属性：贷款号 `VARCHAR(6)`， 6 位数字（Loan）
   - 其他属性：
     - 贷款金额 `DECIMAL(20, 2)`：保留两位小数
     - 贷款时间 `DATETIME`：YYYY-MM-DD HH:MM:SS，精确到秒
     - 贷款期限 `DATETIME`：YYYY-MM-DD HH:MM:SS，精确到秒
     - 当前还款期数 `INT`
     - 当前总还款金额 `DECIMAL(20, 2)`：保留两位小数
     - 当前状态 `VARCHAR(20)`：ungranted, granted_unrepaid, repaid, canceled, 分别代表未发放、已发放未还款、已还款、已取消
6. 银行部门信息
   - 主属性：部门号 `VARCHAR(4)`：以 D 开头，后面为 3 位数字（Department）
   - 其他属性：
     - 部门名称 `VARCHAR(50)`
     - 部门电话 `VARCHAR(20)`
7. 银行员工信息
   - 主属性：员工号 `VARCHAR(7)`：以 E 开头，后面为 6 位数字（Employee）
   - 其他属性：
     - 员工身份证号 `VARCHAR(18)`：与客户身份证号保持一致
     - 员工姓名 `VARCHAR(50)`：与客户姓名保持一致
     - 员工性别 `VARCHAR(1)`：与客户性别保持一致
     - 员工年龄 `INT`：与客户年龄保持一致
     - 员工电话 `VARCHAR(20)`：与客户电话保持一致
     - 员工地址 `VARCHAR(200)`：与客户地址保持一致
     - 员工部门号 `VARCHAR(4)`：与部门号保持一致
     - 员工头像（只是数据库的一个索引） `VARCHAR(200)`：存储头像的路径

## 数据库实体设计

1. 银行 `bank`, `b`
     是银行系统中的可标识对象，因此是实体，实体设计为：
       $(\underline{银行名称}, 银行地址, 银行电话)$
       $(\underline{b\_name}, b\_addr, b\_phone)$

2. 客户 `customer`, `c`
     是现实世界中的可标识对象，因此是实体，实体设计为：
       $(\underline{身份证号}, 姓名, 性别, 年龄, 电话, 地址)$
       $(\underline{c\_id}, c\_name, c\_gender, c\_age, c\_phone, c\_addr)$

3. 部门 `department`, `d`
     是银行系统中的可标识对象，由银行和部门号唯一标识，因此是实体，实体设计为：
     $(\underline{银行名称}, \underline{部门号}, 部门名称, 部门电话)$
     $(\underline{b\_name}, \underline{d\_no}, d\_name, d\_phone)$

4. 员工 `employee`, `e`
     是银行系统中的可标识对象，由银行和员工号唯一标识，因此是实体，实体设计为：
       $(\underline{银行名称}, \underline{员工号}, 员工身份证号, 员工姓名, 员工性别, 员工年龄, 员工电话, 员工地址, 员工部门号, 员工头像)$
       $(\underline{b\_name}, \underline{e\_no}, e\_id, e\_name, e\_gender, e\_age, e\_phone, e\_addr, e\_dno, e\_avatar)$

5. 账户 `account`, `a`
    是银行系统中的可标识对象，由账户号唯一标识，因此是实体，实体设计为：
    $(\underline{账户号}, 账户类型, 货币属性, 账户余额, 开户时间)$
    $(\underline{a\_no}, a\_type, a\_currency, a\_balance, a\_open\_time)$

6. 储蓄账户 `savings_account`, `sa`
    是账户的子类，实体设计与账户相同，但是需要添加利率、提款额度属性
    利率：$sa\_rate$，提款额度：$sa\_withdraw\_limit$

7. 信用卡账户 `credit_account`, `ca`
    是账户的子类，实体设计与账户相同，但是需要添加透支额度、当前透支金额属性
    透支额度：$ca\_overdraft\_limit$，当前透支金额：$ca\_current\_overdraft\_amount$

8.  贷款账户 `loan_account`, `la`
    是账户的子类，实体设计与账户相同，但是需要添加利率、贷款额度属性
    利率：$la\_rate$，贷款额度：$la\_loan\_limit$

9.  账户持有和管理记录 `account_hold_manage`, `ahm`
    是银行系统中的可标识对象，由账户号唯一标识，因此是实体，实体设计为：
    $(\underline{账户号}, 银行名称, 员工号, 身份证号)$
    $(\underline{a\_no}, b\_name, e\_no, c\_id)$

10. 储蓄账户记录 `savings_account_record`, `sar`
    是银行系统中的可标识对象，由账户号和操作时间唯一标识，因此是实体，实体设计为：
    $(\underline{账户号}, \underline{操作时间}, 对方账户号, 操作后余额, 操作金额, 操作类型)$
    $(\underline{a\_no}, \underline{sar\_time}, sar\_other\_a\_no, sar\_after\_balance, sar\_amount, sar\_type)$

11. 信用卡账户记录 `credit_account_record`, `car`
    是银行系统中的可标识对象，由账户号和操作时间唯一标识，因此是实体，实体设计为：
    $(\underline{账户号}, \underline{操作时间}, 对方账户号, 操作后余额, 操作后透支金额, 操作金额, 操作类型)$
    $(\underline{a\_no}, \underline{car\_time}, car\_other\_a\_no, car\_after\_balance, car\_after\_overdraft\_amount, car\_amount, car\_type)$

12. 贷款账户记录 `loan_account_record`, `lar`
    是银行系统中的可标识对象，由账户号和操作时间唯一标识，因此是实体，实体设计为：
    $(\underline{账户号}, \underline{操作时间}, 对方账户号, 操作后余额, 操作金额, 操作类型)$
    $(\underline{a\_no}, \underline{lar\_time}, lar\_other\_a\_no, lar\_after\_balance, lar\_amount, lar\_type)$

13. 贷款信息 `loan`, `l`
    是银行系统中的可标识对象，由银行发放，由贷款号唯一标识，因此是实体，实体设计为；
    $(\underline{贷款号}, 贷款金额, 贷款时间, 贷款期限, 当前还款期数, 当前总还款金额, 当前状态)$
    $(\underline{l\_no}, l\_amount, l\_time, l\_deadline, l\_current\_amount\_period, l\_current\_amount\_total, l\_status)$

14. 还贷记录 `loan_repay`, `lr`
    是银行系统中的可标识对象，由贷款账户号和还款时间唯一标识，因此是实体，实体设计为：
    $(\underline{贷款号}, \underline{还款时间}, 还款金额)$
    $(\underline{l\_no}, \underline{lr\_time}, lr\_amount)$

15. 贷款发放记录 `loan_grant`, `lg`
    是银行系统中的可标识对象，由贷款号唯一标识，因此是实体，实体设计为：
    $(\underline{贷款号}, 贷款账户号)$
    $(\underline{l\_no}, a\_no)$

## 数据库关系设计


1. 账户持有和管理记录 `account_hold_manage`, `ahm`

   - 认为不同银行发布的账户号是互不相同的，也就是账户号是全局唯一的，所以账户号可以唯一标识一个账户，并且根据 account_hold_manage 表，可以找到发布这个账户的银行和账户持有者。这种设计与实际情况也是相符的

   - 一个人可以有多个账户，但一个账户只能属于一个人
   - 一个员工可以管理多个账户，但一个账户只能由一个员工管理

2. 贷款发放记录 `loan_grant`, `lg`

   - 一个贷款号只能绑定到一个贷款账户号，而一个贷款账户号可以绑定多个贷款号。也就是说一个贷款只能由一个账户还贷，但一个账户可以还多个贷款，比如车贷 + 房贷


## 多模态信息需求

对于员工来说，在创建账户时，需要上传**头像**。

> 头像在数据表中只是一个索引，真正的头像不存储在表项中。


## 设计图

### ER 图
![](../design/银行管理系统%20ER%20图.png)

### 数据表依赖

> 这里的单向箭头就是外键依赖。

![](../design/银行管理系统数据表.png)
