from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import News 

# Create your views here.
def index(request):
    news = News.objects.order_by("created_at").all()
    context = {"news": news}
    return render(request, "news/index.html", context)

def detail(request, news_id):
    try :
        news = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        raise Http404("Not Found")
    
    context = {"news": news}
    return render(request, "news/detail.html",context)

def add(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        News.objects.create(title=title, content=content)
        latest_news = News.objects.latest('created_at')
        return redirect(reverse('news:detail', args=[latest_news.pk]))
    return render(request, 'news/add.html')