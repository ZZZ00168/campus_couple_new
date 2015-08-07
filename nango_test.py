__author__ = 'luo.mingnan'
import urllib
import urllib2
import json


#1.9  password_change
def userPasswordChange(mobile, old_password, new_password):
    data = {'mobile': mobile, 'old_password': old_password, 'new_password': new_password}
    data = urllib.urlencode(data)
    req = urllib2.Request(url="http://localhost:8080/user/password/change", data=data)
    return urllib2.urlopen(req).read()
# response=userPasswordChange("18819410001","100001","100001")
# print response

#1.10   password/forget
def userPasswordForget(mobile):
    data = {'mobile': mobile}
    data = urllib.urlencode(data)
    req = urllib2.Request(url="http://localhost:8080/user/password/forget", data=data)
    return urllib2.urlopen(req).read()
# response=userPasswordForget("18819410000")
# print response

#1.11  password_change
def userVerifyPasswordChange(mobile, verify_code, new_password):
    data = {'mobile': mobile, 'verify_code': verify_code, 'new_password': new_password}
    data = urllib.urlencode(data)
    req = urllib2.Request(url="http://localhost:8080/user/password/verify", data=data)
    return urllib2.urlopen(req).read()
# response=userVerifyPasswordChange("18819410000","10000","100000")
# print response

#1.12---------------------?????????????



#4.1 campus/login
def campusLogin(login_name,password):
    data = {'login_name': login_name, 'password': password}
    data = urllib.urlencode(data)
    req = urllib2.Request(url="http://localhost:8080/campus/login", data=data)
    return urllib2.urlopen(req).read()
# response=campusLogin("admin1","admin")#db340f93d690a9840df85c24b64d767f
# print response


#4.2 campus/logout
def campusLogout(access_token):
    data = {'access_token': access_token}
    data = urllib.urlencode(data)
    req = urllib2.Request(url="http://localhost:8080/campus/logout", data=data)
    return urllib2.urlopen(req).read()
# response = campusLogout("")
# print response



#10.5 /user/post/comment/list
def userPostCommentList(access_token=None, user_id=None, post_id=None):
    data = {'access_token': access_token,'user_id':user_id,'post_id':post_id}
    data = urllib.urlencode(data)
    req = urllib2.Request(url="http://localhost:8080/user/post/comment/list", data=data)
    return urllib2.urlopen(req).read()
response = userPostCommentList("123456",2,1)
print response