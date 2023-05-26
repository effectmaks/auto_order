from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('orders_list')
    else:
        form = OrderForm()
    return render(request, 'add_order.html', {'form': form})


@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user == order.user or request.user.is_superuser:
        order.delete()
        messages.success(request, 'Order deleted.')
    else:
        messages.error(request, 'You do not have permission to delete this order.')
    return redirect('orders_list')
