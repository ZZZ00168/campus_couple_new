use campus_couple;
drop table if exists post;
create table post(
	post_id tinyint primary key auto_increment,
	add_time TIMESTAMP DEFAULT now() ,
	user_id tinyint not null,
	content varchar(140)
)engine=InnoDB default charset=utf8;

drop table if exists post_img;
create table post_img(
	post_id int ,
	img_url varchar(100)
)engine=InnoDB default charset=utf8;

drop table if exists favor;
create table favor(
	post_id int ,
	user_id int
)engine=InnoDB default charset=utf8;

drop table if exists comments;
create table comments(
	post_id int not null,
	user_id int not NULL ,#评论者的id
	comment_id int PRIMARY KEY AUTO_INCREMENT,
	commented_id int, #被评论的评论者id
	content varchar(60) ,
	add_time TIMESTAMP
)engine=InnoDB default charset=utf8;

drop table if exists follow;
create table follow(
	user_id int not null,
	followed_id int not null
)engine=InnoDB default charset=utf8;

