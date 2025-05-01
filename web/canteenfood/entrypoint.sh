#!/bin/bash

chmod 600 /entrypoint.sh

mkdir -p /run/mysqld
chown -R mysql:mysql /run/mysqld
mysql_install_db --user=mysql --ldata=/var/lib/mysql
mysqld --user=mysql --console --skip-name-resolve --skip-networking=0 &

while ! mysqladmin ping -h'localhost' --silent; do echo "not up" && sleep .2; done


export DB_USER="user_$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 5 | head -n 1)"
export DB_NAME="db_$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 5 | head -n 1)"

mysql -u root << EOF
CREATE DATABASE $DB_NAME;
CREATE TABLE $DB_NAME.food (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    oldvalue VARCHAR(255),
    price float,
    PRIMARY KEY (id)
);

INSERT INTO $DB_NAME.food (name, oldvalue, price) VALUES ('Spaghetti', '', 2.99);
INSERT INTO $DB_NAME.food (name, oldvalue, price) VALUES ('Burger', '', 100.99);
INSERT INTO $DB_NAME.food (name, oldvalue, price) VALUES ('Cookies', '', 22.30);
INSERT INTO $DB_NAME.food (name, oldvalue, price) VALUES ('Lasagna', '', 7.50);
INSERT INTO $DB_NAME.food (name, oldvalue, price) VALUES ('Schnitzel', '', 5000.99);
INSERT INTO $DB_NAME.food (name, oldvalue, price) VALUES ('','YToyOntpOjA7czo1OiJQaXp6YSI7aToxO2Q6MC45OTt9', 0);

CREATE USER '$DB_USER'@'%';
GRANT SELECT, UPDATE ON *.* TO '$DB_USER'@'%';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'test123';
FLUSH PRIVILEGES;

EOF

echo -e "fastcgi_param DB_NAME $DB_NAME;\nfastcgi_param DB_USER $DB_USER;\nfastcgi_param DB_PASS '';" >> /etc/nginx/fastcgi_params

/usr/bin/supervisord -c /etc/supervisord.conf