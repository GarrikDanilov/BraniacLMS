from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView, View
from mainapp.models import News, Course, Lesson, CourseTeachers, CourseFeedback
from django.template.loader import render_to_string
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from mainapp.forms import CourseFeedbackForm, MailFeedbackForm
from django.core.cache import cache
from config.settings import LOG_FILE
from mainapp.tasks import send_feedback_mail


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = MailFeedbackForm(user=self.request.user)
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(
             f"mail_feedback_lock_{self.request.user.pk}"
            )
        if not cache_lock_flag:
            cache.set(
             f"mail_feedback_lock_{self.request.user.pk}",
             "lock", timeout=300,
            )
            messages.add_message(
             self.request, messages.INFO, _("Message sended")
            )
            send_feedback_mail.delay(
             {
                "user_id": self.request.POST.get("user_id"),
                "message": self.request.POST.get("message"),
             }
            )
        else:
            messages.add_message(
             self.request,
             messages.WARNING,
             _("You can send only one message per 5 minutes"),
            )
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


class CoursesListView(ListView):
    template_name = 'mainapp/courses_list.html'
    model = Course


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsView(ListView):
    model = News
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsDetailView(DetailView):
    model = News


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = "__all__"
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = "__all__"
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


class NewsWithPaginatorView(NewsView):

    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        context["page_num"] = page
        return context


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(Course, pk=pk)
        context["lessons"] = Lesson.objects.filter(course=context["course_object"])
        context["teachers"] = CourseTeachers.objects.filter(
         course=context["course_object"])

        if not self.request.user.is_anonymous:
            if not CourseFeedback.objects.filter(
             course=context["course_object"], user=self.request.user).count():
                context["feedback_form"] = CourseFeedbackForm(
                 course=context["course_object"], user=self.request.user)

        cached_feedback_key = f"feedback_list_{pk}"
        cached_feedback = cache.get(cached_feedback_key)
        if not cached_feedback:
            context["feedback_list"] = CourseFeedback.objects.filter(
             course=context["course_object"]
            ).order_by("-created", "-rating")[:5].select_related()
            cache.set(
             cached_feedback_key, context["feedback_list"], timeout=300
            )
        else:
            context["feedback_list"] = cached_feedback

        return context


class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string(
         "mainapp/includes/inc_feedback_card.html", context={"item": self.object})
        return JsonResponse({"card": rendered_card})


class LogView(UserPassesTestMixin, TemplateView):
    template_name = 'mainapp/logs.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        log_lines = []

        with open(LOG_FILE) as file_logs:
            for idx, line in enumerate(file_logs):
                if idx == 1000:
                    break
                log_lines.insert(0, line)

            context_data['logs'] = ''.join(log_lines)
        return context_data


class LogDownloadView(UserPassesTestMixin, View):
    
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(LOG_FILE, 'rb'))
