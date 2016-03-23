from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import hashlib
import xml.etree.ElementTree as ET

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
    try:
        nonce = paras['nonce']
        timestamp = paras['timestamp']
        signature = paras['signature']
    except:
        return HttpResponse("Goodbye!")
    token = 'wangguosai'
    parameters = sorted([nonce, timestamp, token])
    sha1 = hashlib.sha1(''.join(parameters)).hexdigest()
    if not sha1 == signature:
        return HttpResponse("Goodbye!")
    
    logger.info('Welcome here, Wechat!')
    
    raw_data = request.body
    #logger.info(str(raw_data))
    xml_tree = ET.fromstring(raw_data)
    content = xml_tree.find('Content').text
    from_user_name = xml_tree.find('FromUserName').text
    create_time = xml_tree.find('CreateTime').text
    logger.info(str(content) + ' ' + create_time + ' ' + from_user_name)

    return HttpResponse("")
