from django.conf import settings
#from models import ToyotaModels, Estimate, APICallCounter

import os, requests

class CarbonInterfaceAPI:
    def __init__(self):

        self.api_url = 'https://www.carboninterface.com/api/v1/'

        self.headers = {
            'Authorization': 'Bearer ' + settings.MY_API_KEY,
            'Content-Type': 'application/json',
        }
    
    def display_response(self, response):
        if response.status_code == 200:
            data = response.json()
            print(data)
            # Process the data as needed
        else:
            print(f"Error: {response.status_code}, {response.text}")    
    
    def get_auth(self, printresults = True):
        endpoint = 'auth/'
        response = requests.get(self.api_url + endpoint, headers=self.headers)
        if printresults:
            self.display_response(response)
            
        return response.json()

    def get_vehicle_makes(self,printresults = True):
        endpoint = 'vehicle_makes/'

        response = requests.get(self.api_url + endpoint, headers=self.headers)

        if printresults:
                self.display_response(response)

        return response.json()

if __name__ == "__main__":

    year = 1984
    model = "Land Cruiser Wagon 4WD"
    units = "carbon_kg"
    type_value = "vehicle"
    distance_unit_value = "km"
    distance_value = 100

    data  = Estimate.objects.filter(vehicle_year = year, vehicle_model = model, distance_unit = distance_unit_value, distance_value = distance_value)
    print(data)


