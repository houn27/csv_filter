# CSV Filter
![alt screenshot](https://raw.githubusercontent.com/houn27/public-img/main/WX20240320-081325.png)

This project is used to infer and convert data types in a CSV dataset, which is developed by python 3.10, Django 3.2 and React 18.2.0. 

##### highlight
* can infer different mixed data types (diffrent data types or some outlier in different rows)
```
int: mixed with int/str
float: mixed with int/str
boolean(true/false or 0/1): mixed with str/number
datetime: mixed with other format/str
complex: mixed with int
category: can be inferred as category when there are small numbers of unique values in a col
```

##### to improve
* can have customized data types
* can convert different datetime formats into one

To run this project, you need to complete the following necessary steps:

#### 1. install python 3 and Django 3.2
   ```python -m pip install Django==3.2.25```
#### 2. set up database
 * make sure you have installed mysql
  * install mysql client
  ```pip install mysqlclient```
  * create new database named 'db_csv'
```
sudo mysql -u root -p
mysql> create database db_csv;
```
* set up your mysql sql account at settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'db_csv', 
        'HOST':'localhost', 
        # 'HOST':'db_mysql',  #mysql name in the docker network
        'PORT':'3306', # port
        'USER':'root', # username
        'PASSWORD':'123' # password
    }
}
```
#### 3. run django
```
python manage.py migrate

python manage.py makemigrations

python manage.py runserver
```

#### 4. run frontend
```
cd frontend
npm start
```
