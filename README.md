# news feed

we have two main apps here profiles which handles user related operations
and posts which handles all the posts related operations 

## Installation

to install we have to options normal pip installation and docker installation:

with docker its easy just navigate to the root dir of the project and run the following:

```bash
docker compose up
```
for normal installation a venv is preferred so all you need to do is to make sure you have python 3.10 installed 

clone this repostory and run the following 

```bash
python -m venv venv
```

activate your venv 

windows 
```bash
cd venv/Scripts/
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
./activate
```

```bash
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
```

```bash
./activate
```

on  mac or linux 

```bash
source venv/bin/activate
```

finally run the following to install the requirements  make sure you are in the project base dir

```bash
pip install -r requirments.txt
```

now you can run the server using the [post man collection ](https://documenter.getpostman.com/view/14647839/2s8479ybmz)assumes you are running  on port 8080

```bash
python manage.py runserver 127.0.0.1:8080
```


if you don't have the provided test sqllite DB 
you can test running 

to seed users
```bash
python manage.py seed_users --number 1000
```
to seed posts
```bash
python manage.py seed_posts --number 1000
```
to seed subs
```bash
python manage.py seed_subs --number 500
```


## usage  and testing 
please refer to the provided [postman collection file](https://documenter.getpostman.com/view/14647839/2s8479ybmz) "news feed.postman_collection.json"

you can easily import it in your post man and you will find 2 folders one for posts and one for profiles 

you can test with these endpoints and they have descriptions of the fields as well if you need a data representation you can also refer to [the admin panel](http://127.0.0.1:8080/admin)


there is also a swagger documentation which will list the endpoints at [here](http://127.0.0.1:8080/)

note that it will only list the endpoints with no query parameters since query parameters are not officially supported by swagger for DRF yet 


for further explanation please refrere to the doc strings on the views and the doc.md file


## License
[by khaled yasser](kikokhaled.u@gmail.com)