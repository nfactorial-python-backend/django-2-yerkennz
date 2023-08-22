from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import News, Comment
from django.views import View
from .forms import NewsForm, SignUpForm, CommentsForm
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required

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
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.news = news
            comment.save()
            return HttpResponseRedirect(reverse("news:index"))
    else:
        CommentsForm()
        # content = request.POST['content']
        # Comment.objects.create(content=content, news=news)
        # latest_comment = Comment.objects.latest('created_at')
        # return redirect(reverse('news:detail', args=[news_id]))
    context = {"news": news}
    return render(request, "news/detail.html",context)


@login_required(login_url="/login/")
@permission_required("news.add_news", login_url="/login/")
def add(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return HttpResponseRedirect(reverse("news:index"))
    else:
        form = NewsForm()
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
        
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            group = Group.objects.get(name="default")
            group.user_set.add(user)

            login(request, user)
            return redirect(reverse("news:index"))
    else:
        form = SignUpForm()

    return render(request, "registration/sign_up.html", {"form": form})

def delete_news(request, news_id):
    try :
        news = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        raise Http404("Not Found")
    if request.method == "POST":
        if request.user == news.author or request.user.has_perm(
            "news.delete_news"
        ):
            news.delete()
    return redirect(reverse("news:index"))

def delete_comment(request, news_id, comment_id):
    try :
        news = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        raise Http404("Not Found")
    
    try :
        comment = Comment.objects.get(pk=comment_id, news=news)
    except Comment.DoesNotExist:
        raise Http404("Not Found")
    
    if request.method == "POST":
        if request.user == comment.author or request.user.has_perm(
            "news.delete_comment"
        ):
            comment.delete()
    return redirect(reverse("news:index"))