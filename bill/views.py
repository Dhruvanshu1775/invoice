from io import BytesIO
from re import template
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, DetailView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib.auth import  login as auth_login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from django.urls import reverse, reverse_lazy
import pywhatkit
from selenium import webdriver



# Create your views here.


class Dashboard(LoginRequiredMixin, TemplateView,):
    template_name = 'dashboard.html'


# class HomePage(LoginRequiredMixin, TemplateView):
#     template_name = 'index.html' 

from django.template.loader import get_template

from xhtml2pdf import pisa


# def pdf_data(template_source):
#     # products = Bill.objects.all()

#     # template_path = 'pdf_file.html'

#     context = {'products': 'products'}

#     # response = HttpResponse(content_type='application/pdf')

#     # response['Content-Disposition'] = 'filename="products_report.pdf"'

#     template = get_template(template)

#     html = template.render(context)

#     result  = BytesIO()

#     pdf = pisa.pisaDocument(BytesIO(html.encode("iso-8859-1")),result)

#     if not pdf.error:
#         return HttpResponse(result.getvalue(),context_type="application/pdf")
#     return None



def fetch_resources(uri, rel):
    import os.path
    from django.conf import settings
    path = os.path.join(
            settings.STATIC_ROOT,
            uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),
                                            dest=result,
                                            encoding='ISO-8859-1',
                                            link_callback=fetch_resources)
    if not pdf.err:
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'filename="heyyyyyyyyyyy.pdf"'

        return HttpResponse(result.getvalue(), response)
    return None


from django.db.models import Sum, F
from num2words import num2words

def pdf_report_create(request,id):
    

    
    bill_obj = Bill.objects.get(id = id)
    # bill_data = Bill.objects.filter(id = id).values('product_key','bill_number',)


    product_data = [x  for x in bill_obj.product_key.all().values('name','price','quantity').annotate(total_product_price = Sum(F('price') * F('quantity')))]

    amount_word = num2words(bill_obj.bill_amount, to='cardinal', lang='en_IN')


    context = {
        'id':bill_obj.id,
        'date':bill_obj.create_at,
        'bill_number':bill_obj.bill_number,
        'bill_amount':bill_obj.bill_amount,
        'product_data':product_data,
        'amount_word':amount_word,
    }


    pdf_obj = render_to_pdf('pdf_file.html',context)


    return HttpResponse(pdf_obj,content_type="application/pdf")
    
import time 

class CreateBill(LoginRequiredMixin, TemplateView):
    template_name = 'create_bill.html'

    def post(self, request, *args, **kwargs):

        # driver = webdriver.Chrome()

        # driver.get("https://api.whatsapp.com/send?phone=919104370665")

        
        
        # time.sleep(50)


        # return HttpResponse("heyyyyyyyyyyyy")


        run_loop = self.request.POST['loop']



        amount = 0

        products = []

        for i in range(int(run_loop)):

            i += 1 

            product_name = request.POST['pname'+str(i)]
            product_quantity = request.POST['pquantity'+str(i)]
            product_price = request.POST['pprice'+str(i)]

            total_cost = int(product_price) * int(product_quantity)

            amount += total_cost 

            products.append(ProductDescription.objects.create(name = product_name, price = product_price, quantity = product_quantity))

        bill_obj = Bill.objects.create(bill_amount = amount)
        
        bill_obj.product_key.add(*products)

        return HttpResponseRedirect(reverse('bill', kwargs={ 'pk': bill_obj.id }))

class ProductBillDetail(LoginRequiredMixin, DetailView):
    model = Bill
    template_name='index.html'       



class ProductBillUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'edit_bill'
    model = Bill


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return redirect('login')    


    return render(request, 'login.html')



from django_datatables_too.mixins import DataTableMixin
from django.db.models import Q

class DataTablesAjaxPagination(DataTableMixin, View):
    model = Bill
    queryset = Bill.objects.all()

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        return f'<a href="{obj.get_update_url()}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-pencil"></i></a> <a data-title="{obj}" title="Delete" href="{obj.get_delete_url()}" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash"></i></a>'

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(bill_number__icontains=self.search) |
                Q(bill_amount__icontains=self.search) 
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append({
                'bill_number': o.bill_number,
                'bill_amount': o.bill_amount,
                'actions': self._get_actions(o)
            })
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)    