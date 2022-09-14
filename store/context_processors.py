from .models import Products

def search_query(request):
    links = Products.objects.all()
    return dict(links=links)