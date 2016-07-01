from django.shortcuts import render, HttpResponse


def welcome(request):
    return HttpResponse("Welcome!")


def index(request):
    return HttpResponse("Index")


def new(request):
    return HttpResponse("new")


def show(request, patient_id):
    return HttpResponse("show %s" % patient_id)
