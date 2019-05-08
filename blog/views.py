from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from .models import Blog, BlogType
from comment.models import Comment
from read_count.utils import read_count_once_read


# Create your views here.

def get_common_list(request, blogs_all_list):
    # 每五篇进行分页
    paginator = Paginator(blogs_all_list, 5)
    # 获取url的页面参数（GET请求）
    page_num = request.GET.get('page', 1)  # str
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    # 获取当前页码前后各两页的页码范围
    page_range = list(range(max(current_page_num - 2, 1), min(paginator.num_pages, current_page_num + 2) + 1))

    # 页码省略标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}

    context['blogs'] = blogs_all_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')

    return context

def blog_list(request):

    blogs_all_list = Blog.objects.all()

    context = get_common_list(request, blogs_all_list)

    return render(request,'blog/blog_list.html', context)

def blogs_with_type(request, blog_type_pk):

    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)

    context = get_common_list(request, blogs_all_list)

    context['blog_type'] = blog_type

    return render(request,'blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month):

    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)

    context = get_common_list(request, blogs_all_list)

    context['blog_with_date'] = '%s-%s' % (year, month)
    return  render(request,'blog/blogs_with_date.html', context)


def blog_detail(request, blog_pk):

    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_count_once_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk)

    context = {}
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['comments'] = comments

    response = render(request,'blog/blog_detail.html',context)
    response.set_cookie(read_cookie_key,'true', max_age=300) #阅读cookie标记

    return response

