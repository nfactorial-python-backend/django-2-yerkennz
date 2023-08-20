from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import News, Comment
from django.views import View
from .forms import NewsForm

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
    
    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(content=content, news=news)
        latest_comment = Comment.objects.latest('created_at')
        return redirect(reverse('news:detail', args=[news_id]))
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

class NewsEditView(View):
    def get(self, request, news_id):
        try :
            news = News.objects.get(pk=news_id)
        except News.DoesNotExist:
            raise Http404("Not Found")
        form = NewsForm(instance=news)
        return render(request, "news/news_edit.html", {"form": form, "news_id": news_id})
    
    def post(self, request, news_id):
        try :
            news = News.objects.get(pk=news_id)
        except News.DoesNotExist:
            raise Http404("Not Found")
        
        form = NewsForm(request.POST, instance=news)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))