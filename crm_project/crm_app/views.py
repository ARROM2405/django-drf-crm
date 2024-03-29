import copy
import logging

from django.contrib.auth import login, authenticate, mixins
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum, Count, Subquery, OuterRef, F
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views import generic
from django.db import transaction
from django.http import HttpResponse
import pprint

from .forms import *
from .models import *

info_logger = logging.getLogger('info_logger')

MENU_ALL = [
    {'title': 'Main', 'url_address': 'home_page'},
    {'title': 'Product categories', 'url_address': 'product_category_list'},
    {'title': 'Products', 'url_address': 'product_list'}
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


def add_menu_to_context(context: dict, user_role: str, selected_menu: str) -> dict:
    page_menu = []
    page_menu.extend(MENU_ALL)
    if user_role in ['Operator', 'Administrator']:
        page_menu.extend(MENU_OPERATORS)
    if user_role in ['Payments executive', 'Administrator']:
        page_menu.extend(MENU_PAYMENTS_EXECUTIVE)
    if user_role == 'Administrator':
        page_menu.extend(MENU_ADMIN)
    context['menu'] = page_menu
    context['selected_menu'] = selected_menu
    return context


class RegisterView(generic.View):
    form = RegistrationForm

    def get(self, request, form=form):
        info_logger.info(f'GET request, url: {reverse("register")}')
        return render(request, 'crm_app/registration.html', context={'form': form})

    def post(self, request, form=form):
        info_logger.info(f'POST request, url: {reverse("register")}')
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
            return redirect(reverse('home_page', kwargs={'stat': 'prod'}))
        return render(request, 'crm_app/registration.html', context={'form': form})


class UserLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'crm_app/login.html'

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("login")}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("login")}, user: {self.request.POST.get("username")}')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home_page', kwargs={'stat': 'prod'})


class HomePageView(mixins.LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("home_page", kwargs={"stat": self.kwargs.get("stat")})}, '
                         f'user: {self.request.user}')
        statistics_by = self.kwargs.get('stat')
        context = dict()
        opers = []
        if statistics_by == 'prod':
            prods = OrderedProduct.objects. \
                prefetch_related('product_FK'). \
                values('product_FK'). \
                annotate(total_sold=Sum('ordered_quantity')). \
                order_by('-total_sold')
            for p in prods:
                p['product'] = Product.objects.get(pk=p['product_FK'])
            context['statistics'] = prods
            context['statistic_units'] = 'prod'
        elif statistics_by == 'oper':
            users = User.objects.all()
            for user in users:
                user_total_sales = 0
                orders = Order.objects.filter(order_operator=user, status__in=['Delivered', 'Money_received'])
                ordered_products = OrderedProduct.objects.select_related('order_FK'). \
                    filter(order_FK__in=orders)
                for ordered_product in ordered_products:
                    user_total_sales += ordered_product.total_price()
                if user_total_sales > 0:
                    opers.append((float('{:2f}'.format(user_total_sales)), user))
            context['statistics'] = sorted(opers, reverse=True)
            context['statistic_units'] = 'oper'
        elif statistics_by == 'web':
            webs_stats = []
            webs = Web.objects.all()
            for web in webs:
                leads_count = len(Lead.objects.filter(
                    offer_FK__in=Offer.objects.filter(web=web)))
                if leads_count > 0:
                    webs_stats.append((leads_count, web))
            context['statistics'] = sorted(webs_stats, key=lambda tup: tup[0], reverse=True)
            context['statistic_units'] = 'web'
        context = add_menu_to_context(context=context, user_role=self.request.user.profile.role, selected_menu='Main')
        return render(request, 'crm_app/home_page.html', context=context)


class UserLogoutView(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("logout")}, user: {self.request.user}')
        return super().dispatch(request, *args, **kwargs)


class LeadCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_lead'
    model = Lead
    form_class = LeadCreationForm
    template_name = 'crm_app/lead_creation.html'

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("lead_creation")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        offer = form.cleaned_data.get('offer_FK')
        form.instance.lead_cost = offer.click_cost
        form.save()
        info_logger.info(f'POST request, url: {reverse("lead_creation")}, user: {self.request.user}, form_valid')
        with transaction.atomic():
            web = offer.web
            old_balance = web.balance
            new_balance = old_balance + offer.click_cost
            web.balance = new_balance
            web.save(update_fields=['balance'])
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('lead_list')


class LeadDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_lead'
    model = Lead
    template_name = 'crm_app/lead_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("lead_detail", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("lead_detail", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        self.request.session['lead_pk_to_be_processed'] = self.request.POST.get('lead_id_from_button')
        return redirect('order_creation')


class LeadListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_lead'
    model = Lead
    template_name = 'crm_app/lead_list.html'
    paginate_by = 20

    def get_queryset(self):
        return Lead.objects.values(
            'lead_id',
            'status',
            'created_at',
            'processed_at',
            'operator_assigned',
            'operator_assigned__user__username',
            'offer_FK__web__web_id',
            'offer_FK__web__web_name',
            'offer_FK__product__product_id',
            'offer_FK__product__product_name',

        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_menu_to_context(context=context, user_role=self.request.user.profile.role, selected_menu='Leads')
        return context

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("lead_list")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("lead_list")}, user: {self.request.user}')
        if self.request.POST.get('add_lead'):
            return redirect(reverse('lead_creation'))


class OrderCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_order'
    model = Order
    form_class = OrderCreationForm
    template_name = 'crm_app/order_creation.html'

    def get_initial(self, *args, **kwargs):
        initial = super(OrderCreationView, self).get_initial(**kwargs)
        if self.request.session.get('lead_pk_to_be_processed'):
            lead = Lead.objects.get(pk=self.request.session.get('lead_pk_to_be_processed'))
            initial['customer_first_name'] = lead.customer_first_name
            initial['customer_last_name'] = lead.customer_last_name
            initial['status'] = 'New order'
            initial['contact_phone'] = lead.contact_phone
            return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get('lead_pk_to_be_processed'):
            context['lead'] = Lead.objects.get(pk=self.request.session.get('lead_pk_to_be_processed'))
        return context

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("order_creation")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('delete_lead_link'):
            self.request.session['lead_pk_to_be_processed'] = None
            return redirect('order_creation')
        else:
            form = OrderCreationForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                if form_data.get('product_1') == form_data.get('product_2') or \
                        form_data.get('product_1') == form_data.get('product_3') or \
                        (form_data.get('product_2') is not None and
                         form_data.get('product_2') == form_data.get('product_3')):
                    form.add_error(f'product_1',
                                   f'Products are duplicated. Please pick unique SKU for each field, '
                                   f'or leave others empty.')
                    return render(request, self.template_name, context={'form': form, 'lead':
                        Lead.objects.get(pk=self.request.session.get('lead_pk_to_be_processed'))})

                for product_field, quantity_ordered_field in {
                    'product_1': 'product_1_quantity',
                    'product_2': 'product_2_quantity',
                    'product_3': 'product_3_quantity'
                }.items():
                    if form_data.get(product_field) is not None:
                        product = form_data.get(product_field)
                        quantity_ordered = form_data.get(quantity_ordered_field)
                        if product.quantity_available < quantity_ordered:
                            form.add_error(f'{quantity_ordered_field}',
                                           f'Ordered too many of {product.product_name}. '
                                           f'Available quantity is {product.quantity_available}.')
                            return render(request, self.template_name, context={'form': form})

                with transaction.atomic():
                    if self.request.session.get('lead_pk_to_be_processed'):
                        lead = Lead.objects.get(pk=self.request.session.get('lead_pk_to_be_processed'))
                    else:
                        lead = None
                    order = Order.objects.create(
                        lead_FK=lead,
                        customer_first_name=form_data.get('customer_first_name'),
                        customer_last_name=form_data.get('customer_last_name'),
                        status=form_data.get('status'),
                        sent_date=form_data.get('sent_date'),
                        contact_phone=form_data.get('contact_phone'),
                        delivery_city=form_data.get('delivery_city'),
                        delivery_street=form_data.get('delivery_street'),
                        delivery_house_number=form_data.get('delivery_house_number'),
                        delivery_apartment_number=form_data.get('delivery_apartment_number'),
                        delivery_zip_code=form_data.get('delivery_zip_code'),
                        order_operator=self.request.user
                    )

                    for product_field, quantity_ordered_and_price_fields in {
                        'product_1': ('product_1_quantity', 'product_1_price'),
                        'product_2': ('product_2_quantity', 'product_2_price'),
                        'product_3': ('product_3_quantity', 'product_3_price')
                    }.items():
                        product = form_data.get(product_field)
                        if product is not None:
                            current_available_quantity = product.quantity_available
                            updated_available_quantity = \
                                current_available_quantity - form_data.get(quantity_ordered_and_price_fields[0])
                            product.quantity_available = updated_available_quantity
                            prev_quantity_in_delivery = product.quantity_in_delivery
                            updated_quantity_in_delivery = prev_quantity_in_delivery + \
                                                           form_data.get(quantity_ordered_and_price_fields[0])
                            product.quantity_in_delivery = updated_quantity_in_delivery
                            product.save()

                            OrderedProduct.objects.create(
                                order_FK=order,
                                product_FK=product,
                                ordered_quantity=form_data.get(quantity_ordered_and_price_fields[0]),
                                ordered_product_price=form_data.get(quantity_ordered_and_price_fields[1])
                            )

                            if lead:
                                lead.status = 'Approved'
                                lead.operator_assigned = self.request.user.profile
                                lead.processed_at = now()
                                lead.save()
                    self.request.session['lead_pk_to_be_processed'] = None
                    info_logger.info(f'POST request, url: {reverse("order_creation")}, user: {self.request.user}, '
                                     f'created order pk: {order.pk}')
                    return redirect(reverse('order_list'))
            else:
                return render(self.request, self.template_name, context={'form': form})


class OrderDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_order'
    model = Order
    template_name = 'crm_app/order_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return Order.objects.prefetch_related('orderedproduct_set').get(pk=self.kwargs.get('id'))

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("order_detail", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("order_detail", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        if self.request.POST.get('update_order'):
            return redirect(reverse('order_update', kwargs={'id': self.kwargs.get('id')}))


class OrderListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_order'
    model = Order
    template_name = 'crm_app/order_list.html'
    paginate_by = 30

    def get_queryset(self):
        return Order.objects.select_related('order_operator').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_menu_to_context(context=context, user_role=self.request.user.profile.role, selected_menu='Orders')
        return context

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("order_list")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("order_list")}, user: {self.request.user}')
        if self.request.POST.get('add_order'):
            return redirect(reverse('order_creation'))


class OrderUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'crm_app.change_order'
    model = Order
    template_name = 'crm_app/order_update.html'
    fields = ['status', 'sent_date', 'contact_phone', 'delivery_city', 'delivery_street', 'delivery_house_number',
              'delivery_apartment_number',
              'delivery_zip_code']
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return Order.objects.get(pk=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse('order_detail', kwargs={'id': self.kwargs.get('id')})

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("order_update", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("order_update", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        order = self.get_object()
        ordered_products = OrderedProduct.objects.filter(order_FK=order)
        old_status = order.status
        new_status = self.request.POST.get('status')
        with transaction.atomic():
            if old_status in ('New order', 'In preparation', 'Sent') and new_status in ('Delivered', 'Money received'):
                for ordered_product in ordered_products:
                    product = ordered_product.product_FK
                    old_quantity_in_delivery = product.quantity_in_delivery
                    new_quantity_in_delivery = old_quantity_in_delivery - ordered_product.ordered_quantity
                    product.quantity_in_delivery = new_quantity_in_delivery
                    product.save(update_fields=['quantity_in_delivery'])
            elif old_status in ('New order', 'In preparation', 'Sent') and \
                    new_status in ('Return', 'Confirmed return', 'Canceled'):
                for ordered_product in ordered_products:
                    product = ordered_product.product_FK
                    old_quantity_in_delivery = product.quantity_in_delivery
                    new_quantity_in_delivery = old_quantity_in_delivery - ordered_product.ordered_quantity
                    product.quantity_in_delivery = new_quantity_in_delivery
                    old_quantity_available = product.quantity_available
                    new_quantity_available = old_quantity_available + ordered_product.ordered_quantity
                    product.quantity_available = new_quantity_available
                    product.save(update_fields=['quantity_available', 'quantity_in_delivery'])
            elif old_status in ('Return', 'Confirmed return', 'Canceled') and \
                    new_status in ('New order', 'In preparation', 'Sent'):
                for ordered_product in ordered_products:
                    product = ordered_product.product_FK
                    old_quantity_in_delivery = product.quantity_in_delivery
                    new_quantity_in_delivery = old_quantity_in_delivery + ordered_product.ordered_quantity
                    product.quantity_in_delivery = new_quantity_in_delivery
                    old_quantity_available = product.quantity_available
                    new_quantity_available = old_quantity_available - ordered_product.ordered_quantity
                    product.quantity_available = new_quantity_available
                    product.save(update_fields=['quantity_available', 'quantity_in_delivery'])
            elif old_status in ('Delivered', 'Money received') and \
                    new_status in ('New order', 'In preparation', 'Sent'):
                for ordered_product in ordered_products:
                    product = ordered_product.product_FK
                    old_quantity_in_delivery = product.quantity_in_delivery
                    new_quantity_in_delivery = old_quantity_in_delivery + ordered_product.ordered_quantity
                    product.quantity_in_delivery = new_quantity_in_delivery
                    product.save(update_fields=['quantity_in_delivery'])
            elif old_status in ('Delivered', 'Money received') and \
                    new_status in ('Return', 'Confirmed return', 'Canceled'):
                for ordered_product in ordered_products:
                    product = ordered_product.product_FK
                    old_quantity_in_delivery = product.quantity_in_delivery
                    new_quantity_in_delivery = old_quantity_in_delivery + ordered_product.ordered_quantity
                    product.quantity_in_delivery = new_quantity_in_delivery
                    old_quantity_available = product.quantity_available
                    new_quantity_available = old_quantity_available + ordered_product.ordered_quantity
                    product.quantity_available = new_quantity_available
                    product.save(update_fields=['quantity_available'])
            elif old_status in ('Return', 'Confirmed return', 'Canceled') and \
                    new_status in ('Delivered', 'Money received'):
                for ordered_product in ordered_products:
                    product = ordered_product.product_FK
                    old_quantity_in_delivery = product.quantity_in_delivery
                    new_quantity_in_delivery = old_quantity_in_delivery + ordered_product.ordered_quantity
                    product.quantity_in_delivery = new_quantity_in_delivery
                    old_quantity_available = product.quantity_available
                    new_quantity_available = old_quantity_available - ordered_product.ordered_quantity
                    product.quantity_available = new_quantity_available
                    product.save(update_fields=['quantity_available'])
            return super().post(request, *args, **kwargs)


class WebCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_web'
    model = Web
    form_class = WebCreationForm
    template_name = 'crm_app/web_creation.html'

    def get_initial(self, *args, **kwargs):
        initial = super(WebCreationView, self).get_initial(**kwargs)
        initial['web_api_key'] = BaseUserManager().make_random_password(15)
        return initial

    def get_success_url(self):
        return reverse_lazy('web_detail', kwargs={'id': self.object.pk})

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("web_creation")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("web_creation")}, user: {self.request.user}')
        return super().post(request, *args, **kwargs)


class WebDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_web'
    model = Web
    pk_url_kwarg = 'id'
    query_pk_and_slug = True
    template_name = 'crm_app/web_detail.html'

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("web_detail", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("web_detail", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        if self.request.POST.get('update_web'):
            return redirect(reverse('web_update', kwargs={'id': self.kwargs.get('id')}))


class WebListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_web'
    model = Web
    context_object_name = 'webs'
    template_name = 'crm_app/web-list.html'
    paginate_by = 20

    def get_queryset(self):
        return Web.objects.all().order_by('web_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_menu_to_context(context=context, user_role=self.request.user.profile.role, selected_menu='Webs')
        return context

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("web_list")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("web_list")}, user: {self.request.user}')
        if self.request.POST.get('add_web'):
            return redirect(reverse('web_creation'))
        elif self.request.POST.get('web_pk') is not None:
            return redirect(reverse('payment_creation', kwargs={'web_id': self.request.POST.get('web_pk')}))


class WebUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'crm_app.change_web'
    model = Web
    fields = ['web_name', 'web_description', 'active']
    template_name = 'crm_app/web_update.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_success_url(self):
        return reverse('web_detail', kwargs={'id': self.kwargs.get('id')})

    def get_object(self, queryset=None):
        return Web.objects.get(pk=self.kwargs.get('id'))

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("web_update", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("web_update", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        return super().post(request, *args, **kwargs)


class PaymentCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_paymentstoweb'
    model = PaymentsToWeb
    template_name = 'crm_app/payment_creation.html'
    form_class = PaymentCreationForm
    pk_url_kwarg = 'web_id'
    query_pk_and_slug = True

    def get_success_url(self):
        return reverse('payment_list')

    def get_initial(self, **kwargs):
        initial = super(PaymentCreationView, self).get_initial(**kwargs)
        initial['web_FK'] = Web.objects.get(pk=self.kwargs.get('web_id'))
        initial['user_added'] = self.request.user
        return initial

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("payment_creation", kwargs={"web_id": self.kwargs.get("web_id")})}, '
                         f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("payment_creation", kwargs={"web_id": self.kwargs.get("web_id")})}, '
                         f'user: {self.request.user}')
        form = PaymentCreationForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            web_to_be_paid = form_data.get('web_FK')
            payment_amount = form_data.get('payment_amount')
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

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("payment_detail", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("payment_detail", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        if self.request.POST.get('update_payment'):
            return redirect(reverse('payment_update', kwargs={'id': self.kwargs.get('id')}))


class PaymentListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_paymentstoweb'
    model = PaymentsToWeb
    template_name = 'crm_app/payment_list.html'
    paginate_by = 20

    def get_queryset(self):
        return PaymentsToWeb.objects.select_related('web_FK').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_menu_to_context(context=context, user_role=self.request.user.profile.role, selected_menu='Payments')
        return context

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("payment_list")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("payment_list")}, user: {self.request.user}')
        return super().post(request, *args, **kwargs)


class PaymentUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView, generic.edit.DeletionMixin):
    permission_required = 'crm_app.change_paymentstoweb'
    model = PaymentsToWeb
    template_name = 'crm_app/payment_update.html'
    fields = ['payment_amount']
    pk_url_kwarg = 'id'
    slug_url_kwarg = True

    def get_object(self, queryset=None):
        return PaymentsToWeb.objects.get(pk=self.kwargs.get('id'))

    def get_success_url(self):
        kwarg_id = self.kwargs.get('id')
        if self.request.POST.get('Delete payment'):
            return reverse('payment_delete', kwargs={'id': kwarg_id})
        return reverse('payment_detail', kwargs={'id': kwarg_id})

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("payment_update", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("payment_update", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        payment_object = self.get_object()
        old_payment_sum = copy.copy(payment_object.payment_amount)
        web = payment_object.web_FK
        web_previous_balance = web.balance
        with transaction.atomic():
            if self.request.POST.get('delete_payment'):
                web.balance = web_previous_balance + payment_object.payment_amount
                web.save(update_fields=['balance'])
                self.delete(self.request)
                return redirect(reverse('payment_list'))
            else:
                new_payment_sum = self.request.POST.get('payment_amount')
                difference = float(old_payment_sum) - float(new_payment_sum)
                web.balance = float(web_previous_balance) + difference
                web.save(update_fields=['balance'])
                super().post(request, *args, **kwargs)
                return redirect(self.get_success_url())


class ProductCategoryCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_productcategory'
    form_class = ProductCategoryCreationForm
    template_name = 'crm_app/product_category_creation.html'

    def get_success_url(self):
        return reverse_lazy('product_category_detail', kwargs={'id': self.object.pk})

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("product_category_creation")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("product_category_creation")}, user: {self.request.user}')
        return super().post(request, *args, **kwargs)


class ProductCategoryListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_productcategory'
    model = ProductCategory
    template_name = 'crm_app/product_category_list.html'
    paginate_by = 20

    def get_queryset(self):
        return ProductCategory.objects.prefetch_related('product_set').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_menu_to_context(context=context, user_role=self.request.user.profile.role,
                            selected_menu='Product categories')
        return context

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("product_category_list")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(f'POST request, url: {reverse("product_category_list")}, user: {self.request.user}')
        if self.request.POST.get('add_product_category'):
            return redirect(reverse('product_category_creation'))


class ProductCategoryDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_productcategory'
    model = ProductCategory
    template_name = 'crm_app/product_category_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return ProductCategory.objects.prefetch_related('product_set').get(pk=self.kwargs.get('id'))

    def get(self, request, *args, **kwargs):
        info_logger.info(f'GET request, url: {reverse("product_category_detail", kwargs={"id": self.kwargs.get("id")})}, '
                         f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'POST request, url: {reverse("product_category_update", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return redirect(reverse('product_category_update', kwargs={'id': self.kwargs.get('id')}))


class ProductCategoryUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'crm_app.change_productcategory'
    model = ProductCategory
    fields = ['category_name']
    template_name = 'crm_app/product_category_update.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return ProductCategory.objects.get(pk=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse('product_category_update', kwargs={'id': self.kwargs.get('id')})

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("product_category_update", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'POST request, url: {reverse("product_category_update", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return super().post(request, *args, **kwargs)


class ProductCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_product'
    model = Product
    form_class = ProductCreationForm
    template_name = 'crm_app/product_creation.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'id': self.object.pk})

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("product_creation")}, '
            f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'POST request, url: {reverse("product_creation")}, '
            f'user: {self.request.user}')
        return super().post(request, *args, **kwargs)


class ProductDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_product'
    model = Product
    template_name = 'crm_app/product_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("product_category_detail", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'POST request, url: {reverse("product_category_detail", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}'
        )
        return redirect(reverse('product_update', kwargs={'id': self.kwargs.get('id')}))


class ProductListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_product'
    model = Product
    template_name = 'crm_app/product_list.html'
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.select_related('product_category').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_menu_to_context(context=context, user_role=self.request.user.profile.role, selected_menu='Products')
        return context

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("product_list")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'POST request, url: {reverse("product_list")}, user: {self.request.user}')
        if self.request.POST.get('add_product'):
            return redirect(reverse('product_creation'))


class ProductUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'crm_app.change_product'
    model = Product
    fields = ['product_name', 'product_price', 'product_category', 'product_description', 'product_image',
              'quantity_available']
    template_name = 'crm_app/product_update.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_success_url(self):
        return reverse('product_detail', kwargs={'id': self.kwargs.get('id')})

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("product_update", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'POST request, url: {reverse("product_update", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return super().post(request, *args, **kwargs)


class OfferCreationView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'crm_app.add_offer'
    model = Offer
    template_name = 'crm_app/offer_creation.html'
    form_class = OfferCreationForm

    def get_success_url(self):
        return reverse('offer_detail', kwargs={'id': self.object.pk})

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("offer_creation")}, user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'POST request, url: {reverse("offer_creation")}, '
            f'user: {self.request.user}')
        return super().post(request, *args, **kwargs)


class OfferDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_offer'
    model = Offer
    template_name = 'crm_app/offer_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return Offer.objects.select_related('web', 'product').get(pk=self.kwargs.get('id'))

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("offer_detail", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'POST request, url: {reverse("offer_detail", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        if self.request.POST.get('update_offer'):
            return redirect(reverse('offer_update', kwargs={'id': self.kwargs.get('id')}))
        else:
            return HttpResponse('Not found')


class OfferListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_offer'
    model = Offer
    template_name = 'crm_app/offer_list.html'
    paginate_by = 20

    def get_queryset(self):
        return Offer.objects.select_related('web', 'product').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_menu_to_context(context=context, user_role=self.request.user.profile.role, selected_menu='Offers')
        return context

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("offer_list")}, '
            f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("offer_list")}, '
            f'user: {self.request.user}')
        if self.request.POST.get('add_offer'):
            return redirect(reverse('offer_creation'))


class OfferUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'crm_app.change_offer'
    model = Offer
    template_name = 'crm_app/offer_update.html'
    fields = ['click_cost']
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return Offer.objects.get(pk=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse('offer_detail', kwargs={'id': self.kwargs.get('id')})

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("offer_detail", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'POST request, url: {reverse("offer_detail", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return super().post(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     offer = Offer.objects.get(pk=self.kwargs.get(''))
    #     return redirect(reverse('offer_detail', kwargs={'id': self.kwargs.get('id')}))


class ProfileDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = 'crm_app.view_profile'
    model = Profile
    template_name = 'crm_app/profile_detail.html'
    pk_url_kwarg = 'id'
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("profile_detail", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("profile_detail", kwargs={"id": self.kwargs.get("id")})}, '
            f'user: {self.request.user}')
        return super().post(request, *args, **kwargs)

    # def get_object(self, queryset=None):
    #     return Profile.objects.select_related('user').get(self.kwargs.get('id'))


class ProfileListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = 'crm_app.view_profile'
    model = Profile
    template_name = 'crm_app/profile_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_menu_to_context(context=context, user_role=self.request.user.profile.role, selected_menu='Users')
        return context

    def get(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("profile_list")}, '
            f'user: {self.request.user}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info_logger.info(
            f'GET request, url: {reverse("profile_list")}, '
            f'user: {self.request.user}')
        return super().post(request, *args, **kwargs)
