use campus_couple;

drop table if exists token;
create table token(
  access_token char(32) primary key,
  user_id int not null unique,
  activate_time timestamp
)engine=InnoDB default charset=utf8;

drop table if exists campus_token;
create table campus_token(
  access_token char(32) primary key,
  campus_id int not null unique,
  activate_time timestamp
)engine=InnoDB default charset=utf8;

insert into token(access_token,user_id,activate_time) values(password('18819451351123456'),1,now());
insert into token(access_token,user_id,activate_time) values(password('18819452351123456'),2,now());
insert into token(access_token,user_id,activate_time) values(password('18819451351123456789'),3,now());