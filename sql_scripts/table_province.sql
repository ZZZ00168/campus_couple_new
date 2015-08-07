use campus_couple;
drop table if exists province;
create table province(
	province_id tinyint primary key auto_increment,
	province_name varchar(10) not null unique
)engine=InnoDB default charset=utf8;

insert into province(province_name) values("广东");
insert into province(province_name) values("北京");
insert into province(province_name) values("天津");
insert into province(province_name) values("河北");
insert into province(province_name) values("山西");
insert into province(province_name) values("内蒙古");
insert into province(province_name) values("辽宁");
insert into province(province_name) values("吉林");
insert into province(province_name) values("黑龙江");
insert into province(province_name) values("上海");
insert into province(province_name) values("江苏");
insert into province(province_name) values("浙江");
insert into province(province_name) values("安徽");
insert into province(province_name) values("福建");
insert into province(province_name) values("江西");
insert into province(province_name) values("山东");
insert into province(province_name) values("湖北");
insert into province(province_name) values("河南");
insert into province(province_name) values("湖南");
insert into province(province_name) values("广西");
insert into province(province_name) values("海南");
insert into province(province_name) values("重庆");
insert into province(province_name) values("四川");
insert into province(province_name) values("贵州");
insert into province(province_name) values("云南");
insert into province(province_name) values("西藏");
insert into province(province_name) values("陕西");
insert into province(province_name) values("甘肃");
insert into province(province_name) values("青海");
insert into province(province_name) values("宁夏");
insert into province(province_name) values("新疆");
insert into province(province_name) values("香港");
insert into province(province_name) values("澳门");
insert into province(province_name) values("台湾");
