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

urlpatterns = [
  url(r'^$', TemplateView.as_view(template_name='index.html'), name='uHome'),
  path('api/v1/authentication/', include('authentication.urls')),
  path('api/v2/group/', include('group.urls')),
  path('spending/', include('spending.urls')),
  path('api/v4/spending_history/', include('spending_history.urls')),
  path('fund/', include('fund.urls'))

]

urlpatterns += staticfiles_urlpatterns()
