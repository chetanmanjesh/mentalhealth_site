from django.shortcuts import render
from django.http import HttpResponse
from os import  system

import io
import os


def index(request):

    return render(request, "home/accept_input_from_user.html",{})