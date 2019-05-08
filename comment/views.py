from django.shortcuts import render, redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

def comment_update(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    # 数据检查
    if not request.user.is_authenticated:
        return render(request,'error.html',{'message':'Please sign in first','redirect_to': referer})

    text = request.POST.get('text','').strip()
    if text == '':
        return render(request, 'error.html', {'message': 'Please input your comment','redirect_to': referer})

    try:
        content_type = request.POST.get('content_type','')
        object_id = int(request.POST.get('object_id',''))
        # Blog.objects.get(pk = object_id)
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk = object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': "The object doesn't exist",'redirect_to': referer})

    # 检查通过 保存数据
    comment = Comment()
    comment.user = request.user
    comment.text = text

    comment.content_object = model_obj
    comment.save()

    return redirect(referer)


