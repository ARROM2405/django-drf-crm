from django.contrib.auth import login, authenticate, mixins
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.db import transaction

from .forms import *
from .models import *

MENU_ALL = [
    {'title': 'Main', 'url_address': 'home_page'},
    {'title': 'Product categories', 'url_address': 'product_category_list'},
    {'title': 'Products', 'url_address': 'products_list'}
]

MENU_OPERATORS = [
    {'title': 'Leads', 'url_address': 'lead_list'},
    {'title': 'Orders', 'url_address': 'order_list'},
]


MENU_PAYMENTS_EXECUTIVE = [
    {'title': 'Webs', 'url_address': 'web_list'},
    {'title': 'Offers', 'url_address': 'offer_list'},
    {'title': 'Payments', 'url_address': 'payment_list'}
]

MENU_ADMIN = [
    {'title': 'Users', 'url_address': 'profile_list'}
]


class RegisterView(generic.View):
    form = RegistrationForm

    def get(self, request, form=form):
        return render(request, 'crm_app/registration.html', context={'form': form})

    def post(self, request, form=form):
        form = form(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            Profile.objects.create(
                user=user,
                role='Test role',
            )
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home_page')
        return render(request, 'crm_app/registration.html', context={'form': form})


class UserLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'crm_app/login.html'

    def get_success_url(self):
        return reverse('home_page')


class HomePageView(mixins.LoginRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'crm_app/home_page.html')


class UserLogoutView(LogoutView):
    next_page = 'login'


class LeadCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.create_lead'
    model = Lead
    form_class = LeadCreationForm
    template_name = 'crm_app/lead_creation.html'

    def form_valid(self, form):
        offer = form.cleaned_data.get('offer_FK')
        form.instance.lead_cost = offer.click_cost
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lead_list')


class LeadDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_lead'
    permission_denied_message = 'Permission is required!!!!'
    model = Lead
    template_name = 'crm_app/lead_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True


class LeadListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_lead'
    model = Lead
    template_name = 'crm_app/lead_list.html'

    def get_queryset(self):
        return Lead.objects.select_related('offer_FK').all()


class LeadToOrderCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    pass


class OrderDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_order'
    model = Order
    template_name = 'crm_app/order_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return Order.objects.prefetch_related('orderedproduct_set').get(pk=self.kwargs.get('id'))


class OrderListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'order.view_order'
    model = Order
    template_name = 'crm_app/order_list.html'

    def get_queryset(self):
        return Order.objects.select_related('order_operator').all()


class WebCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.create_web'
    model = Web
    form_class = WebCreationForm
    template_name = 'crm_app/web_creation.html'

    def get_initial(self, *args, **kwargs):
        initial = super(WebCreationView, self).get_initial(**kwargs)
        initial['web_api_key'] = BaseUserManager().make_random_password(15)
        return initial

    def get_success_url(self):
        return reverse_lazy('web_detail', kwargs={'id': self.object.pk})


class WebDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_web'
    model = Web
    pk_url_kwarg = 'id'
    query_pk_and_slug = True
    template_name = 'crm_app/web_detail.html'


class WebListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_web'
    model = Web
    context_object_name = 'webs'
    template_name = 'crm_app/web-list.html'

    def get_queryset(self):
        return Web.objects.all().order_by('web_name')


class PaymentCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_paymentstoweb'
    model = PaymentsToWeb
    template_name = 'crm_app/payment_creation.html'
    form_class = PaymentCreationForm
    pk_url_kwarg = 'web_id'
    query_pk_and_slug = True

    def get_success_url(self):
        return reverse('payment_list')

    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['web'] = Web.objects.get(pk=self.kwargs.get('web_id'))
    #     return context

    def get_initial(self, **kwargs):
        initial = super(PaymentCreationView, self).get_initial(**kwargs)
        initial['web_FK'] = Web.objects.get(pk=self.kwargs.get('web_id'))
        initial['user_added'] = self.request.user
        return initial

    def post(self, request, *args, **kwargs):
        form = PaymentCreationForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            web_to_be_paid = form_data.get('web_FK')
            payment_amount = form.cleaned_data.get('payment_amount')
            web_previous_balance = web_to_be_paid.balance
            web_new_balance = web_previous_balance - payment_amount
            with transaction.atomic():
                PaymentsToWeb.objects.create(
                    web_FK=web_to_be_paid,
                    payment_amount=payment_amount,
                    user_added=self.request.user
                )
                web_to_be_paid.balance = web_new_balance
                web_to_be_paid.save()
                return redirect(reverse('payment_list'))
        else:
            form.add_error('__all__', 'Something went wrong. Try again.')
            return render(request, 'crm_app/payment_creation.html', {'form': form}
                          )


class PaymentDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_paymentstoweb'
    model = PaymentsToWeb
    template_name = 'crm_app/payment_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return PaymentsToWeb.objects.select_related('web_FK').get(pk=self.kwargs.get('id'))


class PaymentListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_paymentstoweb'
    model = PaymentsToWeb
    template_name = 'crm_app/payment_list.html'

    def get_queryset(self):
        return PaymentsToWeb.objects.select_related('web_FK').all()


class ProductCategoryCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_productcategory'
    form_class = ProductCategoryCreationForm
    template_name = 'crm_app/product_category_creation.html'

    def get_success_url(self):
        return reverse_lazy('product_category_detail', kwargs={'id': self.object.pk})


class ProductCategoryListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_productcategory'
    model = ProductCategory
    template_name = 'crm_app/product_category_list.html'

    def get_queryset(self):
        return ProductCategory.objects.prefetch_related('product_set').all()


class ProductCategoryDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_productcategory'
    model = ProductCategory
    template_name = 'crm_app/product_category_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return ProductCategory.objects.prefetch_related('product_set').get(pk=self.kwargs.get('id'))


class ProductCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_product'
    model = Product
    form_class = ProductCreationForm
    template_name = 'crm_app/product_creation.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'id': self.object.pk})


class ProductDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_product'
    model = Product
    template_name = 'crm_app/product_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True


class ProductListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_product'
    model = Product
    template_name = 'crm_app/product_list.html'

    def get_queryset(self):
        return Product.objects.select_related('product_category').all()


class OfferCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_offer'
    model = Offer
    template_name = 'crm_app/offer_creation.html'
    form_class = OfferCreationForm

    def get_success_url(self):
        return reverse('offer_detail', kwargs={'id': self.object.pk})


class OfferDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_offer'
    model = Offer
    template_name = 'crm_app/offer_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return Offer.objects.select_related('web', 'product').get(pk=self.kwargs.get('id'))


class OfferListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_offer'
    model = Offer
    template_name = 'crm_app/offer_list.html'

    def get_queryset(self):
        return Offer.objects.select_related('web', 'product').all()


class ProfileDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_profile'
    model = Profile
    template_name = 'crm_app/profile_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    # def get_object(self, queryset=None):
    #     return Profile.objects.select_related('user').get(self.kwargs.get('id'))


class ProfileListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_profile'
    model = Profile
    template_name = 'crm_app/profile_list.html'
