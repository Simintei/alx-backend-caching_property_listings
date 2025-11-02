from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property   # assuming your model is named Property
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = Property.objects.all().values()
    return JsonResponse(list(properties), safe=False)


def property_list(request):
    properties = get_all_properties()
    return render(request, 'properties/property_list.html', {'properties': properties})
