use campus_couple;
drop table if exists user;
create table user
(
	user_id int primary key auto_increment,
	mobile char(11) not null unique,
	passwd char(33),
	verified enum('yes', 'no') not null,
  campus_id int,
  sex enum('m', 'f'),
  default_address_id int,
	add_time timestamp not null
)engine=InnoDB default charset=utf8;

drop table if exists userinfo;
create table userinfo
(
	user_id int,
	type enum('img_url', 'birthday', 'nickname', 'description',
		'province_id', 'location', 'profession') not null,
	information varchar(100) not null
)engine=InnoDB default charset=utf8;

drop table if exists user_verify;
create table user_verify
(
  user_id int primary key,
  verify_code int not null,
  fail_count int not null,
  add_time timestamp not null
)engine=InnoDB default charset=utf8;
