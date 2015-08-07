use campus_couple;
drop table if exists ordered_food;
create table ordered_food
(
  order_id int not null,
  food_id int not null,
  number int not null
)engine=InnoDB default charset=utf8;