#!/bin/bash
set -e

# sudo pacman -Syu

if ! pacman -Q git; then
    echo "---> Git not installed. Installing..."
    sudo pacman -S git
    echo "---> Supply your git username:"
    read git_user
    git config --global user.name "$git_user"
    echo "---> Supply your git email:"
    read git_email
    git config --global user.email "$git_email"
else
    echo "---> Git already installed. Don't forget to set your credentials."
fi

if [ ! -d "ds4reboot" ]; then
    git clone "https://github.com/studentenhuisDS4/ds4reboot.git"
else
    echo "---> Skipping git clone. Found the ds4reboot folder already."
fi

cd ds4reboot
git checkout develop

if ! pacman -Q python-pip; then
    sudo pacman -S python-pip
else    
    echo "---> python-pip already installed."
fi

if ! pacman -Q postgresql; then
    sudo pacman -S postgresql
else    
    echo "---> postgresql already installed."    
fi

if [ ! -d "/var/lib/postgres/data" ]; then
    sudo -u postgres mkdir /var/lib/postgres/data
    sudo chown -c -R postgres:postgres /var/lib/postgres
    sudo -u postgres initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data'
fi


echo "
---> Return to sudo. Starting postgresql service.
"
#https://netarky.com/programming/arch_linux/Arch_Linux_PostgreSQL_database_setup.html
sudo systemctl enable postgresql
sudo systemctl start postgresql.service

echo "---> Trying to check if postgres is running: "
systemctl status postgresql.service | grep "active (running)"

if [ "$USER" == "root" ]; then
    echo "---? Specify a non-root user to be used on the database:"
    read DB_USER
else 
    echo "---> Took non-root '$USER' as user to be added."
    DB_USER="$USER"
fi

if ! psql --list | grep "$norootuser"; then
    echo "Couldn't find user database...?"
    createuser -s -U postgres "$norootuser"
fi

if ! psql --list | grep ds4db; then
    createdb
    createdb ds4db
else 
    echo "---!> ds4db exists already"
fi

echo "---> Creating a random password for the database role"
DB_PWD="$(cat /dev/urandom | tr -dc 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)' | fold -w 10 | head -n 1)"

cd ds4reboot/

echo "---> Auto-generating SECRET_KEY:"
rng_secret="$(cat /dev/urandom | tr -dc 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)' | fold -w 50 | head -n 1)"

file="secret_settings.py"

if [ ! -e "${file}" ]; then
    touch "${file}"
fi

echo "# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$rng_secret'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['ds4.nl', 'localhost']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'PORT': '5432',
        'NAME': 'ds4db',
        'USER': '$DB_USER',
        'PASSWORD': '$DB_PWD',
        'HOST': 'localhost',
    }
}
SECRET_APPS = []" > "${file}"

echo "---!> (Re-)created settings file with random secret key+pw."

echo "---> Assigning pw to postgres."
sudo -u ${DB_USER} psql -c "ALTER USER postgres WITH PASSWORD '${DB_PWD}';"

cd ..
if ! pip freeze | grep "virtualenv"; then
    echo "Virtualenv not installed"
    sudo pip install virtualenv
fi

virtualenv venv

sudo pip install -r requirements.txt --user

python manage.py migrate

echo "---!>Creating superuser (name: admin, pw:admin):"
echo "from django.contrib.auth.models import User;
from user.models import Housemate;
User.objects.filter(username='admin').delete(); 
u=User.objects.create_superuser('admin', 'admin@mail.com', 'admin');
u2=User.objects.create_superuser('huis', 'studentenhuisds4@gmail.com', 'Studentenhuis');
Housemate.objects.create(user=User.objects.get(username='admin'), display_name='Admin');
Housemate.objects.create(user=User.objects.get(username='huis'), display_name='Huis')" | python manage.py shell

echo "---> Finished! When you press enter the server will be started... 'python manage.py runserver'"

python manage.py runserver
