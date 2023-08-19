from django.test import TestCase
from .models import News, Comment
from django.urls import reverse

# Create your tests here.
class NewsModelTests(TestCase):
    def test_has_comments_true(self):
        news = News.objects.create(title="Test case", content='test content')
        comment = Comment.objects.create(content="comment test", news=news)
        self.assertTrue(news.has_comments())

    def test_has_comment_false(self):
        news = News.objects.create(title="Test case", content='test content')
        self.assertFalse(news.has_comments())

class NewsViewTests(TestCase):
    def test_index(self):
        nw1 = News.objects.create(title="Test1", content='test1')
        nw2 = News.objects.create(title="Test2", content='test2')
        nw3 = News.objects.create(title="Test3", content='test3')

        nw1.save()
        nw2.save()
        nw3.save()

        response = self.client.get(reverse("news:index"))
        self.assertQuerysetEqual([nw1,nw2,nw3], response.context["news"])

    def test_detail(self):
        nw = News.objects.create(title="Test1", content="test1")
        nw.save()
        response = self.client.get(reverse("news:detail", args=(nw.id,)))
        self.assertEqual(nw,response.context['news'])
    
    def test_detail_comment(self):
        nw = News.objects.create(title="Test1", content="test1")
        cm1 = Comment.objects.create(content="test1", news=nw)
        cm2 = Comment.objects.create(content="test2", news=nw)
        cm3 = Comment.objects.create(content="test3", news=nw)

        nw.save()
        response = self.client.get(reverse("news:detail", args=(nw.id,)))
        cm = response.context['news'].comment_set.all()
        self.assertQuerysetEqual([cm1,cm2,cm3], cm)

