from django.shortcuts import get_object_or_404, render_to_response
from ecomstore.catalog.models import Category, Product, ProductReview
from django.template import RequestContext
from django.template import Context

from django.core import urlresolvers
from ecomstore.cart import cart
from django.http import HttpResponseRedirect, HttpResponse
from ecomstore.catalog.forms import ProductAddToCartForm, ProductReviewForm

from ecomstore.stats import stats
from ecomstore.settings import PRODUCTS_PER_ROW

from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import simplejson

def index(request, template_name="catalog/index.html"):
    search_recs = stats.recommended_from_search(request)
    featured = Product.featured.all()[0:PRODUCTS_PER_ROW]
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)
    page_title = 'Modern Musician | Musical Instruments and Sheet Music for Musicians'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def show_category(request, category_slug, template_name="catalog/category.html"):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def show_product(request, product_slug, template_name="catalog/product.html"):
    """ view for each product page """
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.all()
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description

    # evaluate the HTTP method, change as needed
    if request.method == 'POST':
        #create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        #check if posted data is valid
        if form.is_valid():
            #add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
    else:
        #create the unbound form. Notice the request as a keyword argument
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set test cookie to make sure cookies are enabled
    request.session.set_test_cookie()
    stats.log_product_view(request, p)
    # product review additions, CH 10
    product_reviews = ProductReview.approved.filter(product=p).order_by('-date')
    review_form = ProductReviewForm()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def add_review(request):
    """ AJAX view that takes a form POST from a user submitting a new product review;
    requires a valid product slug and args from an instance of ProductReviewForm;
    return a JSON response containing two variables: 'review', which contains 
    the rendered template of the product review to update the product page, 
    and 'success', a True/False value indicating if the save was successful.
    """
    import pdb; pdb.set_trace()
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        slug = request.POST.get('slug')
        product = Product.active.get(slug=slug)
        review.user = request.user
        review.product = product
        review.save()
    
        template = "catalog/product_review.html"
        html = render_to_string(template, {'review': review })
        response = simplejson.dumps({'success':'True', 'html': html})
        
    else:
        html = form.errors.as_ul()
        response = simplejson.dumps({'success':'False', 'html': html})

    ret = HttpResponse(response, 
                           content_type='application/javascript; charset=utf-8')
    return ret


