from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.template import RequestContext
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse


import numpy as np

from django.contrib.auth.models import User
from .models import Image, Annotation, PoolItem


@login_required
def index(request):

    user_id = request.user.id

    # getting the first pool_item to be annatated
    image_pool = PoolItem.objects.filter(is_done=False).filter(user=user_id)

    if image_pool.count() == 0:
        return HttpResponse("<h1>THERE IS NO MORE IMAGES!</h1>")

    # get the first element on pool without image's annotation
    pool_item = image_pool[0]

    # getting the total number of image to annotated
    total_num_images = PoolItem.objects.filter(user=user_id).count()

    # getting the total number of image annotated
    img_annotated = PoolItem.objects.filter(
        is_done=True).filter(user=user_id).count()

    pool_item_id = pool_item.id
    img_path = static(pool_item.image.img_path)
    num_img_to_finish = total_num_images - img_annotated

    context = {
        'img_path': img_path,
        'pool_item_id': pool_item_id,
        'num_img_to_finish': num_img_to_finish
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


@csrf_protect
def receive_query_search(request):
    if request.is_ajax() and request.POST:

        # get post parameters
        img_path = request.POST.get("imgPath").replace("/static/", "").strip()
        pool_id = request.POST.get("poolItemId").strip()
        question_list = request.POST.get("questionList").split(";")
        question_list = [el.strip() for el in question_list]

        user_id = request.user.id

        # update pool item to done
        pool_item = PoolItem.objects.get(id=pool_id)
        pool_item.is_done = True
        pool_item.save()

        # store the questions
        for question in question_list:
            annotation = Annotation()
            annotation.pool_item = pool_item
            annotation.question_text = question
            annotation.save()

        # getting the first pool_item to be annotated
        image_pool = PoolItem.objects.filter(
            is_done=False).filter(user=user_id)

        # if there is no more images to annotate
        if image_pool.count() == 0:
            return HttpResponse("<h1>THERE IS NO MORE IMAGES!</h1>")

        # get the first element on pool without image's annotation
        pool_item = image_pool[0]

        # getting the total number of image to annotated
        total_num_images = PoolItem.objects.filter(user=user_id).count()

        # getting the total number of image annotated
        img_annotated = PoolItem.objects.filter(
            is_done=True).filter(user=user_id).count()

        pool_item_id = pool_item.id
        img_path = static(pool_item.image.img_path)
        num_img_to_finish = total_num_images - img_annotated

        context = {
            'img_path': img_path,
            'pool_item_id': pool_item_id,
            'num_img_to_finish': num_img_to_finish
        }
        
        template = loader.get_template('form.html')
        return HttpResponse(template.render(context, request))

    else:
        return HttpResponse("something wrong happened!")
