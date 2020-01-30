from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def sayhello ( request ) :
    print("execute sayhello")
    return HttpResponse("Hello, I am bobo.")


def hello2 ( request, username ):
    print("execute hello")
    return HttpResponse("Hello " + username)
