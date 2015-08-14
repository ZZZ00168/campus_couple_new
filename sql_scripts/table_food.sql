use campus_couple;
drop table if exists food;
create table food(
	food_id int primary key auto_increment,
	food_name varchar(20) not null,
	campus_id int not null,
  food_price double not null,
  food_desc varchar(100),
  food_img_url varchar(100) not null,
  is_sold_out enum('yes', 'no') not null,
  is_served enum('yes', 'no') not null
)engine=InnoDB default charset=utf8;

insert into food(food_name, campus_id, food_price,
                 food_img_url, is_sold_out, is_served)
    values('白饭', 1, 1.5, 'http://imgurl/rice', 'no', 'yes');

insert into food(food_name, campus_id, food_price, food_desc,
                 food_img_url, is_sold_out, is_served)
    values('鸡扒饭A', 1, 10, '好好味啊',
           'http://imgurl/chicken_rice', 'yes', 'no');
