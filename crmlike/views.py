from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomerProfile, Task, StatusTask
from .forms import LoginForm, RegistrationForm, ChangeForm


class BasePage(TemplateView):
    template_name = 'index.html'


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('base_page')

    def form_valid(self, form):
        user = CustomerProfile.objects.filter(
            username='_'.join([form.data['name'], form.data['surname']])).first()
        if user is not None and user.check_password(form.data['password']):
            login(request=self.request, user=user)
            return super().form_valid(form)
        else:
            if user is not None:
                form.add_error(field=None, error="Ошибка валидации.")
            else:
                form.add_error(field=None, error="Пользователь не зарегистрирован.")
            return super().form_invalid(form)


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('base_page')


class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('base_page')

    def form_valid(self, form):
        username = '_'.join([form.data['name'], form.data['surname']])
        user = CustomerProfile.objects.filter(username=username).first()
        if user is None and form.data['password1'] == form.data['password2']:
            new_user = CustomerProfile(first_name=form.data['name'], last_name=form.data['surname'])
            new_user.set_password(form.data['password1'])
            new_user.save()
            login(request=self.request, user=new_user)
            return super().form_valid(form)
        else:
            form.add_error(field=None, error="Пользователь с таким именем уже существует.")
            return super().form_invalid(form)


class ChangeView(LoginRequiredMixin, FormView):
    template_name = 'change.html'
    form_class = ChangeForm
    success_url = reverse_lazy('base_page')

    def form_valid(self, form):
        exist_user = CustomerProfile.objects.get(pk=self.request.user.pk)
        new_name = form.data['first_name'] or exist_user.first_name
        new_surname = form.data['last_name'] or exist_user.last_name
        new_avatar = form.cleaned_data['customer_avatar'] or exist_user.customer_avatar
        new_username = '_'.join([new_name, new_surname])
        if new_avatar or (new_username != exist_user.username and (
                CustomerProfile.objects.filter(username=new_username).first() is None)):
            exist_user.first_name = new_name
            exist_user.last_name = new_surname
            exist_user.customer_avatar = new_avatar
            exist_user.save()
            return super().form_valid(form)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasklist.html'
    context_object_name = 'tasks'
    paginate_by = 4
    queryset = Task.objects.all()

    def get_queryset(self):
        try:
            status_filter = int(self.request.GET['filter'])
            return Task.objects.filter(status_id=status_filter).filter(performer=self.request.user)
        except Exception as err:
            return Task.objects.filter(performer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            status_filter = int(self.request.GET['filter'])
            context['status_filter'] = status_filter
        except Exception as err:
            pass
        context['filter_data'] = StatusTask.objects.all()
        return context
