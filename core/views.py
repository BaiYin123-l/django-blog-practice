from time import strftime

from django.shortcuts import render
from django.views import View


# Create your views here.


class BaseView(View):
    context = {
        "runningYear": strftime("%Y"),
    }


class IndexView(BaseView):
    def get(self, request):
        return render(request, "index.html", context=self.context)


class AboutView(BaseView):
    def get(self, request):
        context = self.context
        return render(request, "about.html", context=context)
