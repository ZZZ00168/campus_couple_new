use campus_couple;
drop table if exists messages;
create table messages(
  sender_id int not null,
  receiver_id int not null,
  content varchar(200) not null,
  add_time TIMESTAMP not null
)engine=InnoDB default charset=utf8;