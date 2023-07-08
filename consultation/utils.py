from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

def pagination(request, invoices):
     #======== Pour la pagination (5 données par page)
    default_page = 1 # page par défaut
    page = request.GET.get('page', default_page)
        # paginate item
    items_per_page = 5
        # on va passer notre liste d'objet (invoices) à l'intérieur de Paginator et on lui donne le nombre
        # d'éléments par page (items_per_page)
    paginator = Paginator(invoices, items_per_page)
        
    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)
        
    return items_page