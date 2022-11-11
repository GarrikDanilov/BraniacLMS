from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from mainapp.models import News


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'


class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = News.objects.filter(deleted=False)
        return context


class NewsDetail(TemplateView):
    template_name = 'mainapp/news_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        context['news_object'] = get_object_or_404(News, pk=pk)
        return context


class NewsWithPaginatorView(NewsView):

    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        context["page_num"] = page
        return context
