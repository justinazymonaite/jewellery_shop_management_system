from django.shortcuts import render, get_object_or_404
from . models import Product, Category, Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from . forms import ProductReviewForm
from django.contrib import messages
from django.views.generic.base import ContextMixin

def index(request):
    return render(request, 'jewellery/index.html', {"categories": Category.objects.all()})


class CategoriesMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    

class ProductListView(ListView, CategoriesMixin):
    model = Product
    template_name = 'jewellery/product_list.html'
    paginate_by = 21

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category_id')
        if category_id:
            context['category'] = get_object_or_404(Category, id=category_id)
        return context


class ProductDetailView(FormMixin, DetailView, CategoriesMixin):
    model = Product
    template_name = 'jewellery/product_detail.html'
    form_class = ProductReviewForm

    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.get_object().id})

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(self.request, _("You're posting too much!"))
            return self.form_invalid(form)

    def get_initial(self):
        return {
            'product': self.get_object(), 
            'customer': self.request.user
        }

    def form_valid(self, form):
        form.instance.product = self.get_object()
        form.instance.customer = self.request.user
        form.save()
        messages.success(self.request, _("Your review has been posted."))
        return super().form_valid(form)


class OrderListView(LoginRequiredMixin, ListView, CategoriesMixin):
    model = Order
    template_name = 'jewellery/order_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'customer'):
            queryset = queryset.filter(customer=self.request.user.customer).order_by('date')
        else:
            queryset = None
        return queryset

    
class OrderDetailView(FormMixin, DetailView, CategoriesMixin):
    model = Order
    template_name = 'jewellery/order_detail.html'

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.get_object().id})

