from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.db.models import Q

from django.urls import reverse
from django.contrib import auth
from django.conf import settings


import requests
import asyncio, aiohttp
import numpy as np
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ToyotaModels, Estimate, APICallCounter
from .utils import CarbonInterfaceAPI
# Create your views here.
  

 
class ToyotaModelListView(LoginRequiredMixin, View):
    def __init__(self) -> None:
        self.template_name = 'carbon/view_emission.html'
        self.none_str = "0"

    def get(self, request):
        unique_objects_count = ToyotaModels.objects.distinct().count()

        if unique_objects_count == 0:
            ci = CarbonInterfaceAPI()
            toyota_make_id = "2b1d0cd5-59be-4010-83b3-b60c5e5342da"
            endpoint = 'vehicle_makes/' + toyota_make_id + '/vehicle_models'
            response = requests.get(ci.api_url + endpoint, headers=ci.headers)
            data = response.json()

            counter, created = APICallCounter.objects.get_or_create(
            defaults={'call_count': 0}  # Default to 0 if not exists, then add 1 next
            )
            
            # Increment the call count
            counter.call_count += 1
            counter.save()  # Don't forget to save the changes

            for item in data:
                attributes = item['data']['attributes']
                ToyotaModels.objects.create(
                id=item['data']['id'],
                name=attributes['name'],
                year=attributes['year'],
                vehicle_make=attributes['vehicle_make'],
                )

        
        #messages.success(request, 'Dropdowns populated from database')
        self.unique_years = ToyotaModels.objects.values_list('year', flat=True).distinct().order_by('year')
        self.unique_models = ToyotaModels.objects.values_list('name', flat=True).distinct().order_by('name')
        

        return render(request, self.template_name, {
            'unique_years': self.unique_years,
            'unique_models': self.unique_models,
        })
    
    def post(self, request):

        self.unique_years = ToyotaModels.objects.values_list('year', flat=True).distinct().order_by('year')
        self.unique_models = ToyotaModels.objects.values_list('name', flat=True).distinct().order_by('name')
        

        year = request.POST['selected_year']
        model = request.POST['selected_model']
        units = request.POST['selected_units']

        html_options = {
            "carbon_lb": " Pounds (lb)",
            "carbon_kg": " Kilograms (kg)",
            "carbon_mt": " Metric Tonne (mt)",
            "carbon_g": " Grams (g)"
        }
        
        unit_info = html_options[units]

        if year != self.none_str and model != self.none_str and units != self.none_str: 
            table_list = ToyotaModels.objects.filter(year=year, name=model).values_list('id', flat=True)
            query_list = ToyotaModels.objects.filter(Q(year=year) | Q(name=model)).values_list('id', flat=True)

            type_value = "vehicle"
            distance_unit_value = "km"
            distance_value = 100

            counter, created = APICallCounter.objects.get_or_create(
                    defaults={'call_count': 0}  # Default to 0 if not exists, then add 1 next
                    )

            for model_id in query_list:
                ci = CarbonInterfaceAPI()
                
                if not Estimate.objects.filter(vehicle_model_id=model_id, distance_unit = distance_unit_value, distance_value = distance_value).exists():
                    
                    json_data = {
                        "type": type_value,
                        "distance_unit": distance_unit_value,
                        "distance_value": distance_value,
                        "vehicle_model_id": model_id,
                    }

                    response = requests.post(
                        "https://www.carboninterface.com/api/v1/estimates", headers=ci.headers, json=json_data
                    )

                    
                    
                    # Increment the call count
                    counter.call_count += 1
                    counter.save()  # Don't forget to save the changes

                    # Load JSON response
                    response_data = response.json()

                    try:
                        if type(response_data) == 'list':
                            if len(response_data) != 0:
                                id_list = [response_data[i]['data']['id'] for i in range(len(response_data))]

                                for i, id in enumerate(id_list):
                                    if not Estimate.objects.filter(id=id).exists():
                                        data_dict = response_data[i]["data"]

                                        result_dict = {
                                            "id": data_dict["id"],
                                            "type": data_dict["type"],
                                            **data_dict["attributes"]
                                        }

                                        Estimate.objects.create(**result_dict)
                        else:
                            if response.status_code == 201:
                                data_dict = response_data["data"]

                                result_dict = {
                                    "id": data_dict["id"],
                                    "type": data_dict["type"],
                                    **data_dict["attributes"]
                                }

                                Estimate.objects.create(**result_dict)

                    except Exception as e:
                        # Handle the exception here (print or log the error, or take appropriate action)
                        print(f"An error occurred: {e}")

            

            # async def fetch_and_save_estimate(session, ci, model_id):

            #     json_data = {
            #         "type": type_value,
            #         "distance_unit": distance_unit_value,
            #         "distance_value": distance_value,
            #         "vehicle_model_id": model_id,
            #     }
            
            #     if not Estimate.objects.filter(vehicle_model_id=model_id, distance_unit = distance_unit_value, distance_value = distance_value).exists():
                    
            #         async with session.post("https://www.carboninterface.com/api/v1/estimates", headers=ci.headers, json=json_data) as response:
            #             response_data = await response.json()

            #             counter, created = APICallCounter.objects.get_or_create(
            #             defaults={'call_count': 0}  # Default to 0 if not exists, then add 1 next
            #             )
                        
            #             # Increment the call count
            #             counter.call_count += 1
            #             counter.save()  # Don't forget to save the changes

            #             try:
            #                 if type(response_data) == 'list':
            #                     if len(response_data) != 0:
            #                         id_list = [response_data[i]['data']['id'] for i in range(len(response_data))]

            #                         for i, id in enumerate(id_list):
            #                             if not Estimate.objects.filter(id=id).exists():
            #                                 data_dict = response_data[i]["data"]

            #                                 result_dict = {
            #                                     "id": data_dict["id"],
            #                                     "type": data_dict["type"],
            #                                     **data_dict["attributes"]
            #                                 }

            #                                 Estimate.objects.create(**result_dict)

            #                 else:
            #                     if response.status_code == 201:
            #                         data_dict = response_data["data"]

            #                         result_dict = {
            #                             "id": data_dict["id"],
            #                             "type": data_dict["type"],
            #                             **data_dict["attributes"]
            #                         }

            #                         Estimate.objects.create(**result_dict)
                        
            #             except Exception as e:
            #                 # Handle the exception here (print or log the error, or take appropriate action)
            #                 print(f"An error occurred: {e}")
            
            # async def get_estimate_data():
            #     async with aiohttp.ClientSession() as session:
            #         ci = CarbonInterfaceAPI()  # Make sure you have the appropriate setup for CarbonInterfaceAPI

            #         tasks = [fetch_and_save_estimate(session, ci, model_id) for model_id in query_list]

            #         # Run the tasks concurrently
            #         await asyncio.gather(*tasks)

            # asyncio.run(get_estimate_data())
            
                        
            # Filter Estimate objects based on query_list
            filtered_estimates = Estimate.objects.filter(Q(vehicle_year=year) | Q(vehicle_model=model)).filter(distance_unit = distance_unit_value, distance_value = distance_value)

            year_average_val = round(np.array(filtered_estimates.filter(vehicle_year = year).values_list(units, flat=True)).mean(), 2)
            model_average_val = round(np.array(filtered_estimates.filter(vehicle_model = model).values_list(units, flat=True)).mean(), 2)
            selected_emissions = filtered_estimates.filter(vehicle_model = model, vehicle_year =year ).values_list(units, flat=True)

            rows = [[year, model, str(emission) + unit_info] for emission in selected_emissions]
            average_emissions_year = str(year_average_val) + unit_info
            average_emissions_model = str(model_average_val) + unit_info

            info1 = f"The emissions estimates above are calculated based on vehicles travelling {distance_value} {distance_unit_value}. \n"
            info2 = f"Information has been retrieved from the Carbon Interface API. Call count: {counter.call_count}"

            return render(request, 'carbon/view_emission.html', {
                'rows': rows,
                'unique_years': self.unique_years,
                'unique_models': self.unique_models,
                'average_emissions_year': average_emissions_year,
                'average_emissions_model': average_emissions_model,
                'footer_text': info1 + info2,
            })
    

        


