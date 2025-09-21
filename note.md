**1. 파이썬 가상환경** ->

예제)

* venv 가상환경 만들기 -> python -m venv 가상환경이름
* 가상환경 실행하기 -> source 가상환경이름/bin/activate
* 가상환경 끄기 -> deactivate
* 가상환경 설치 리스트 확인, 복제, 설치 	-> pip freeze > requirements.txt

 					-> pip install -r requirements.txt

python manage.py createsuperuser
Username (leave blank to use 'dmltj'): euiseok_jeong
Email address: euiseokjeongnz@gmail.com
Password: dmltjr5050

oepn server commend: python manage.py runserver 8000

pip freeze > requirements.txt
pip install -r requirements.txt

MariaDB 서버 켜져있는지 확인 -> mysql -u root -p -h 127.0.0.1 -P 3306

USE myshop;
SHOW TABLES;