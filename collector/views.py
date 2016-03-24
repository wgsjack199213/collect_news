from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login
from collector.models import Article
from django.utils import timezone

import hashlib
import xml.etree.ElementTree as ET
import time

# try logging
import logging
logger = logging.getLogger(__name__)

from parse import *


# Create your views here.
def index(request):
    logger.info(str(request))

    """ 
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponse("Hello, world. Zootopia is so great!")
        else:
            # Return a 'disabled account' error message
            pass         
    else:
        # Return an 'invalid login' error message.
        pass
    """

    return HttpResponse("Hello, world. Zootopia is so great!")
    #return HttpResponse("Sorry=___________=")


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
    to_user_name = xml_tree.find('ToUserName').text
    create_time = xml_tree.find('CreateTime').text
    logger.info(create_time + ' ' + str(content) + ' ' + from_user_name)

    # Parse the url and collect the data
    if get_article(content, from_user_name, to_user_name, create_time) == -1:
        message = 'New url cannot be parsed. But we have recorded it!'
    else:
        message = 'Success!'

    # Generate response
    response_xml = respond(message, from_user_name, to_user_name, xml_tree)
    return HttpResponse(response_xml)

def respond(message, from_user_name, to_user_name, xml_tree):
    #return HttpResponse("")
    xml_tree.find('Content').text = message
    xml_tree.find('FromUserName').text = to_user_name
    xml_tree.find('ToUserName').text = from_user_name
    #xml_tree.find('CreateTime').text = str(int(time.time() - 10))
    response_xml = ET.tostring(xml_tree)
    return response_xml


def get_article(url, from_user_name, to_user_name, create_time):
    article = parse_url(url)
    if article == -1:
        return -1   
 
    logger.info(str(article))

    a = Article(source=article['source'], url=article['url'], \
                content=article['content'], title=article['title'], \
                title2=article['title2'], timestamp=int(time.time()), \
                pub_date=timezone.now())
    a.save()

    return
    
     
