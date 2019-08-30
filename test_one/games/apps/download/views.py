from django.shortcuts import render
from .models import GameDetails,GameClass,Publishers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.
#
# def classify(request):
#     return render(request, 'download/download_list.html')

# def download_list(request):
#     game_list = GameDetails.objects.all()
#     return render(request, 'download/download_list.html',{"game_list":game_list})

def Download_list(request):
    contact_list = GameDetails.objects.all()
    paginator = Paginator(contact_list, 16) # Show 25 contacts per page
    gameclass = GameClass.objects.all()
    # 判断
    page = request.GET.get('page')

    # 实现搜索功能
    if request.GET.get('search') is not None:
        search = request.GET.get('search')
        ##通过django Q 来实现多字段搜索
        results=GameDetails.objects.filter(Q(game_name__contains=search)|Q(gameclass__type_name__contains=search))
        paginator = Paginator(results,16)


    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    kwgs = {
        "contacts":contacts,
    }
    return render(request, 'download/download_list.html', locals())


def Download_classify(request):
    gameclass = GameClass.objects.all()
    kwgs = {
        'gameclass':gameclass
    }
    return render(request,'download/download_classify.html',locals())



@login_required
# class Download_details(LoginRequiredMixin, DetailView):
def Download_details(request, id):
    download_details = GameDetails.objects.get(id=id)
    picture_max_list = eval(download_details.picture_max)
    picture_min_list = eval(download_details.picture_min)
    tag_list = eval(download_details.tag)
    kwgs = {
        'download_details': download_details,
        'picture_max_list': picture_max_list,
        'picture_min_list': picture_min_list,
        'tag_list':tag_list,
    }
    # print(download_details.picture_min)
    return render(request, 'download/download_details.html', kwgs)


@login_required
def Sort(request,pk):
    if pk == 100:
        # games_lsit = GameDetails.objects.filter(gameclass=pk)
        games_lsit = GameDetails.objects.all()
    else:
        # games_lsit = GameDetails.objects.all()
        games_lsit = GameDetails.objects.filter(gameclass=pk)
    # print(games_lsit)
    gameclass = GameClass.objects.all()
    paginator = Paginator(games_lsit, 16)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    kwgs = {
        "contacts":contacts,
    }
    return render(request, 'download/download_list.html', locals())