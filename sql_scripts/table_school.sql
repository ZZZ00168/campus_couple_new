use campus_couple;
drop table if exists school;
create table school(
	school_id int primary key auto_increment,
	school_name varchar(30) not null unique
)engine=InnoDB default charset=utf8;

drop table if exists campus;
create table campus(
	campus_id int primary key auto_increment,
	campus_name varchar(20),
	login_name varchar(20) unique not null,
	passwd char(33) not null,
	school_id int not null,
	advance_time tinyint not null
)engine=InnoDB default charset=utf8;

drop table if exists region;
create table region(
	region_id int primary key auto_increment,
  region_name varchar(20) not null,
  campus_id int not null
)engine=InnoDB default charset=utf8;

insert into school(school_name) values("华南理工大学");
insert into school(school_name) values('fake_school');
insert into campus(campus_name, login_name, passwd, school_id)
		values('大学城校区', 'admin',
					 '21232f297a57a5a743894a0e4a801fc3', 1);

insert into campus(campus_name, login_name, passwd, school_id) 
	values('fake_campus', 'fake_campus', '21232f297a57a5a743894a0e4a801fc3', 1);
insert into region(region_name, campus_id) values('C11', 1);
insert into region(region_name, campus_id) values('C12', 1);
