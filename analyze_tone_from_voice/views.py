from django.shortcuts import render
from django.http import HttpResponse
import io
import os
import json
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Depression, Stress, ADHD, PTSD
from analyze_tone_from_voice.classifier.classifier import Classifier
import _pickle as pickle



# Create your views here.
class PostUserData(APIView):


    @csrf_exempt
    def post(request, format = None):
        response_dict = dict(request.POST)
        string = ''
        for item in response_dict:
            string += str(item)+" : "+str(response_dict[item][0])+"\n"
            print(item)
        comment = response_dict['question_2'][0]
        # Classify using Naive Bayes

        classifier = Classifier(model='analyze_tone_from_voice/classifier/model.p')
        naive_bayes_pred = classifier.predict(comment)
        response_dict = {}
        response_dict['comment'] = comment
        ret_str="<head><link rel=\"stylesheet\" href=\"assets/bootstrap/css/bootstrap.min.css\"><link rel=\"stylesheet\" href=\"assets/flat-icon/flaticon.css\"><link rel=\"stylesheet\" href=\"temp/styles/styles.css\"></head>"
        ret_str += '<h1> Analysis of Results </h1>'
        ret_str += '<br>Comment made by user : <b>\"' + comment + '\"</b></br>'

        if naive_bayes_pred == 'depression':
            response_dict['sentiment'] = 'Depression'
            ret_str += '<br>Disorder predicted using our predictive model is : <b>' + response_dict['sentiment'] + '</b></br>'
            ret_str += '<h3>Here are some links to resouces that could help you:</h3>'
            for item in Depression.objects.all():
                response_dict[item.id] = item.link
                ret_str += "<br><a href=\"" + item.link + "\">" + item.link + "</a></br>"

        elif naive_bayes_pred == 'stress':
            response_dict['sentiment'] = 'Stress'
            ret_str += '<br>Disorder predicted using our predictive model is : <b>' + response_dict['sentiment'] + '</b></br>'
            ret_str += '<h3>Here are some links to resouces that could help you:</h3>'
            for item in Stress.objects.all():
                response_dict[item.id] = item.link
                ret_str += "<br><a href=\"" + item.link + "\">"+item.link+"</a></br>"


        if naive_bayes_pred == 'adhd':
            response_dict['sentiment'] = 'ADHD'
            ret_str += '<br>Disorder predicted using our predictive model is : <b>' + response_dict['sentiment'] + '</b></br>'
            ret_str += '<h3>Here are some links to resouces that could help you:</h3>'
            for item in ADHD.objects.all():
                response_dict[item.id] = item.link
                ret_str += "<br><a href=\"" + item.link + "\">" + item.link + "</a></br>"

        elif naive_bayes_pred == 'ptsd':
            response_dict['sentiment'] = 'PTSD'
            ret_str += '<br>Disorder predicted using our predictive model is : <b>' + response_dict['sentiment'] + '</b></br>'
            ret_str += '<h3>Here are some links to resouces that could help you:</h3>'
            for item in PTSD.objects.all():
                response_dict[item.id] = item.link
                ret_str += "<br><a href=\"" + item.link + "\">"+item.link+"</a></br>"

        return HttpResponse(ret_str)

def index(request):
    print('Hello! Welcome to our site!!!')


