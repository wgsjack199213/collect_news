from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import hashlib

# try logging
import logging
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    logger.info(str(request))

    return HttpResponse("Hello, world. Zootopia is so great!")


@csrf_exempt
def receive_link(request):
    logger.info(str(request))
    paras = request.GET

    # Decide if the request is from Weixin
    nonce = paras['nonce']
    timestamp = paras['timestamp']
    signature = paras['signature']
    token = 'wangguosai'
    parameters = sorted([nonce, timestamp, token])
    sha1 = hashlib.sha1(''.join(parameters)).hexdigest()
    if not sha1 == signature:
        return HttpResponse("Goodbye!")
    
    logger.info('Welcome here, Wechat!')
    

    return HttpResponse("Hello!")
