# Guest

A Web project based on Django, used for Web programming and Web API testing practice.

Installed apps:

- sign

## Commands

- `python3 manage.py runserver` or `python3 manage.py runserver 127.0.0.1:8001` to launch the site.
- `python3 manage.py shell` to enable Django shell console

### How to install Mysql in Ubuntu 16.04 and enable remote-access?

1. `sudo apt-get install mysql-server`, `sudo apt isntall mysql-client`, `sudo apt install libmysqlclient-dev`.
2. Use `sudo netstat -tap | grep mysql` to check whether mysql is running, open mysql console using `mysql -uroot -p`.
3. To enable remote-access, `sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf` and comment the line of `bind-address = 127.0.0.1`.
4. Open mysql console again, execute `grant all on *.* to root@'%' identified by 'ROOT-PASSWORD' with grant option;` and `flush privileges;`.
5. Quit mysql console and restart mysql service by `service mysql restart`.

## Setup

- Mysql service is required, IP address, user name and password need be configured in guest/settings.py as part of DATABASES configuraiton.
- `mysql> create database guest character set utf8;` to init guest database in Mysql at very beiginning.
- `python3 manage.py createsuperuser` to create super user account.