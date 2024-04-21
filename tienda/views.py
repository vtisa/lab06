from django.shortcuts import get_object_or_404, render
from .models import Categoria, Producto
 
def index(request):
    product_list = Producto.objects.order_by('nombre')[:6]
    categorias = Categoria.objects.all()  
    contexto = {'product_list': product_list, 'categorias': categorias, 'requerido': True}
    return render(request, 'index.html', contexto)


def producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    categorias = Categoria.objects.all()  
    context = {'producto': producto, 'categorias': categorias, 'requerido': True}
    return render(request, 'producto.html', context)


def lista_productos_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    producto_cat = categoria.producto_set.all()
    return render(request, 'categoria.html', {'categoria': categoria, 'producto_cat': producto_cat})
