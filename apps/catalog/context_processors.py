from .models import Category, FragranceFamily

def categories_context(request):
    return {
        'nav_categories': Category.objects.all(),
        'nav_families': FragranceFamily.objects.all(),
    }
