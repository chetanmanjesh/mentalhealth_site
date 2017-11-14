from django.shortcuts import render
from django.http import HttpResponse
import io
import os
#from google.cloud import speech
#from google.cloud.speech import enums
#from google.cloud.speech import types
#import requests
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
from .models import Depression, Stress, Person2
from analyze_tone_from_voice.classifier.classifier import Classifier
import _pickle as pickle


# Create your views here.
class PostUserData(APIView):


    @csrf_exempt
    def post(request, format = None):
        html_response = request.POST
        response_dict = dict(request.POST)
        string = ''
        for item in response_dict:
            string += str(item)+" : "+str(response_dict[item][0])+"\n"
            print(item)
        comment = response_dict['question_2'][0]
        sentiment = get_tone(comment)
        # Classify using Naive Bayes

        classifier = Classifier(model='analyze_tone_from_voice/classifier/model.p')
        naive_bayes_pred = classifier.predict(comment)

        response_dict = {}
        response_dict['comment'] = comment
        ret_str="<head><link rel=\"stylesheet\" href=\"assets/bootstrap/css/bootstrap.min.css\"><link rel=\"stylesheet\" href=\"assets/flat-icon/flaticon.css\"><link rel=\"stylesheet\" href=\"temp/styles/styles.css\"></head>"
        ret_str += '<h1> Analysis of Results </h1>'
        ret_str += '<br>Comment made by user : ' + comment + "</br>"
        ret_str += '<br>Disorder predicted using our predictive model is : <b>'+naive_bayes_pred+'</b></br>'
        if sentiment == 'Sadness':
            response_dict['sentiment'] = 'Depression'
            ret_str += "<br>Disorder predicted using the IBM Tone Analyzer from comment : <b>depression</b> </br><h1>Useful Coping resources</h1>"
            for item in Depression.objects.all():
                response_dict[item.id] = item.link
                ret_str += "<br><a href=\"" + item.link + "\">" + item.link + "</a></br>"

        elif sentiment == 'Anger':
            response_dict['sentiment'] = 'Stress'
            ret_str += "<br>Precited mental disorder from comment : <b>stress</b> </br><h1>Useful Coping resources</h1>"
            for item in Stress.objects.all():
                response_dict[item.id] = item.link
                ret_str += "<br><a href=\"" + item.link + "\">"+item.link+"</a></br>"
        else:
            ret_str +="The user seems okay and not in need of any serious help"

        return HttpResponse(ret_str)
        #return HttpResponse(json.dumps(response_dict), content_type="application/json")
        #return HttpResponse(serializer)

def index(request):
    print('Hello! Welcome to our site!!!')

'''
def index(request):
    text_from_audio = get_text_from_audio()
    print("The type of object is :", request.body)
    tone = get_tone(text_from_audio)
    html_response = "<h1>Welome to Voice Analysis, your predicted tone is:" + tone + "</h1>"
    return HttpResponse(html_response)

def get_text_from_audio():
    os.system(
        "export GOOGLE_APPLICATION_CREDENTIALS='analyze_tone_from_voice/Google_cloud_key/My_First_Project_926af8a5744c.json'")
    os.system(
        'ffmpeg -i analyze_tone_from_voice/input.m4a -acodec libmp3lame -ab 128k analyze_tone_from_voice/input.mp3')
    os.system(
        'sox analyze_tone_from_voice/input.mp3 --rate 16k --bits 16 --channels 1 analyze_tone_from_voice/input.flac')

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = 'analyze_tone_from_voice/input.flac'

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    # for result in response.results:
    text = response.results[0].alternatives[0].transcript
    # print('Transcript: {}'.format(response.results[0].alternatives[0].transcript))
    # remove audio files
    os.system('rm analyze_tone_from_voice/input.mp3')
    os.system('rm analyze_tone_from_voice/input.flac')
    return text
'''

def get_tone(input):
    tone_analyzer = ToneAnalyzerV3(
        username='d2bb67f8-01c6-46f6-86c3-169179260d14',
        password='ipQZoxFok1Jx',
        version='2016-05-19')

    tones = tone_analyzer.tone(text=input)['document_tone']['tone_categories'][0]['tones']

    tone_name = []
    score = []
    for tone in tones:
        tone_name.append(tone['tone_name'])
        score.append(tone['score'])

    predicted_tone = sorted(zip(tone_name, score), key=lambda x: x[1], reverse=True)

    # print ("The emotion you are feeling is  : ", predicted_tone[0][0])
    tone = predicted_tone[0][0]
    return tone
