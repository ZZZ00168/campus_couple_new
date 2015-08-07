use campus_couple;
drop table if exists orders;
create table orders(
  order_id int primary key auto_increment,
  address_id int not null,
  user_id int not null,
  campus_id int not null,
  add_time timestamp not null,
  status enum('submitted', 'confirmed', 'preparing',
              'delivering', 'arrived') not null
)engine=InnoDB default charset=utf8;