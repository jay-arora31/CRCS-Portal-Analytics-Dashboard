from django.shortcuts import render
from .models import *
import pandas as pd
import numpy as np
import json
from django.http import JsonResponse
from django.db.models import Sum
import itertools

# Create your views here.



def home(request):
    data=CooperativeSociety.objects.all()

    ##=====================Getting Totals of column distinct value=============================================##
    tot_society=data.count()
    df1 = CooperativeSociety.objects.all().values()
    df = pd.DataFrame.from_records(df1)
    total_society = df.shape[0]
    dist_state=df['sector_state'].unique()
    tot_state = np.unique(dist_state).size
    df1 = df[df['sector_district'].notna()]
    dist_district=df1['sector_district'].unique()
    tot_district = np.unique(dist_district).size


    ##====geting area of operation  =======
    df1=df
    df1['Column1'] = df['sector_area_of_operation'].str.split(',')

    # Explode the values into separate rows
    df1 = df1.explode('Column1')

    # Remove leading/trailing whitespaces
    df1['Column1'] = df1['Column1'].str.strip()

    # Get distinct values and skip blank values
    distinct_area = df1.loc[df1['Column1'] != '', 'Column1'].unique()
    distinct_area=distinct_area.size
    ##===================================



    ###++++++++++++++++++++++++++++++++++Bar chart+++++++++++++++++++++++++++++++++##

    queryset = CooperativeSociety.objects.values('sector_registration_date')
    # Convert the queryset to a pandas DataFrame
    df_year = pd.DataFrame.from_records(queryset)

    # Extract the year from the date_of_registration column
    df_year['Year'] = pd.to_datetime(df_year['sector_registration_date']).dt.year

    # Group the data by year and get the count
    countss = df_year['Year'].value_counts().sort_index()
    years = countss.index.astype(str).tolist()
    
    ##==================================End 

    sector_state_counts = CooperativeSociety.objects.exclude(sector_state=None).values('sector_state').annotate(count=Count('sector_state'))

    # Convert the queryset to a pandas DataFrame
    df = pd.DataFrame.from_records(sector_state_counts)

    # Convert the DataFrame to a dictionary
    sector_state_counts_dict = df.set_index('sector_state')['count'].to_dict()
    print(sector_state_counts_dict)
    sector_state_dis = CooperativeSociety.objects.exclude(sector_district__isnull=True).values('sector_district').annotate(count=Count('sector_district'))
    df12 = pd.DataFrame.from_records(sector_state_dis)
    sector_state_counts_dict_dis = df12.set_index('sector_district')['count'].to_dict()


    colors = [
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF',
        '#FF00FF', '#800000', '#008000', '#000080', '#808000',
        '#800080', '#008080', '#808080', '#FFA500', '#FFC0CB',
        '#FFB6C1', '#FFD700', '#ADFF2F', '#00FF7F', '#87CEEB'
    ]
    color_cycle = itertools.cycle(colors)

    data_dict={
        'tot_society':total_society,
        'tot_state':tot_state,
        'tot_district':tot_district,
        'distinct_area':distinct_area,
        'years':years,
        'sector_state_counts':sector_state_counts_dict,
        'color_cycle':color_cycle,
        'sector_state_counts_dict_dis':sector_state_counts_dict_dis
         }

    return render(request,'home.html',data_dict)


def Barchart(request):



    queryset = CooperativeSociety.objects.values('sector_registration_date')
    # Convert the queryset to a pandas DataFrame
    df = pd.DataFrame.from_records(queryset)

    # Extract the year from the date_of_registration column
    df['Year'] = pd.to_datetime(df['sector_registration_date']).dt.year

    # Group the data by year and get the count
    counts = df['Year'].value_counts().sort_index()

    # Prepare the data for Chart.js
    chart_labels = counts.index.astype(str).tolist()
    chart_values = counts.values.tolist()

    data = {
        'labels': chart_labels,
        'data': chart_values,
    }

    return JsonResponse(data)
import json
import numpy as np

def barch(request):
    if request.GET.get('year', None) is not None:
        year = request.GET.get('year')
        queryset = CooperativeSociety.objects.values('sector_registration_date')
        # Convert the queryset to a pandas DataFrame
        df = pd.DataFrame.from_records(queryset)
        df['sector_registration_date'] = pd.to_datetime(df['sector_registration_date'])

        # Filter a specific year (e.g., 2022)
        year_to_filter = int(year)
        filtered_df = df[df['sector_registration_date'].dt.year == year_to_filter]

        # Get the count of each month for the filtered year
        month_counts = filtered_df['sector_registration_date'].dt.month.value_counts().sort_index()

        # Create a list of counts with zeros for missing months
        month_counts_list = [month_counts.get(month, 0) for month in range(1, 13)]
        month_word = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        chart_labels = month_word
        chart_values = [int(count) for count in month_counts_list]  # Convert int64 to int

        data = {
            'labels': chart_labels,
            'data': chart_values,
        }

        return JsonResponse(data)
def testing(request):

    queryset = CooperativeSociety.objects.values('sector_registration_date')

    df = pd.DataFrame.from_records(queryset)

    # Extract the year from the date_of_registration column
    df['Year'] = pd.to_datetime(df['sector_registration_date']).dt.year

    # Group the data by year and get the count
    counts = df['Year'].value_counts().sort_index()
    chart_labels1 = counts.index.astype(str).tolist()

    return render(request,'testing.html',{'chart_labels1':chart_labels1})





def registered_mscs_by_location(request):
    # Query the database to get the count of registered MSCS by district
    counts = CooperativeSociety.objects.values('state_district').exclude(sector__isnull=True).annotate(count=models.Count('id'))

    # Extract the district names and their respective counts
    labels = [entry['state_district'] for entry in counts]
    data = [entry['count'] for entry in counts]

    # Prepare the data for the chart
    chart_data = {
        'labels': labels,
        'data': data,
    }

    return JsonResponse(chart_data)

def mscs_sector_pie_chart(request):


    
    # Retrieve the data from the CooperativeSociety table and calculate MSCS count in each sector
    # Retrieve the data from the CooperativeSociety table
    queryset = CooperativeSociety.objects.values('sector_sector_type')
    
    # Convert the queryset to a pandas DataFrame
    df = pd.DataFrame.from_records(queryset)
    
    # Drop rows with null values in the 'sector' column
    df = df.dropna(subset=['sector_sector_type'])
    
    # Calculate the count of MSCS in each sector
    sector_counts = df['sector_sector_type'].value_counts()
    
    # Calculate the percentage of each sector
    total_count = sector_counts.sum()
    sector_percentages = (sector_counts / total_count) * 100
    
    sector_percentages = sector_percentages.round(0)
    # Prepare the data for the pie chart
    labels = sector_counts.index.tolist()
    data = sector_percentages.values.tolist()
    chart_data = {
        'labels': labels,
        'data': data
    }
    
    return JsonResponse(chart_data)



def mscs_state_percentage_chart(request):
     # Retrieve the data from the CooperativeSociety table
    queryset = CooperativeSociety.objects.all()
    
    # Convert the queryset to a pandas DataFrame
    df = pd.DataFrame.from_records(queryset.values('sector_state'))
    
    # Drop rows with null values in the 'state' column
    df = df.dropna(subset=['sector_state'])
    
    # Calculate the percentage distribution of MSCS across states
    state_percentages = df['sector_state'].value_counts(normalize=True) * 100
    
    # Format the percentages with 1 decimal place
    state_percentages = state_percentages.round(1)
    
    # Prepare the data for the chart
    labels = state_percentages.index.tolist()
    data = state_percentages.values.tolist()
    
    chart_data = {
        'labels': labels,
        'data': data
    }
    
    return JsonResponse(chart_data)


def mscs_district_percentage_chart(request):
     # Retrieve the data from the CooperativeSociety table
    queryset = CooperativeSociety.objects.all()
    
    # Convert the queryset to a pandas DataFrame
    df = pd.DataFrame.from_records(queryset.values('sector_district'))
    
    # Drop rows with null values in the 'state' column
    df = df.dropna(subset=['sector_district'])
    
    # Calculate the percentage distribution of MSCS across states
    state_percentages = df['sector_district'].value_counts(normalize=True) * 100
    
    # Format the percentages with 1 decimal place
    state_percentages = state_percentages.round(1)
    
    # Prepare the data for the chart
    labels = state_percentages.index.tolist()
    data = state_percentages.values.tolist()
    
    chart_data = {
        'labels': labels,
        'data': data
    }
    
    return JsonResponse(chart_data)




import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import CooperativeSociety

@require_GET
def registered_mscs_by_state(request):
    data = CooperativeSociety.objects.values('sector_state', 'sector_registration_date')
    processed_data = {}

    for entry in data:
        state = entry['sector_state']
        registration_date = entry['sector_registration_date'].strftime('%Y-%m-%d')

        if state not in processed_data:
            processed_data[state] = {}

        if registration_date not in processed_data[state]:
            processed_data[state][registration_date] = 0

        processed_data[state][registration_date] += 1

    return JsonResponse(processed_data)

import json
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from .models import CooperativeSociety

def stacked_area_chart_data_sector(request):
    sectors = CooperativeSociety.objects.values_list('sector_sector_type', flat=True).distinct()
    dates = CooperativeSociety.objects.values_list('sector_registration_date', flat=True).distinct().order_by('sector_registration_date')

    data = []
    for sector in sectors:
        sector_data = []
        for date in dates:
            count = CooperativeSociety.objects.filter(sector_sector_type=sector, sector_registration_date__lte=date).count()
            sector_data.append(count)
        data.append(sector_data)

    chart_labels = [date.strftime('%Y-%m-%d') for date in dates]
    chart_data = {
        'labels': chart_labels,
        'datasets': []
    }

    for i, sector in enumerate(sectors):
        dataset = {
            'label': sector,
            'data': data[i]
        }
        chart_data['datasets'].append(dataset)
    
   
    print(chart_data['datasets'].pop())
    return JsonResponse(chart_data)



def stacked_area_chart_data_state(request):
    sectors = CooperativeSociety.objects.values_list('sector_state', flat=True).distinct()
    dates = CooperativeSociety.objects.values_list('sector_registration_date', flat=True).distinct().order_by('sector_registration_date')

    data = []
    for sector in sectors:
        sector_data = []
        for date in dates:
            count = CooperativeSociety.objects.filter(sector_state=sector, sector_registration_date__lte=date).count()
            sector_data.append(count)
        data.append(sector_data)

    chart_labels = [date.strftime('%Y-%m-%d') for date in dates]
    chart_data = {
        'labels': chart_labels,
        'datasets': []
    }

    for i, sector in enumerate(sectors):
        dataset = {
            'label': sector,
            'data': data[i]
        }
        chart_data['datasets'].append(dataset)
    
   
    return JsonResponse(chart_data)


def treemap_data(request):
    data = CooperativeSociety.objects.all().values('sector_sector_type')
    df = pd.DataFrame.from_records(data)
    df = df.dropna(subset=['sector_sector_type'])
    registrations = df['sector_sector_type'].value_counts().reset_index()
    registrations.columns = ['sector_sector_type', 'count']
    treemap_data = []
    for index, row in registrations.iterrows():
        treemap_data.append({
            'id': row['sector_sector_type'],
            'name': row['sector_sector_type'],
            'parent': '',
            'value': row['count']
        })
    return JsonResponse(treemap_data, safe=False)




def bubble_map_view(request):
    cooperative_societies = CooperativeSociety.objects.all()
    return render(request, 'testing.html', {'cooperative_societies': cooperative_societies})


from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import CooperativeSociety

from django.shortcuts import render
from .models import CooperativeSociety
def your_view(request):

    # Retrieve query parameters from the request
    search_query = request.GET.get('search_query', '')
    sector_state = request.GET.getlist('sector_state[]')
    sector_district = request.GET.getlist('sector_district[]')
    sector_area_of_operation = request.GET.getlist('sector_area_of_operation[]')
    sector_sector_type = request.GET.getlist('sector_sector_type[]')
    sector_registration_start_date = request.GET.get('sector_registration_start_date')
    sector_registration_end_date = request.GET.get('sector_registration_end_date')

    # Perform filtering based on the selected values
    queryset = CooperativeSociety.objects.all()

    if search_query:
        queryset = queryset.filter(sector_name__icontains=search_query) | queryset.filter(sector_address__icontains=search_query)

    if sector_state:
        queryset = queryset.filter(sector_state__in=sector_state)

    if sector_district:
        queryset = queryset.filter(sector_district__in=sector_district)

    if sector_area_of_operation:
        queryset = queryset.filter(sector_area_of_operation__in=sector_area_of_operation)

    if sector_sector_type:
        queryset = queryset.filter(sector_sector_type__in=sector_sector_type)

    if sector_registration_start_date:
        queryset = queryset.filter(sector_registration_date__gte=sector_registration_start_date)

    if sector_registration_end_date:
        queryset = queryset.filter(sector_registration_date__lte=sector_registration_end_date)

    # Pagination
    paginator = Paginator(queryset, 5)  # Assuming 10 objects per page
    page_number = request.GET.get('page')
    objects = paginator.get_page(page_number)

    # Retrieve distinct values for filter options
    states = CooperativeSociety.objects.values_list('sector_state', flat=True).distinct()
    districts = CooperativeSociety.objects.exclude(sector_district__isnull=True).values_list('sector_district', flat=True).distinct()
    sector_types = CooperativeSociety.objects.exclude(sector_sector_type__isnull=True).values_list('sector_sector_type', flat=True).distinct()

    areas = CooperativeSociety.objects.values_list('sector_area_of_operation', flat=True).distinct()


    # Prepare context data
    context = {
        'search_query': search_query,
        'sector_state': sector_state,
        'sector_district': sector_district,
        'sector_area_of_operation': sector_area_of_operation,
        'sector_sector_type': sector_sector_type,
        'sector_registration_start_date': sector_registration_start_date,
        'sector_registration_end_date': sector_registration_end_date,
        'states': states,
        'districts': districts,
        'areas': areas,
        'sector_types': sector_types,
        'objects': objects
    }

    return render(request, 'filter.html', context)
