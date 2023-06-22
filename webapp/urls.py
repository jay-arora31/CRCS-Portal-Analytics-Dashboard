"""pragati URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path ,include
from . import views


urlpatterns = [
      path('',views.home,name='home' ),
      path('Barchart/',views.Barchart,name='Barchart' ),
      path('testing/',views.testing,name='testing' ),
      path('barch/',views.barch,name='barch' ),
      path('registered_mscs_by_location/',views.registered_mscs_by_location,name='registered_mscs_by_location' ),
          path('mscs_sector_pie_chart/', views.mscs_sector_pie_chart, name='mscs_sector_pie_chart'),
          path('mscs_state_percentage_chart/', views.mscs_state_percentage_chart, name='mscs_state_percentage_chart'),
          path('mscs_district_percentage_chart/', views.mscs_district_percentage_chart, name='mscs_district_percentage_chart'),
          path('registered_mscs_by_state/', views.registered_mscs_by_state, name='registered_mscs_by_state'),
          path('stacked_area_chart_data_sector/', views.stacked_area_chart_data_sector, name='stacked_area_chart_data_sector'),
          path('stacked_area_chart_data_state/', views.stacked_area_chart_data_state, name='stacked_area_chart_data_state'),
              path('treemap-data/', views.treemap_data, name='treemap_data'),
              path('bubble_map_view/', views.bubble_map_view, name='bubble_map_view'),
              path('filter_view/', views.your_view, name='your_view'),



     

]


