use campus_couple;
drop table if exists address;
create table address
(
	address_id int primary key auto_increment,
  user_id int not null,
  region_id int not null,
	phone char(12) not null,
  consignee varchar(20) not null,
  further_detail varchar(20)
)engine=InnoDB default charset=utf8;