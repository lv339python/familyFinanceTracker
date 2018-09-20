# familyFinanceTracker


## Description
ToDo

## Technologies
* Python (3.7.0)
* PostgreSQL (10.5)
* npm (3.5.2)

## Install
For the next steps of service installation, you will need setup of Ubuntu OS


### Install and configure PostgreSQL server on your local machine:
```
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql postgres

postgres=# \password
Enter new password:
Enter it again:

postgres=# CREATE DATABASE your_custom_db_name;

postgres=# \q
```


### Go to the cloned repository and install requirement project's packages
```
pip install -r requirements.txt
```

* Go to the `iBudget/ibudget` project directory and create your own local_settings.py in the folder with settings.py and configure correct database connection.
```
SECRET_KEY = "YOUR_SECRET_KEY_FOR_DJANGO_APP"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_custom_db_name',
        'USER': 'your_custom_db_user',
        'PASSWORD': 'your_password_for_user_above',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'

AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'

AWS_STORAGE_BUCKET_NAME = 'AWS_STORAGE_BUCKET_NAME'
```


* Go to the folder with `manage.py` file and run migrate files
```
python manage.py migrate
```

### Install npm and vue-cli on your local machine:
```
sudo apt-get install npm
sudo npm install -g vue-cli 
```

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build
```

For detailed explanation on how things work, consult the [docs for vue-loader](http://vuejs.github.io/vue-loader).

## Run Project

### Django
Go to the folder with `manage.py` file, run iBudget.api 
```
python manage.py runserver
```
