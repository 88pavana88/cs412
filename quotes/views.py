from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.
quotes = [
    "Life is not a waste of time, time is not a waste of life. So let's not waste any time, get wasted and have the time of our lives.",
    "This is for everyone going through tough times, been there done that, but everyday above ground is a great day, remember that.",
    "If you don't know where you're from, you don't know where you're going, and if you don't stand for something, you'll fall for anything."
]

images = [
    "pitbull1.JPEG",
    "pitbull2.JPEG",
    "pitbull3.JPEG"
]

def quote(request):
    random_quote = random.randint(0, len(quotes) - 1)
    random_image = random.randint(0, len(quotes) - 1)
    context = {
        'quote': quotes[random_quote],
        'image': images[random_image]
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    context = {
        'quotes': quotes,  
        'images': images  
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    return render(request, 'quotes/about.html')