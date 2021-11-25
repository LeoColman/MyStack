FROM nextcloud:fpm-alpine

# For cron configuring
# https://stackoverflow.com/questions/36453787/failed-to-edit-crontab-linux-alpine
RUN apk add --update busybox-suid

# Crontabs
USER www-data
RUN crontab -l | { cat; echo "*/30 * * * * php -f /var/www/nextcloud/occ face:background_job -t 900"; } | crontab -
