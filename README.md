#### Install dependencies

    pip intsall -r requirements.txt

#### Local settings

    cd kpi_notificator/settings
    cp local.sample.py local.py

#### Run services and web server

    docker-compose up

#### Migrations

    docker exec <container id> python manage.py migrate

#### Diagrams

![Overview](https://g.gravizo.com/source/svg?https://raw.githubusercontent.com/bloogrox/hasoffers-kpi/master/diagrams/overview.plantuml)

![Manager](https://g.gravizo.com/source/svg?https://raw.githubusercontent.com/bloogrox/hasoffers-kpi/master/diagrams/manager.plantuml)
