from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.template.defaultfilters import slugify
from cloudinary.models import CloudinaryField
import markdown

# Create your models here.


class Article(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Rascunho'),
        (PUBLISHED, 'Publicado'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    content = models.TextField(max_length=4000)
    picture = CloudinaryField(_(u'foto'), blank=True, null=True)
    url_download = models.CharField(_(u'download link'), max_length=100,
                                    blank=True, null=True)
    url_preview = models.CharField(_(u'preview link'), max_length=100,
                                   blank=True, null=True)
    url_github = models.CharField(_(u'github link'), max_length=100,
                                  blank=True, null=True)
    status = models.TextField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(
        User, null=True, blank=True, related_name="+")

    class Meta:
        verbose_name = _("Artigo")
        verbose_name_plural = _("Artigos")
        ordering = ("-create_date",)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Article, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "{0} {1}".format(self.pk, self.title.lower())
            self.slug = slugify(slug_str)
        super(Article, self).save(*args, **kwargs)

    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')

    @staticmethod
    def get_published():
        articles = Article.objects.filter(status=Article.PUBLISHED)
        return articles

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(
                    tag=tag.lower(), article=self)

    def get_tags(self):
        return Tag.objects.filter(article=self)

    def get_summary(self):
        if len(self.content) > 255:
            return u'(0)...'.format(self.content[:255])
        else:
            return self.content

    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode="escape")


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    article = models.ForeignKey(Article)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        unique_together = (('tag', 'article'),)
        index_together = [['tag', 'article'], ]

    def __unicode__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for tag in tags:
            if tag.article.status == Article.PUBLISHED:
                if tag.tag in count:
                    count[tag.tag] = count[tag.tag] + 1
                else:
                    count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


class Contact(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField(max_length=500, verbose_name='Mensagem')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Mensagem para " + str(self.email)
