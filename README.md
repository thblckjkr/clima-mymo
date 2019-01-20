# clima-mymo

A little tool to translate mysql from WeeWx into mongodb using mysql binlog (*Like the redis*)

- Thanks to @nevill for his project [ZongJi](https://github.com/nevill/zongji)
- Thanks to the marvelous documentation of [Maxwell's daemon](http://maxwells-daemon.io/) that allowed me to understand better the redis configurations

> Author: Teo Gonzalez Calzada [@thblckjkr]

## How it works?

In simple terms, it reads the binlog file of MySQL, and replicates it to a mongo database.

**What happens if the service is down, but MySQL is still running?**

Since, this daemon reads the binlog file, anything happens. When you restart the service, it will read all the missed events from the binlog. No losts.

> Unless, you set **startAtEnd** on the initialization of ZongJi to `true`

## Requirements

### TL;DR

A MySQL server, a mongoDB server, a NodeJS installed, **npm** and access to the servers.

## Installation

*First, clone this repository*

### Install the dependencies

```
npm install
```

### Enable access from MySQL to redis clients

Enable logging in MySQL. This allow the redis client to read the binary log.

To do it, search for `mysqld.cnf` (In my case, with mysql under Ubuntu 16.04 is located on `/etc/mysql/mysql.conf.d/`) and do the following changes to the file

```conf
# Must be unique integer from 1-2^32
server-id        = 1
# Row format required for ZongJi
binlog_format    = row
# Directory must exist. This path works for Linux. Other OS may require
#   different path.
log_bin          = /var/log/mysql/mysql-bin.log

binlog_ignore_db = mysql       # Optional but RECOMMENDED. 
binlog_do_db     = employees   # Optional, limit which databases to log
expire_logs_days = 10          # Optional, purge old logs
max_binlog_size  = 100M        # Optional, limit log size
```

> Note: Why i recommend the use of *binlog_ignore_db* over *binlog_do_db*? Because if you specify from wich databases do the binlog, you should restart the server everytime that you'll need to add another database. But, it's not the case with the *ignore* flag.
>
> *server-id* is used on case of having more than one instance of mysql on the same server. If you have only one instance, leave it on 1

Create a new user for the redis (On MySQL shell)

```sql
-- For running it in the same server that is MySQL
GRANT SELECT, REPLICATION CLIENT, REPLICATION SLAVE on *.* to 'your_username'@'localhost' identified by 'SECURE_PASSWORD';

GRANT ALL on your_username.* to 'your_username'@'localhost';

-- For running it from **another** server
GRANT ALL on your_username.* to 'your_username'@'%' identified by 'SECURE_PASSWORD';

GRANT SELECT, REPLICATION CLIENT, REPLICATION SLAVE on *.* to 'your_username'@'%';
```

Copy the `database/config.example.json` to `config/database.json` and save your previously generated credentials credentials

```json
{
    "mysql" :
    {
        "serverId" : 1,
        "host": "localhost",
        "username": "your_username",
        "password": "your_password",
    },
}
```

## Configuration

### Specify the databases list

Instead of modifying the *binlog_do* and *binlog_ignore* fields of `mysqld.conf`, you can add the following line to `mymo.js` inside ZongJi initialization:

```js
var zongji = new ZongJi({
   serverId : db.mysql.serverId,
   host: db.mysql.host,
   user: db.mysql.username,
   password: db.mysql.password,
   includeSchema: db.mysql.schemas // Add this line
});
```
And update the schemas on config file as desired


> Remember to add mysql, and the others, to *binlog_ignore* on *mysqld.conf*, to prevent logs becoming unnecessary big

## Running

If you installed and configured the service, just run it. Prefferably, on a tmux window.

```
npm start

OR

node mymo.js
```