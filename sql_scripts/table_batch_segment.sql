use campus_couple;

drop table if exists batch_segment;
create table batch_segment(
	campus_id int not null,
	begin_hour tinyint not null,
	begin_min tinyint not null,
	begin_second tinyint not null,
	end_hour tinyint not null,
	end_min tinyint not null,
	end_second tinyint not null
)engine=InnoDB default charset=utf8;

