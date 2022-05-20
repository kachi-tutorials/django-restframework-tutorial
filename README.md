# Django Rest Framework Tutorial

A quick tutorial on how to make a Restful Api with Django RestFramework in 10 minutes!

## Prerequisite

Django is a python framework so ensure that you have a version of python 3 and pip installed. Check this by running:

```bash
python3 --version
pip --version
```

If you don't have python download it by clicking [here](https://www.python.org/ftp/python/3.10.4/python-3.10.4-macos11.pkg). Then re-run the commands above to ensure you have both python and pip installed.

## Setting up the project
I highly recommend that you use [Pycharm](https://www.jetbrains.com/pycharm/) as your text editor for this tutorial. **PyCharm** provides a ton of benefits for building python projects but you could also follow this tutorial manually using your terminal and a text editor of your choice.

### OPTION #1 - Pycharm
Create a new project with the following settings: 
- **Location** - choose the directory in which you want your project to sit and name the directory.
- **Python Interpreter** - select virtualenv, leave the location to the default, ensure the base interpreter is at least a version of python 3 (i.e: Python 3.7 or 3.8)

Finally open the pyCharm terminal screen located at the bottom navigation. *It will be located next to Problems, Version Control and Python*Packages.

**Now you are ready to go!**

### OPTION #2 - Manually creating your project
*If you choose not to install PyCharm*, **that's fine too!** 

First let's navigate to the directory you wish to create the project in using your terminal and make the directory. We'll call this project **django_tutorial**. 

Let's run the following command:

```bash
mkdir django_tutorial
cd django_tutorial
```
As with most python projects we'll need a virtual environment, so let's create one now:
```bash
python3 -m venv venv
```
Now lets activate our virtual enviroment:
```bash
source venv/bin/activate
```
What we've done is create the virtual environment for the project and activated it. If you're not using **PyCharm**, you will need to remember to activate the venv each time via terminal to run your project.

Finally, open up your project in the text editor of your choosing!

**Now you're ready to go!**

## Installation
Let us begin by installing our packages. Run the following command in your terminal:

```bash
pip install django djangorestframework django-cors-headers 
```
Now, let's quickly saves all our packages with the following command:
```
pip freeze > requirements.txt
```
Now we've installed our django packages, let's run the following command in our terminal to create our django project. We'll call this project **django_rest_api**.

```bash
django-admin startproject django_rest_api .
```
This command should have created a directory with the files: **url.py**, **settings.py**, **asgi.py** and **wsgi.py**. You should also have a **manage.py** file in your root directory.

Now we've created our django project, we can start creating our apps. For this tutorial we'll be creating a simple **events** app. So let us run this command:

```bash
python manage.py startapp events
```

Now your folder structure should look like this:

```bash
-- django_rest_api
-- events
-- venv
-- manage.py
```
Now our project is beginning to take shape! 

Next we need to configure our settings file, go to your **django_rest_api** directory and open up your **settings.py** file.

We'll need to add the apps we've installed earlier (through pip) to our **INSTALLED_APPS**. Scroll down to roughly **line 31** of the settings.py file and add  **'corsheaders'**, **'rest_framework'** and **'events'** to the bottom of your **INSTALLED_APPS** array.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # INSERT THESE APPS TO YOUR LIST
    'corsheaders',
    'rest_framework',
    'events'
]
```
Now add the **'corsheaders.middleware.CorsMiddleware'** to enable your cors headers on roughly **line 47** of your **MIDDLEWARE** array in the **settings.py** file.

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # INSERT HERE
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

Finally, add the cors settings to the bottom of the **settings.py** file. 

For this tutorial I will be adding local port **3000**, but depending on which port your frontend client is running on, you can edit the **CORS_ORIGIN_WHITELIST**.

```python
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```
Our configurations are now complete! Let's make our first project migration.

```bash
python manage.py migrate
```
Now lets run our server for the first time! Use the following command to deploy the server:
```bash
python manage.py runserver
```
BOOM! There we go, lets click here and make sure our server is running: [**http://127.0.0.1:8000/**](http://127.0.0.1:8000/). 

If everything is working so far, let's kill the server for now:
- If you're using **windows** it's *Ctrl*+*F4*.
- For **Mac** it's *Ctrl*+*C*.

## Creating our model
Models are the schemas we use for our data in django restframework.

Inside your **events** directory, open up your **models.py** file. Here we'll create our first model with the following fields:

- **Title** - this will be a character field which allows text and requires a max length.
- **Venue** - similar to our title field, but let's increase our max length from 250 to 350.
- **Description** - this will be a text field that accept a string value without needing to declare a limit. 
- **Date** - this is a date field which takes a date.
- **Adults only** - this will be a boolean field, let's add a default value and set it to false.
- **Number of attendees** - this will be an integer field, that will accept values between -2147483648 and 2147483647.

```python
from django.db import models


class Event(models.Model):
    title = models.CharField("Title", max_length=200)
    venue = models.CharField("Venue", max_length=350)
    description = models.TextField("Description")
    date = models.DateField("Date")
    adults_only = models.BooleanField("Adults_Only", default=False)
    number_of_attendees = models.IntegerField("Number_Of_Attendees")
```
Before creating models, make sure you know exactly what fields you want to use. Doing some research into the [different fields](https://www.geeksforgeeks.org/django-model-data-types-and-fields-list/) and what they will prevent issues further down the line.

Now we've written up our model, let's migrate it with the following command.
```python
python manage.py makemigrations
python manage.py migrate
```

## Creating our serializer

Serializing is process of converting objects into JSON.

In your **events** directory let's create a file and call it **serializers.py**.

```bash
touch events/serializers.py
```

Firstly, let's import our Event model from our **models.py** file. We'll then need our ModelSerializers from django rest framework to serialize our model. When serializing a model, we must declare the model and the fields we want serialized.

To serialize all the fields, use the following:

```python
from rest_framework.serializers import ModelSerializer
from .models import Event

class EventsSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
```

To serialize only specific fields, you can declare them in an array like this:

```python
from rest_framework.serializers import ModelSerializer
from .models import Event


class EventsSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title",
            "venue",
            "description",
            "date",
            "number_of_attendees"
        ]
```
Here we've excluded our **adults_only** field from the **Event** model. 

Remember to add a default value or **null=True** or **default_value=True/False** to any field you include in your model but exclude from your serializer. As we've added a **default_value=False** to our **adults_only** field, this will not throw any errors when we make a post request.

Now we have our model and our serializer, let's start creating our the views and routes!

## Creating our views and routes

Views are what our url endpoints return. In this case we want it to return the serialized data from our models. To do this we'll need to import the **api_view**, status and **Response** from django restframework.

This is also  need to import our **Event** model and **EventsSerializer** that we made earlier.

The **EventSerializer** will multiple arguments:

1. The Event objects we wish to pass through, in this case we'll be returning all the event objects with ***Event.objects.all()***
2. It will also take the request type (for this tutorial it will be ***POST*** and ***GET***.
3. We'll also pass **many=True** as an argument. This argument determines whether or not the request will return one or multiple objects, so in this case we want all objects so we will set it to true.

So this is our ***GET*** request:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import Event
from .serializers import EventsSerializer


@api_view(['GET'])
def events_list(request):
    data = Event.objects.all()
    context_args = {'request': request}

    serializer = EventsSerializer(data, context=context_args, many=True)

    return Response(serializer.data, status=HTTP_200_OK)

```
Now we've got our ***GET*** request, let make our ***POST*** request. 

The data will use the same serializer as our ***GET*** request. If you want to pass an object through your post request,

It will take the request data from multiple objects and will check if it's valid: 

- If the data is valid it will be saved and return a **HTTP_201_CREATED**.
- If it will return a **400_BAD_REQUEST** error. 

```python
@api_view(['POST'])
def post_event(request):
    post_data = EventsSerializer(data=request.data, many=True)
    if post_data.is_valid():
        post_data.save()
        return Response(status=HTTP_201_CREATED)

    return Response(post_data.errors, status=HTTP_400_BAD_REQUEST)
```

We're almost done! 

The final step is to create the url endpoints by adding the views we just made to our router. 

Lets go to our **django_rest_api** directory and open up the **urls.py** file.

We can replace the code in that file with the following:

```python
from django.contrib import admin
from django.urls import path
from events.views import events_list, post_event  # OUR IMPORTS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events_list', events_list),  # GET REQUEST
    path('post_event', post_event)  # POST REQUEST
]
```
And that's it! We're all done! 

Lets run our server with:
```bash
python manage.py runserver
```
# Using the endpoints
- To get your events simply use this endpoint [http://127.0.0.1:8000/events_list/](http://127.0.0.1:8000/events_list)
- To post an event, use your frontend or postman and simply post to this endpoint [http://127.0.0.1:8000/post_event](http://127.0.0.1:8000/post_event/)

Now we're done! Quick and painless
