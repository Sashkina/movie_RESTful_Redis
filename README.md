# movie_RESTful_Redis

Описание:  
Проект movie_RESTful - это простое api, написанное на Flask с помощью базы данных Redis, позволяющее добавлять, изменять и получать данные о кинофильмах.
После запуска docker-compose работает на порту 8080.

Технологии:  
Python==3.11.5  
Flask==3.0.0  
Flask_RESTful==0.3.10  
redis==5.0.1  

Как запустить проект:  

- Клонировать репозиторий и перейти в него в командной строке:  

git clone https://github.com/Sashkina/movie_RESTful_Redis.git  

- Cоздать и активировать виртуальное окружение:  

python3 -m venv venv  
source venv/bin/activate  

- Установить зависимости из файла requirements.txt:  

python3 -m pip install --upgrade pip  
pip install -r requirements.txt  

- Запустить  

docker-compose up
