FROM debian:bullseye-slim@sha256:6344a6747740d465bff88e833e43ef881a8c4dd51950dba5b30664c93f74cbef

# Setup user
RUN useradd www

# Install system packeges
RUN apt-get update && apt-get install -y supervisor nginx lsb-release mariadb-server mariadb-client wget gcc

# Add repos
RUN wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
RUN echo "deb https://packages.sury.org/php/ bullseye main" | tee /etc/apt/sources.list.d/php.list

# Install PHP dependencies
RUN apt update && apt install -y php7.1-fpm php7.1-mysql

# Configure php-fpm and nginx
COPY config/fpm.conf /etc/php/7.1/fpm/php-fpm.conf
COPY config/supervisord.conf /etc/supervisord.conf
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/mariadb.conf /etc/mysql/mariadb.conf.d/50-server.cnf

# Copy challenge files
COPY challenge /www

# Copy flag
COPY flag.txt /
COPY logs.txt /


# Add readflag binary and prepare flag
COPY readflag.c /
RUN gcc /readflag.c -o /readflag \
    && chown root:root /readflag \
    && chmod +s /readflag \
    && rm /readflag.c \
    && chmod 400 /flag.txt

# Setup permissions
RUN chown -R www:www /www /var/lib/nginx
RUN chown www:www /logs.txt

RUN apt-get remove gcc wget -y

# Expose the port nginx is listening on
EXPOSE 80

# Start db and start supervisord
COPY --chown=root entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
