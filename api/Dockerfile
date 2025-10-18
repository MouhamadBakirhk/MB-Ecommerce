# استخدم صورة PHP مع Composer و Apache
FROM php:8.2-apache

# فعّل mod_rewrite
RUN a2enmod rewrite

# نسخ ملفات المشروع
COPY . /var/www/html

# تثبيت Composer
RUN apt-get update && apt-get install -y unzip git libzip-dev && docker-php-ext-install zip pdo pdo_mysql
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# تثبيت الـ dependencies
WORKDIR /var/www/html
RUN composer install --no-interaction --optimize-autoloader

# توليد المفتاح
RUN php artisan key:generate

EXPOSE 80
CMD ["apache2-foreground"]
