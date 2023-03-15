# Houselog

A simple tracking system for house-related tasks

Includes:
- frequency tracker
- email reminder (WIP)
- notes (like furnace filter size, or fridge model, etc)

<table>
    <tr>
        <td>
            <img src="docs/images/login.png" width=400>
        </td>
        <td>
            <img src="docs/images/dashboard.png" width=400>
        </td>
    </tr>
</table>

### Usage

```
mv .env.example .env
vim .env
docker-compose build
docker-compose run web python manage.py migrate
docker-compose run web python manage.py collectstatic
docker-compose run web python manage.py createsuperuser
docker-compose up
```
