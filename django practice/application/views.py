from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.

def sayhello ( request ) :
    print("execute sayhello")
    return HttpResponse( "Hello, I am bobo." ) 


def hello2 ( request, username ):
    print("execute hello2")
    return HttpResponse( "Hello " + username )

def hello3 ( request, username ):
    print("execute hello3")
    now = datetime.now()
    return render( request, "hello3.html", locals() )

def hello4 ( request, username ) :
    print("execute hello4")
    now = datetime.now()
    return render( request, "hello4.html", locals() )