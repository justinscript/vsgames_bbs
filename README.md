
# vsgames bbs
Django开发的激战2游戏社区
========
Env
------------
- Python 2.7.3
- Django 1.4
- MySQL
- uwsgi
- Nginx

Install
-------
```
$ apt-get install automake build-essential flex git libmysqlclient-dev libpcre3 libpcre3-dev libpython2.7 libssl libssl-dev libtool libzip1 libzip-dev mysql mysql-client mysql-server pip python-dev python-pip python-pyasn1 libcurl4-openssl-dev tcl8.5 python-pylibmc python-imaging sudo pip install django-simple-captcha

$ python setup.py install
$ ...

$ /opt/bin/nginx start
$ /opt/run/openssh/sbin/sshd
$ /opt/bin/uwsgi stop 8001 && sleep 3 && /opt/bin/uwsgi start 8001
```