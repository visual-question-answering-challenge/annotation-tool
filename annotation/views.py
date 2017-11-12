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
from .models import Image, Annotation


@login_required
def index(request):

    list_annotated_images = [
        annot.fk_image.id for annot in Annotation.objects.all()]
    images = Image.objects.exclude(id__in=list_annotated_images)

    if len(images) == 0:
        return HttpResponse("<h1>THERE IS NO MORE IMAGES!</h1>")

    img_url = static(images[0])

    context = {
        'img_path': img_url
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


@csrf_protect
def receive_query_search(request):
    if request.is_ajax() and request.POST:

        question_list = request.POST.get("questionList").split(";")
        question_list = [el.strip() for el in question_list]
        img_path = request.POST.get("imgPath").replace("/static/", "").strip()

        user_id = request.user.id
        user = User.objects.get(id=user_id)
        image = Image.objects.get(img_path=img_path)

        for question in question_list:
            annotation = Annotation()
            annotation.fk_user = user
            annotation.fk_image = image
            annotation.question_text = question
            annotation.save()

        list_annotated_images = [
            annot.fk_image.id for annot in Annotation.objects.all()]
        images = Image.objects.exclude(id__in=list_annotated_images)

        if len(images) == 0:
            return HttpResponse("<h1>THERE IS NO MORE IMAGES!</h1>")
        else:
            img_url = static(images[0])
            context = {
                'img_path': img_url,
            }
            template = loader.get_template('form.html')
            return HttpResponse(template.render(context, request))
