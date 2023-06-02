# Pinechat
This is made with **Django**(Python),HTML and 
[Bootstarp](https://getbootstrap.com/)

# Deployment
To run this project,you need to installl python 3 and follow this commands
```bash
git clone https://github.com/Foisal1301/PineChat.git
cd PineChat-main
pip3 install -r requirements.txt
python3 manage.py makemigrations core
python3 manage.py makemigrations room
python3 manage.py migrate
python3 manage.py runserver
```
It will start a development server in [localhost:8000](http://localhost:8000)<br>
After that,go to django_project > **settings.py** file<br>
Here,you need to put your email and password in **EMAIL_HOST_USER** and **EMAIL_HOST_PASSWORD**
[**Note**:Password will not be actual password of your google account,it will be an app password provided by google]
```python
EMAIL_HOST_USER = "yourmail@gmail.com"
EMAIL_HOST_PASSWORD = "yourpassword"
```
<br>
For social login,you need to add Social Appliactions with client id and secret key from admin panel of the site.