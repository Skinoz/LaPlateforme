# LaPlateforme
LaPlateforme is a project in developpement to create a training plateforme. Create with django and vue to show information. 
===========================
Developement Environement :
===========================

create venv :
```sh
python3 -m venv PATH
```

Activate venv :
On Windows, run:
```sh
tutorial-env\Scripts\activate
```
On Unix or MacOS, run:
```sh
source tutorial-env/bin/activate
```

Next to activate, it will need to install pip package : 
```sh
pip3 install -r requirements.txt
```

Laragon can it install to create a database : https://laragon.org/index.html
Laragon >= 6.0 

Configure Src/LaPlateforme/settings.py with your credentials and execute to migrate application to your database :
```sh
python manage.py migrate                                                                                                                             
```
Start web app with 
```sh
python manage.py runserver                 
```

Webhook test