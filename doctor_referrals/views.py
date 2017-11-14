# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from . import betterdoctors_api
#from betterdoctors_api import betterdoctor_searchDriver
#from mentalhealth_site.doctor_referrals import betterdoctors_api

def index(request):
    storage = betterdoctors_api.betterdoctor_searchDriver()
    template = loader.get_template("doctor_referrals/index.html")
    context = {
        "storage": storage
    }
    return HttpResponse(template.render(context, request))


