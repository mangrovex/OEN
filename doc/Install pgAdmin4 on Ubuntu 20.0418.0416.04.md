## Install pgAdmin4 on Ubuntu 20.04/18.04/16.04

The one requirement for installation of pgAdmin4 on Ubuntu 20.04/18.04/16.04 is PostgreSQL server. You can choose to go with any version of PostgreSQL server >=9.6. We have guides which can be used as reference while installing PostgreSQL database server.

[Install PostgreSQL 12 on Ubuntu](https://computingforgeeks.com/install-postgresql-12-on-ubuntu/)

Having completed installation of PostgreSQL database server on Ubuntu, proceed to install and initiate pgAdmin4 on Ubuntu 18.04 / Ubuntu 16.04. See below

## Add PostgreSQL APT repository

The PostgreSQL Global Development Group (PGDG) maintains an APT repository of PostgreSQL packages for Debian and Ubuntu. The repository can be added using the commands shown below.

```
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
```

The repository added contains many different packages including third party addons. Mainly:

- postgresql-client
- **postgresql** core database server
- libpq-dev
- postgresql-server-dev
- pgadmin packages

## Install pgAdmin4 on Ubuntu 20.04/18.04/16.04

Finally, update the package lists.

```
sudo apt update
```

To install pgAdmin4 packages on Ubuntu 20.04/18.04/16.04 system, run these commands, providing correct version number:

```
sudo apt update
sudo apt install pgadmin4 pgadmin4-apache2
```

During installation, you’re asked to configure initial user account. Provide email address.

[![Install pgAdmin4 on Ubuntu](https://computingforgeeks.com/wp-content/uploads/2019/10/install-pgadmin-ubuntu-01-1024x368.png?ezimgfmt=rs:696x250/rscb8/ng:webp/ngcb8)](data:image/svg+xml,<%2Fsvg>)

Also set admin password

[![Install pgAdmin4 on Ubuntu](https://computingforgeeks.com/wp-content/uploads/2019/10/install-pgadmin-ubuntu-02-1024x451.png?ezimgfmt=rs:696x307/rscb8/ng:webp/ngcb8)](data:image/svg+xml,<%2Fsvg>)

Apache service should have been started after installation.

```
$ systemctl status apache2
● apache2.service - The Apache HTTP Server
   Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
  Drop-In: /lib/systemd/system/apache2.service.d
           └─apache2-systemd.conf
   Active: active (running) since Sun 2019-10-06 13:47:00 UTC; 23s ago
 Main PID: 5678 (apache2)
    Tasks: 83 (limit: 2362)
   CGroup: /system.slice/apache2.service
           ├─5678 /usr/sbin/apache2 -k start
           ├─5682 /usr/sbin/apache2 -k start
           ├─5683 /usr/sbin/apache2 -k start
           └─5684 /usr/sbin/apache2 -k start

Oct 06 13:47:00 ubuntu18 systemd[1]: Stopped The Apache HTTP Server.
Oct 06 13:47:00 ubuntu18 systemd[1]: Starting The Apache HTTP Server...
Oct 06 13:47:00 ubuntu18 systemd[1]: Started The Apache HTTP Server.
```

If you have UFW firewall configured, allow http and https traffic.

```
sudo ufw allow http
sudo ufw allow https
```

Open your browser and `http://[ServerIP_or_domain]/pgadmin4`.

[![Install pgAdmin4 on Ubuntu](https://computingforgeeks.com/wp-content/uploads/2019/10/install-pgadmin-ubuntu-03-1024x497.png?ezimgfmt=rs:696x338/rscb8/ng:webp/ngcb8)](data:image/svg+xml,<%2Fsvg>)

Login by using set email address and password.

[![Install pgAdmin4 on Ubuntu](https://computingforgeeks.com/wp-content/uploads/2019/10/install-pgadmin-ubuntu-04-1024x419.png?ezimgfmt=rs:696x285/rscb8/ng:webp/ngcb8)](data:image/svg+xml,<%2Fsvg>)

Wait for a few seconds for initialization to complete.

[![Install pgAdmin4 on Ubuntu](https://computingforgeeks.com/wp-content/uploads/2019/10/install-pgadmin-ubuntu-05-1024x320.png?ezimgfmt=rs:696x218/rscb8/ng:webp/ngcb8)](data:image/svg+xml,<%2Fsvg>)

On the first page of pgAdmin, add a PostgreSQL server to administer with pgAdmin by clicking on **“Add New Server”.** This can be local or a remote PostgreSQL server.

[![Install pgAdmin4 on Ubuntu](https://computingforgeeks.com/wp-content/uploads/2018/11/pgAdmin-centos-7-fedora-29-add-server-01-1024x202.png?ezimgfmt=rs:696x137/rscb8/ng:webp/ngcb8)](data:image/svg+xml,<%2Fsvg>)

Under the **“General”** section, give the server a name & description.

[![Install pgAdmin4 on Ubuntu](https://computingforgeeks.com/wp-content/uploads/2018/11/pgAdmin-centos-7-fedora-29-addd-server-02-1024x777.png?ezimgfmt=rs:696x528/rscb8/ng:webp/ngcb8)](data:image/svg+xml,<%2Fsvg>)

Under **“Connection”** tab, provide access details – DB host, DB user and Password.

[![Install pgAdmin4 on Ubuntu](https://computingforgeeks.com/wp-content/uploads/2018/11/pgAdmin-centos-7-fedora-29-add-server-03-1013x1024.png?ezimgfmt=rs:696x704/rscb8/ng:webp/ngcb8)](data:image/svg+xml,<%2Fsvg>)

When done, Click **Save** button to save the configurations. If you were successful adding the server, the name will appear in the left sidebar.

[![Install pgAdmin4 on Ubuntu](https://computingforgeeks.com/wp-content/uploads/2019/03/install-pgadmin-debian-10-9-8-06-1024x297.png?ezimgfmt=rs:696x202/rscb8/ng:webp/ngcb8)](data:image/svg+xml,<%2Fsvg>)

Select the server to see database summary information and make changes. Learn more on how to use pgAdmin from the [documentation](https://www.pgadmin.org/docs/pgadmin4/dev/) page.