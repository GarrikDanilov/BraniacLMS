# from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


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
        context['object_list'] = [
            {
                'title': 'Новость 1',
                'date': '2021-04-29 20-50-26',
                'preview': 'Предварительное описание новости 1'
            }, {
                'title': 'Новость 2',
                'date': '2021-04-28 20-50-26',
                'preview': 'Предварительное описание новости 2'
            }, {
                'title': 'Новость 3',
                'date': '2021-04-27 20-50-26',
                'preview': 'Предварительное описание новости 3'
            }, {
                'title': 'Новость 4',
                'date': '2021-04-26 20-50-26',
                'preview': 'Предварительное описание новости 4'
            }, {
                'title': 'Новость 5',
                'date': '2021-04-25 20-50-26',
                'preview': 'Предварительное описание новости 5'
            }
        ]
        return context


class NewsWithPaginatorView(NewsView):

    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        context["page_num"] = page
        return context
