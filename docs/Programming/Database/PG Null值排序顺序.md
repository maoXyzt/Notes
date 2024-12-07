# PG Null值排序顺序

null排在有值的行前面还是后面通过语法来指定

```sql
--null值在前
select * from tablename order by id nulls first;
 
 
--null值在后
select * from tablename order by id nulls last;
 
 
--null在前配合desc使用
select * from tablename order by id desc nulls first;
 
 
--null在后配合desc使用
select * from tablename order by id desc nulls last;
 
 
举例:
null值在后,先按照count1降序排列,count1相同再按照count2降序排列
 
order by count1 desc nulls last, count2  desc nulls last;
```

---------------------
作者：sixmillions 
来源：CSDN 
原文：https://blog.csdn.net/weixin_42183854/article/details/83650624 