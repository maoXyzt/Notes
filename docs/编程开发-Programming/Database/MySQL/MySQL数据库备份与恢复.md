# MySQL数据库备份与恢复

## 连接数据库

```bash
# 连接到127:0.0.1:3306
mysql -uroot -p
# 指定host和port
mysql -h192.168.16.236 -P3309 -uroot -p
```

## 数据备份

1、导出数据和表结构——将特定数据库特定表中的数据和表格结构和数据全部返回

```bash
mysqldump --u  b_user -h 101.3.20.33 -p'H_password'  -P3306 database_di up_subjects > 0101_0630_up_subjects.sql
```

2、导出表结构却不导出表数据——只返回特定数据库特定表格的表格结构，不返回数据,添加“-d”命令参数

```bash
mysqldump --u  b_user -h 101.3.20.33 -p'H_password'  -P3306 -d database_di up_subjects > 0101_0630_up_subjects.sql
```

3、导出表结构和满足挑顶条件的表数据——只返回特定数据库中特定表的表格结构和满足特定条件的数据

```bash
mysqldump --u  b_user -h 101.3.20.33 -p'H_password'  -P3306 database_di up_subjects --where=" ctime>'2017-01-01' and ctime<'2017-06-30'" > 0101_0630_up_subjects.sql
```

4、导出数据却不导出表结构——只返回特定数据库中特定表格的数据，不返回表格结构，添加“-t”命令参数

```bash
mysqldump --u  b_user -h 101.3.20.33 -p'H_password' -t -P3306 database_di up_subjects  >0101_0630_up_subjects.sql
```

5、导出特定数据库的所有表格的表结构及其数据，添加“--databases ”命令参数

```bash
mysqldump  --u  b_user -h 101.3.20.33 -p'H_password' -P3306 --databases test  > all_database.sql
```

## 恢复导入数据库数据

1、系统命令行

格式：mysql -h链接ip -P(大写)端口 -u用户名 -p密码 数据库名 < XX.sql

```bash
mysql -uusername -ppassword db1 < tb1tb2.sql
```

2、或mysql命令行

```sql
mysql>

user db1;

source tb1_tb2.sql;
```

3、恢复整个数据库的方法：

```bash
mysql -u  b_user -h 101.3.20.33 -p'H_password' -P3306   < all_database.sql
```
