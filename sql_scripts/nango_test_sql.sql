----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------

--table_user.sql

--插入用户手机验证码 1-5
insert into user_verify(user_id,verify_code,add_time) values(1,10001,now());
insert into user_verify(user_id,verify_code,add_time) values(2,10002,now());
insert into user_verify(user_id,verify_code,add_time) values(3,10003,now());
insert into user_verify(user_id,verify_code,add_time) values(4,10004,now());
insert into user_verify(user_id,verify_code,add_time) values(5,10005,now());

--创建用户1-5
insert into user(user_id,mobile,passwd,verified,campus_id,sex,default_address_id,add_time)
        values(1,'18819410001',password('100001'),'yes',1,'m',1,now());
insert into user(user_id,mobile,passwd,verified,campus_id,sex,default_address_id,add_time)
        values(2,'18819410002',password('100002'),'yes',2,'m',1,now());
insert into user(user_id,mobile,passwd,verified,campus_id,sex,default_address_id,add_time)
        values(3,'18819410003',password('100003'),'yes',1,'f',1,now());
insert into user(user_id,mobile,passwd,verified,campus_id,sex,default_address_id,add_time)
        values(4,'18819410004',password('100004'),'yes',1,'m',2,now());
insert into user(user_id,mobile,passwd,verified,campus_id,sex,default_address_id,add_time)
        values(5,'18819410005',password('100005'),'yes',1,'m',1,now());

--增加用户的信息1-5
insert into userinfo(user_id, type, information) values(1,'img_url',"http://www.campus_couple.com/imgurl/1");
insert into userinfo(user_id,type, information) values(1,'birthday',"1994-01-01");
insert into userinfo(user_id,type, information) values(1,'nickname',"nickname_1");
insert into userinfo(user_id,type, information) values(1,'description',"I'm number 1");
insert into userinfo(user_id,type, information) values(1,'province_id',1);
insert into userinfo(user_id,type, information) values(1,'location',"广州市番禺区大学城华南理工大学");
insert into userinfo(user_id,type, information) values(1,'profession',"计算机科学与技术");

insert into userinfo(user_id, type, information) values(2,'img_url',"http://www.campus_couple.com/imgurl/2");
insert into userinfo(user_id,type, information) values(2,'birthday',"1994-01-02");
insert into userinfo(user_id,type, information) values(2,'nickname',"nickname_2");
insert into userinfo(user_id,type, information) values(2,'description',"I'm number 2");
insert into userinfo(user_id,type, information) values(2,'province_id',2);
insert into userinfo(user_id,type, information) values(2,'location',"广州市番禺区大学城华南理工大学");
insert into userinfo(user_id,type, information) values(2,'profession',"计算机科学与技术");

insert into userinfo(user_id, type, information) values(3,'img_url',"http://www.campus_couple.com/imgurl/3");
insert into userinfo(user_id,type, information) values(3,'birthday',"1994-01-03");
insert into userinfo(user_id,type, information) values(3,'nickname',"nickname_3");
insert into userinfo(user_id,type, information) values(3,'description',"I'm number 3");
insert into userinfo(user_id,type, information) values(3,'province_id',3);
insert into userinfo(user_id,type, information) values(3,'location',"广州市番禺区大学城华南理工大学");
insert into userinfo(user_id,type, information) values(3,'profession',"计算机科学与技术");

insert into userinfo(user_id, type, information) values(4,'img_url',"http://www.campus_couple.com/imgurl/4");
insert into userinfo(user_id,type, information) values(4,'birthday',"1994-01-04");
insert into userinfo(user_id,type, information) values(4,'nickname',"nickname_4");
insert into userinfo(user_id,type, information) values(4,'description',"I'm number 4");
insert into userinfo(user_id,type, information) values(4,'province_id',4);
insert into userinfo(user_id,type, information) values(4,'location',"广州市番禺区大学城华南理工大学");
insert into userinfo(user_id,type, information) values(4,'profession',"计算机科学与技术");

insert into userinfo(user_id, type, information) values(5,'img_url',"http://www.campus_couple.com/imgurl/5");
insert into userinfo(user_id,type, information) values(5,'birthday',"1994-01-05");
insert into userinfo(user_id,type, information) values(5,'nickname',"nickname_5");
insert into userinfo(user_id,type, information) values(5,'description',"I'm number 5");
insert into userinfo(user_id,type, information) values(5,'province_id',5);
insert into userinfo(user_id,type, information) values(5,'location',"广州市番禺区大学城华南理工大学");
insert into userinfo(user_id,type, information) values(5,'profession',"计算机科学与技术");


----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
------campus

--create campus
insert into campus(campus_id,campus_name, login_name, passwd, school_id,advance_time) values(1,'大学城校区', 'admin1','21232f297a57a5a743894a0e4a801fc3', 1,10);
insert into campus(campus_id,campus_name, login_name, passwd, school_id,advance_time) values(2,'五山校区', 'admin2','21232f297a57a5a743894a0e4a801fc3', 1,20);






