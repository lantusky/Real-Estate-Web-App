from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Listing
from .choices import price_choices, state_choices, bedroom_choices

def listings(request):
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  paginator = Paginator(listings, 3)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)
  context = {
    'listings': paged_listings
  }
  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    'listing': listing
  }
  return render(request, 'listings/listing.html', context)

def search(request):
  queryset_list = Listing.objects.order_by('-list_date')
  # handle keywords filter
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # handle exact filters
  filters = ['city', 'state', 'bedrooms']
  for key in filters:
    if key in request.GET:
      val = request.GET[key]
      if val:
        dict = {key + '__iexact': val}
        queryset_list = queryset_list.filter(**dict)
  
  # handle range filters
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'state_choices': state_choices,
    'price_choices': price_choices,
    'bedroom_choices': bedroom_choices,
    'listings': queryset_list,
    'values': request.GET
  }
  return render(request, 'listings/search.html', context)
