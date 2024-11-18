FROM ubuntu:22.04

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 php8.1 libapache2-mod-php8.1 && \
    apt-get clean

RUN a2enmod php8.1

RUN echo '<Directory /var/www/>\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>' >> /etc/apache2/sites-available/000-default.conf

# настройка прав
COPY . /var/www/html
RUN mkdir -p /var/www/html/uploads && \
    chown -R www-data:www-data /var/www/html && \
    chown -R www-data:www-data /var/www/html/uploads && \
    chmod -R 755 /var/www/html && \
    chmod -R 775 /var/www/html/uploads

RUN sed -i 's/Options Indexes FollowSymLinks/Options FollowSymLinks/' /etc/apache2/apache2.conf

EXPOSE 8080

CMD ["apache2ctl", "-D", "FOREGROUND"]