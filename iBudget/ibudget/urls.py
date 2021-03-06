"""iBudget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic import TemplateView
from ibudget.views import FileHandler


urlpatterns = [
  url(r'^$', TemplateView.as_view(template_name='index.html'), name='uHome'),
  path('api/v1/authentication/', include('authentication.urls')),
  path('api/v1/group/', include('group.urls')),
  path('api/v1/spending/', include('spending.urls')),
  path('api/v1/spending_history/', include('spending_history.urls')),
  path('api/v1/fund/', include('fund.urls')),
  path('api/v1/files/', FileHandler.as_view()),
  path('api/v1/income/', include('income.urls')),
  path('api/v1/income_history/', include('income_history.urls')),
  path('api/v1/custom_profile/', include('custom_profile.urls'))
]

urlpatterns += staticfiles_urlpatterns()
