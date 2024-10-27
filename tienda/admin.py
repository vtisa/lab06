from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto, Cliente
from django.contrib import messages
from datetime import datetime

def actualizar_stock(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        nuevo_stock = request.POST.get('nuevo_stock')
        if categoria_id and nuevo_stock:
            try:
                categoria = Categoria.objects.get(pk=categoria_id)
                productos = Producto.objects.filter(categoria=categoria)
                productos.update(stock=int(nuevo_stock))
                messages.success(request, f"Stock actualizado a {nuevo_stock} unidades para la categoría {categoria.nombre}.")
            except Categoria.DoesNotExist:
                messages.error(request, "La categoría seleccionada no existe.")
        else:
            messages.error(request, "No se proporcionaron datos suficientes.")
        return redirect('admin:tienda_producto_changelist')
    else:
        categorias = Categoria.objects.all()
        return render(request, 'admin/actualizar_stock.html', {'categorias': categorias})

def actualizar_fecha_publicacion(request):
    categoria_id = request.POST.get('categoria_id')
    categoria = None
    if categoria_id:
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        if request.method == 'POST':
            nueva_fecha = request.POST.get('nueva_fecha')
            if nueva_fecha:
                try:
                    nueva_fecha_dt = datetime.strptime(nueva_fecha, '%Y-%m-%dT%H:%M')
                    productos = Producto.objects.filter(categoria=categoria)
                    productos.update(pub_date=nueva_fecha_dt)
                    nueva_fecha_str = nueva_fecha_dt.strftime('%Y-%m-%d %H:%M')
                    messages.success(request, f"Fecha de publicación actualizada a {nueva_fecha_str} para la categoría {categoria.nombre}.")
                except ValueError:
                    messages.error(request, "Formato de fecha incorrecto. Utiliza el formato 'YYYY-MM-DDTHH:MM'.")
            else:
                messages.error(request, "No se ingresó una fecha válida.")
        return redirect('admin:tienda_producto_changelist')
    categorias = Categoria.objects.all()
    return render(request, 'admin/actualizar_fecha_publicacion.html', {'categorias': categorias, 'categoria': categoria})
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'pub_date']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('actualizar_stock/', self.admin_site.admin_view(actualizar_stock), name='actualizar_stock'),
            path('actualizar_fecha_publicacion/', self.admin_site.admin_view(actualizar_fecha_publicacion), name='actualizar_fecha_publicacion'),
        ]
        return custom_urls + urls

admin.site.register(Categoria)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Cliente)