from django.db import models
import uuid
from PIL import Image
from django.utils.timezone import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from datetime import date


User = get_user_model()


class Pearl(models.Model):
    parcel = models.CharField(_("parcel"), max_length = 30)
    shape = models.CharField(_("shape"), max_length = 30)
    color = models.CharField(_("color"), max_length = 30)
    size = models.CharField(_("size"), max_length = 30)
    type_name = models.CharField(_("type name"), max_length = 30)

    def __str__(self) -> str:
        return f"{self.color} {self.type_name} {self.size}"

    class Meta:
        ordering = ['shape']


class MetalType(models.Model):
    alloy = models.CharField(_("alloy"), max_length = 30, blank=True)

    def __str__(self) -> str:
        return self.alloy

    class Meta:
        ordering = ['alloy']


class JewelleryType(models.Model):
    name = models.CharField(_("jewellery type"), max_length = 80, help_text=_("Enter the name of jewellery type"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(_("category"), max_length = 80, help_text=_("Enter the name of jewellery category"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def link_filtered_products(self):
        link = reverse('products')+'?category_id='+str(self.id)
        return format_html('<a class="category" href="{link}">{name}</a>', link=link, name=self.name)

class Product(models.Model):
    category = models.ManyToManyField(Category, verbose_name=_("category(-ies)"), help_text=_("Choose category(-ies) for this product"))
    name = models.CharField(_("product name"), max_length = 100)
    price = models.DecimalField(_("product price"), max_digits=18, decimal_places=2)
    image = models.ImageField(_("product image"), upload_to='product_images', blank=True, null=True)
    jewellery_type = models.ForeignKey(JewelleryType, verbose_name=_("jewellery type"), on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image.path)
            if image.width > 500 or image.height > 500:
                output_size = (500, 500)
                image.thumbnail(output_size)
                image.save(self.image.path)

    def display_category(self) -> str:
        return ', '.join(category.name for category in self.category.all())
    display_category.short_description = _('category(-ies)')

    def __str__(self) -> str:
        return f"{self.name} {self.jewellery_type}"


class Customer(models.Model):
    phone = models.CharField(_("phone"), max_length=20)
    user = models.OneToOneField(get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE, related_name="customer")

    def __str__(self) -> str:
        return f"{self.user}"


def get_due_date():
        return date.today() + timedelta(days=30)


class Order(models.Model):
    STATUS_CHOICES = (
        ('n', _('new - not approved')),
        ('a', _('advance payment taken - approved')),
        ('b', _('design stage')),
        ('m', _('manufacturing stage')),
        ('d', _('done but not picked up')),
        ('p', _('done and picked up')),
        ('c', _('cancelled')),
        ('f', _('fully paid')),
    )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='n')
    date = models.DateField(_("order date"), auto_now_add=True)
    total = models.DecimalField(_("total amount"), max_digits=18, decimal_places=2, default=0)
    customer = models.ForeignKey(Customer, verbose_name=_("customer"), on_delete=models.CASCADE)
    due_date = models.DateField(_('due date'), default=get_due_date)

    @property
    def is_overdue(self):
        if self.due_date and self.due_date < datetime.date(datetime.now()):
            return True
        return False

    class Meta:
        ordering = ['due_date']

    def get_total(self):
        total = 0
        for line in self.order_lines.all():
            total += line.total
        return total

    # def save(self, *args, **kwargs ):
    #     if not self._state.adding:
    #         old = self.get_object(id=self.id)
    #         if old.status != self.status and self.status == 'd':
    #             print('siusti maila')
    #     super().save(*args, **kwargs)
     

    def __str__(self) -> str:
        return f"{self.customer} - {self.due_date} - {self.total}"

    # @classmethod
    # def get_object(cls, id):
    #     return cls.objects.get(id=id)


class OrderLine(models.Model):
    unique_id = models.UUIDField(_('unique ID'), default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, verbose_name=_("order"), on_delete=models.CASCADE, related_name="order_lines")
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE, related_name="order_lines")
    quantity = models.IntegerField(_("quantity"), default=1)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)
    HAND_CHOICES = (
        ('r', _("right")), 
        ('l', _('left'))
    )
    hand = models.CharField(_('hand'), max_length=1, choices=HAND_CHOICES, blank=True, null=True)
    FINGER_CHOICES = (
        ('t', _("thumb")), 
        ('i', _('index')), 
        ('m', _('middle')), 
        ('r', _('ring')), 
        ('p', _('pinky')),
    )
    finger = models.CharField(_('finger'), max_length=1, choices=FINGER_CHOICES, blank=True, null=True)
    ring_size = models.CharField(_('ring_size'), max_length=20, blank=True, null=True)
    measurement = models.CharField(_('measurement'), max_length=200, blank=True, null=True)
    metal_type = models.ManyToManyField(MetalType, verbose_name=_("metal type(s)"))
    pearl = models.ManyToManyField(Pearl, verbose_name=_("pearl(s)"), blank=True)
    weight = models.CharField(_('weight'), max_length=200, blank=True, null=True)
    photo = models.ImageField(_("photo"), upload_to='product_photos', blank=True, null=True)
    specification = models.TextField(_("specification"), max_length=2000, blank=True, null=True, help_text=_("Enter preferred specifications for this product"))
    engraving = models.TextField(_('engraving text'),  max_length=150, blank=True, null=True)
    engraving_file = models.FileField(_("engraving file"), upload_to='engraving_files', blank=True, null=True)
    certificate = models.CharField(_('certificate'), max_length=20, blank=True, null=True)
    restoration = models.DateField(_("restoration date"), blank=True, null=True)

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self) -> str:
        return f"{self.product} {self.quantity} {self.price}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo or self.engraving_file:
            photo = Image.open(self.photo.path)
            if photo.width > 500 or photo.height > 500:
                output_size = (500, 500)
                photo.thumbnail(output_size)
                photo.save(self.photo.path)
        self.order.total = self.order.get_total()
        self.order.save()
            
    def display_metal_type(self) -> str:
        return ', '.join(metal_type.alloy for metal_type in self.metal_type.all())
    display_metal_type.short_description = _("metal type(s)")

    def display_pearl(self) -> str:
        return ', '.join(f"{pearl.type_name} {pearl.color} / {pearl.size}"  for pearl in self.pearl.all())
    display_pearl.short_description = _("pearl(s)")

class ReviewProduct(models.Model):
    customer = models.ForeignKey(get_user_model(), verbose_name=_('customer'), on_delete=models.CASCADE, related_name='product_reviews')
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField(_("content"), max_length=2000)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f"{self.customer} review on {self.product} at {self.created_at}"
