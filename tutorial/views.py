from django.shortcuts import render,HttpResponse
from django.template import loader
# Create your views here.
from django.http import HttpResponseRedirect
from .form import CommentForm
from .ML import predict
from .crawl import get_list
import re
import selenium
def index(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if(re.search(r"https?:\/\/(www\.)?shopee.vn\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",text)):
            try:
                lst_text = get_list(text)
                #print(lst_text)
                lst_pre = predict()
                return render(request, 'tutorial/index2.html',{'tot':lst_pre[0],'xau':lst_pre[1]})
            except selenium.common.exceptions.TimeoutException:
                return render(request, 'tutorial/index1.html',{'error':"* Kiểm tra lại đường link, hãy chắc chắn đó là đường link chi tiết của một sản phẩm shopee"})
            except selenium.common.exceptions.WebDriverException:
                return render(request, 'tutorial/index1.html',{'error':"* Có lỗi xảy ra, kiểm tra lại đường truyền mạng"})
        else:
            return render(request, 'tutorial/index1.html',{'error':"* Vui lòng nhập đúng đường link sản phẩm trên trang Shopee"})
    return render(request, 'tutorial/index1.html')
