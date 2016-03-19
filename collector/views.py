from django.shortcuts import render
from django.http import HttpResponse

# try logging
import logging
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    logger.info(str(request))
    return HttpResponse("Hello, world. Zootopia is so great!")
