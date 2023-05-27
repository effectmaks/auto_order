from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Image
from django.conf import settings
import os
import logging
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import imghdr
import time
logger = logging.getLogger('django')


@login_required
def orders_list(request):
    if request.user.is_superuser:  # Если пользователь - суперпользователь, показываем все заказы
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)  # Для обычного пользователя показываем только его заказы
    context = {'orders': orders}
    return render(request, 'list_orders.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user == order.user or request.user.is_superuser:
        context = {'order': order}
        return render(request, 'detail_orders.html', context)
    else:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('orders_list')


@login_required
def add_order1(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('orders_list')
    else:
        form = OrderForm()
    return render(request, 'add_order.html', {'form': form})


from .forms import OrderForm, ImageInlineForm
from django.forms import inlineformset_factory

@login_required
def add_order(request):
    ImageFormSet = inlineformset_factory(Order, Image, form=ImageInlineForm, extra=3, can_delete=False)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)

        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()

            for form in formset:
                if form.cleaned_data.get('image'):
                    image = form.save(commit=False)
                    image.order = order
                    image.save()
            return redirect('orders_list')
    else:
        order_form = OrderForm()
        formset = ImageFormSet()

    context = {
        'order_form': order_form,
        'formset': formset,
    }

    return render(request, 'add_order.html', context)


@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user == order.user or request.user.is_superuser:
        order.delete()
        messages.success(request, 'Order deleted.')
    else:
        messages.error(request, 'You do not have permission to delete this order.')
    return redirect('orders_list')
