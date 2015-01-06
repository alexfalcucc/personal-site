# coding: utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from resume.core.models import Article, Tag
from resume.core.forms import ArticleForm, ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decouple import config
import twitter
from django.conf import settings
from django.template import Context
from django.http import HttpResponse


def home(request):
    api = twitter.Api(consumer_key=config('consumer_key'),
                      consumer_secret=config('consumer_secret'),
                      access_token_key=config('access_token_key'),
                      access_token_secret=config('access_token_secret')
                      )
    statuses = api.GetUserTimeline(screen_name='AlexFalcucci')
    posts = [s.text for s in statuses]
    all_articles = Article.get_published()

    return render(request, 'core/index.html', {'posts': posts[0:10],
                                               'articles': all_articles[0:10],
                                               'form': ContactForm(request.POST
                                                                   or None)})


def _articles(request, articles):
    paginator = Paginator(articles, 2)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()
    return render(request, 'core/blog/all_articles.html', {
        'articles': articles,
        'popular_tags': popular_tags
    })


def all_articles(request):
    all_articles = Article.get_published()
    return _articles(request, all_articles)


def article(request, slug):
    article = get_object_or_404(Article, slug=slug, status=Article.PUBLISHED)
    all_articles = Article.get_published()
    for i, a in enumerate(all_articles):
        if a == article:
            indice_pre = i - 1
            indice_next = i + 1
    previous_post = all_articles[indice_pre] if indice_pre >= 0 else None
    next_post = all_articles[indice_next] if indice_next != len(
        all_articles) else None
    context = {
        'article': article,
        'articles': all_articles[0:3],
        'previous_post': previous_post,
        'next_post': next_post,
    }
    return render(request, 'core/blog/article.html', context)


def write(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        print request.FILES
        if form.is_valid():
            print 'AÇLSDKFJÇALSKJDFAÇLKFDJAÇLFKJASÇD'
            article = Article()
            article.create_user = request.user
            article.title = request.POST['title']
            article.content = request.POST['content']
            if request.FILES['picture'] is not None:
                article.picture = request.FILES['picture']
            article.url_download = request.POST['url_download']
            article.url_preview = request.POST['url_preview']
            article.url_github = request.POST['url_github']
            status = request.POST['status']
            if status in [Article.PUBLISHED, Article.DRAFT]:
                article.status = request.POST['status']
            article.save()
            tags = request.POST['tags']
            article.create_tags(tags)
            return redirect('/')
    else:
        form = ArticleForm()
    return render(request, 'core/blog/write.html', {'form': form})


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid() and request.is_ajax():
        save_it = form.save(commit=False)
        save_it.save()
        subject = 'Hello my friend {username}, do you called me? =)'.format(
            username=save_it.name)
        from_email = settings.EMAIL_HOST_USER
        to = save_it.email
        text_content = 'Olá {username}, do you called me?'.format(
            username=save_it.name)
        c = Context({
            'user': save_it.name, 'github': 'https://github.com/alexfalcucc',
            'linkedin': 'https://www.linkedin.com/in/alexfalcucci'
        })
        html_content = render_to_string(
            'core/emails/welcome.html', c
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse("success")
    return render(request, 'core/index.html', {'form': form})
