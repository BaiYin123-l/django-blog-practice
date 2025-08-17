#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

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
