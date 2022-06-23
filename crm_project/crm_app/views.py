from django.contrib.auth import login, authenticate
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import *
from .models import *


class RegisterView(generic.View):
    form = RegistrationForm

    def get(self, request, form=form):
        return render(request, 'crm_app/registration.html', context={'form': form})

    def post(self, request, form=form):
        form = form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(username, raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home_page')
        return render(request, 'crm_app/registration.html', context={'form': form})


class UserLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'crm_app/login.html'

    def get_success_url(self):
        return reverse('home_page')


class HomePageView(generic.View):
    def get(self, request):
        return render(request, 'crm_app/home_page.html')


class UserLogoutView(LogoutView):
    next_page = 'login'


class LeadCreationView(generic.View):
    def get(self, request):
        form = LeadCreationForm()
        return render(request, 'crm_app/lead_creation.html', {'form': form})

    def post(self, request):
        form = LeadCreationForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            product_name = Product.objects.get(pk=form_data.get('product_FK')).values('product_name')
            web_name = Web.objects.get(pk=form_data.get('web_FK')).values('web_name')
            lead_cost = Offer.objects.get(product=form_data.get('product_FK'),
                                          web=form_data.get('web_FK')).values('click_cost')
            new_lead = Lead.objects.create(
                offer_FK=form_data.get('offer_fk'),
                contact_phone=form_data.get('contact_phone'),
                customer_first_name=form_data.get('customer_first_name'),
                customer_last_name=form_data.get('customer_last_name'),
                product_FK=form_data.get('product_FK'),
                product_name=product_name,
                web_FK=form_data.get('web_FK'),
                web_name=web_name,
                lead_cost=lead_cost
            )
            return redirect(reverse('lead_detail', kwargs={'id': new_lead.id}))
        return render(request, 'crm_app/lead_creation.html', {'form': form})


class LeadDetailView(generic.DetailView):
    model = Lead
    template_name = 'crm_app/lead_detail'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return Lead.objects.select_related('order').get(pk=self.kwargs.get('id'))


class LeadListView(generic.ListView):
    model = Lead
    template_name = ''


class LeadToOrderCreationView():
    pass


class OrderDetailView():
    pass


class OrderListView():
    pass


class WebCreationView(generic.CreateView):
    model = Web
    form_class = WebCreationForm
    template_name = 'crm_app/web_creation.html'

    def get_initial(self, *args, **kwargs):
        initial = super(WebCreationView, self).get_initial(**kwargs)
        initial['web_api_key'] = BaseUserManager().make_random_password(15)
        return initial

    def get_success_url(self):
        return reverse_lazy('web_detail', kwargs={'id': self.object.pk})


class WebDetailView(generic.DetailView):
    model = Web
    pk_url_kwarg = 'id'
    query_pk_and_slug = True
    template_name = 'crm_app/web_detail.html'


class WebListView(generic.ListView):
    model = Web
    context_object_name = 'webs'
    template_name = 'crm_app/web-list.html'

    def get_queryset(self):
        return Web.objects.all().order_by('web_name')


class PaymentsCreationView():
    pass


class PaymentsDetailView():
    pass


class PaymentsListView():
    pass


class ProductCategoryCreationView(generic.CreateView):
    form_class = ProductCategoryCreationForm
    template_name = 'crm_app/product_category_creation.html'

    def get_success_url(self):
        return reverse_lazy('product_category_detail', kwargs={'id': self.object.pk})


class ProductCategoryListView(generic.ListView):
    model = ProductCategory
    template_name = 'crm_app/product_category_list.html'

    def get_queryset(self):
        return ProductCategory.objects.prefetch_related('product_set').all()


class ProductCategoryDetailView(generic.DetailView):
    model = ProductCategory
    template_name = 'crm_app/product_category_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return ProductCategory.objects.prefetch_related('product_set').get(pk=self.kwargs.get('id'))


class ProductCreationView(generic.CreateView):
    model = Product
    form_class = ProductCreationForm
    template_name = 'crm_app/product_creation.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'id': self.object.pk})


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'crm_app/product_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True


class ProductListView(generic.ListView):
    model = Product
    template_name = 'crm_app/product_list.html'

    def get_queryset(self):
        return Product.objects.select_related('product_category').all()
