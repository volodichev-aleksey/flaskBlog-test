**DEPLOY**

Подразумевается, что docker и certbot уже стоят, dns, фаервол и ssh настроены.
1. Склонировать репозиторий:

git clone https://github.com/volodichev-aleksey/flaskBlog-test.git
3. Перейти в каталог и запустить:

docker compose up -d
4. Получить le-сертификат командой:

sudo certbot certonly --webroot --webroot-path ./nginx/certbot/ -d test-devops2.vizorlabs.ru
ответить на вопросы
5. Раскоментировать строки с 12 по 20 в файле  ./nginx/conf.d/test.conf
6. Перезапустить nginx командой:

docker restart nginx 
7. Добавить права на исполнение файлам backup.sh и restore.sh

chmod a+x backup.sh restore.sh


**BACKUP**

Для бэкапа сервера выполнить в каталоге проекта файл backup.sh. В каталоге обозначенном в переменной backup_path будет создана копия базы с названием "db.дата_время" и симлинк на неё с названием db.latest.

Для восстановления необходимо выполнить файл restore.sh либо вручную скопировать нужную версию файлов из более ранних бэкапов.
