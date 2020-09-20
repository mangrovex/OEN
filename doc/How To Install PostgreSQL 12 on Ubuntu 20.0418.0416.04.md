# How To Install PostgreSQL 12 on Ubuntu 20.04/18.04/16.04

This guide will walk you through the steps used to install PostgreSQL 12 on Ubuntu 20.04/18.04/16.04 Linux system. PostgreSQL is one of the most widely adopted object-relational database management system based on POSTGRES 4.2. PostgreSQL 12 has been released for general use, fit for Production and all Development use cases.

If you want to see all the new features and improvements in PostgreSQL 12, visit the [PostgreSQL 12 release notes ](https://www.postgresql.org/about/news/1976/)page so check the major enhancements in PostgreSQL 12. Without much wait, let’s buckle to the installation of PostgreSQL 12 on Ubuntu 20.04/18.04/16.04 Linux system.

## Step 1: Update system

It is recommended to update your current system packages if it is a new server instance.

```
sudo apt update
sudo apt -y install vim bash-completion wget
sudo apt -y upgrade
```

A reboot is necessary after an upgrade.

```
sudo reboot
```

## Step 2: Add PostgreSQL 12 repository

We need to import GPG key and add PostgreSQL 12 repository into our Ubuntu machine. Run the following commands to accomplish this.

```
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```

After importing GPG key, add repository contents to your Ubuntu 18.04/16.04 system:

```
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
```

The repository added contains many different packages including third party addons. They include:

- postgresql-client
- postgresql
- libpq-dev
- postgresql-server-dev
- pgadmin packages

## Step 3: Install PostgreSQL 12 on Ubuntu 20.04/18.04/16.04 LTS

Now the repository has been added successfully, update the package list and install PostgreSQL 12 server and client packages on your Ubuntu 20.04/18.04/16.04 Linux system.

```
sudo apt update
sudo apt -y install postgresql-12 postgresql-client-12
```

A successful installation prints a message that is similar to one shared in the next screenshot.



[![img](https://computingforgeeks.com/wp-content/uploads/2019/10/install-postgresql-12-ubuntu-01-1024x576.png?ezimgfmt=rs:696x392/rscb8/ng:webp/ngcb8)](data:image/svg+xml,<%2Fsvg>)

The PostgreSQL service is started and set to come up after every system reboot.

```
$ systemctl status postgresql.service 
 ● postgresql.service - PostgreSQL RDBMS
    Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
    Active: active (exited) since Sun 2019-10-06 10:23:46 UTC; 6min ago
  Main PID: 8159 (code=exited, status=0/SUCCESS)
     Tasks: 0 (limit: 2362)
    CGroup: /system.slice/postgresql.service
 Oct 06 10:23:46 ubuntu18 systemd[1]: Starting PostgreSQL RDBMS…
 Oct 06 10:23:46 ubuntu18 systemd[1]: Started PostgreSQL RDBMS.

$ systemctl status postgresql@12-main.service 
 ● postgresql@12-main.service - PostgreSQL Cluster 12-main
    Loaded: loaded (/lib/systemd/system/postgresql@.service; indirect; vendor preset: enabled)
    Active: active (running) since Sun 2019-10-06 10:23:49 UTC; 5min ago
  Main PID: 9242 (postgres)
     Tasks: 7 (limit: 2362)
    CGroup: /system.slice/system-postgresql.slice/postgresql@12-main.service
            ├─9242 /usr/lib/postgresql/12/bin/postgres -D /var/lib/postgresql/12/main -c config_file=/etc/postgresql/12/main/postgresql.conf
            ├─9254 postgres: 12/main: checkpointer   
            ├─9255 postgres: 12/main: background writer   
            ├─9256 postgres: 12/main: walwriter   
            ├─9257 postgres: 12/main: autovacuum launcher   
            ├─9258 postgres: 12/main: stats collector   
            └─9259 postgres: 12/main: logical replication launcher   
 Oct 06 10:23:47 ubuntu18 systemd[1]: Starting PostgreSQL Cluster 12-main…
 Oct 06 10:23:49 ubuntu18 systemd[1]: Started PostgreSQL Cluster 12-main.

$ systemctl is-enabled postgresql
enabled
```

## Step 4: Test PostgreSQL Connection

During installation, a postgres user is created automatically. This user has full **superadmin** access to your entire PostgreSQL instance. Before you switch to this account, your logged in system user should have sudo privileges.

```
sudo su - postgres
```

Let’s reset this user password to a strong Password we can remember.

```
psql -c "alter user postgres with password 'StrongAdminP@ssw0rd'"
```

Start PostgreSQL prompt by using the command:

```
$ psql
```

Get connection details like below.

```
$ psql
psql (12.0 (Ubuntu 12.0-1.pgdg18.04+1))
Type "help" for help.

postgres=# \conninfo
You are connected to database "postgres" as user "postgres" via socket in "/var/run/postgresql" at port "5432".
```

Let’s create a test database and user to see if it’s working.

```
postgres=# CREATE DATABASE mytestdb;
CREATE DATABASE
postgres=# CREATE USER mytestuser WITH ENCRYPTED PASSWORD 'MyStr0ngP@SS';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE mytestdb to mytestuser;
GRANT
```

List created databases:

```
postgres=# \l
                               List of databases
   Name    |  Owner   | Encoding | Collate |  Ctype  |    Access privileges    
-----------+----------+----------+---------+---------+-------------------------
 mytestdb  | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =Tc/postgres           +
           |          |          |         |         | postgres=CTc/postgres  +
           |          |          |         |         | mytestuser=CTc/postgres
 postgres  | postgres | UTF8     | C.UTF-8 | C.UTF-8 | 
 template0 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres            +
           |          |          |         |         | postgres=CTc/postgres
 template1 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres            +
           |          |          |         |         | postgres=CTc/postgres
(4 rows)
```

Connect to database:

```
postgres-# \c mytestdb
You are now connected to database "mytestdb" as user "postgres".
```

Other PostgreSQL utilities installed such as **createuser** and **createdb** can be used to create database and users.

```
postgres@ubuntu:~$ createuser myuser --password
Password:
postgres@ubuntu:~$ createdb mydb -O myuser
postgres@ubuntu:~$ psql -l 
```

We can create and connect to a database on PostgreSQL server.

## Step 5: Configure remote Connection (Optional)

Installation of PostgreSQL 12 on Ubuntu only accepts connections from localhost. In ideal production environments, you’ll have a central database server and remote clients connecting to it – But of course within a **private network** (LAN).

To enable remote connections, edit PostgreSQL configuration file:

```
sudo nano /etc/postgresql/12/main/postgresql.conf 
```

Uncomment line **59** and change the Listen address to accept connections within your networks.

```
# Listen on all interfaces
listen_addresses = '*'

# Listen on specified private IP address
listen_addresses = '192.168.10.11'
```

After the change, restart postgresql service.

```
sudo systemctl restart postgresql
```

Confirm Listening addresses.

```
# netstat  -tunelp | grep 5432
tcp        0      0 0.0.0.0:5432            0.0.0.0:*               LISTEN      111        112837     11143/postgres      
tcp6       0      0 :::5432                 :::*                    LISTEN      111        112838     11143/postgres      
```

## Step 6: Install pgAdmin4 Management Tool

If you want to manage your PostgreSQL database server from a web interface, then install pgAdmin4.

[Install pgAdmin4 on Ubuntu](https://computingforgeeks.com/how-to-install-pgadmin-4-on-ubuntu/)

Enjoy using PostgreSQL 12 on Ubuntu 20.04/18.04/16.04. Other guides related to databases are shared in the list below.