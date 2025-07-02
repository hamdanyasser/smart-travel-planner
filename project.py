"""
Smart Travel Planner
Main file with required functions
"""

import tkinter as tk
from ui import TravelPlannerUI
from data import CitiesData
from weather import WeatherService
from utils import PDFExporter

class SmartTravelPlanner:
    """Main planner class"""

    def __init__(self):
        self.cities_data = CitiesData()
        self.weather_service = WeatherService()
        self.pdf_exporter = PDFExporter()

    def get_trip_data(self, destination, trip_type, duration):
        """Function 1: Get all trip data"""
        weather = self.weather_service.get_forecast(destination, duration)
        packing = self.generate_packing_list(destination, trip_type, weather, duration)
        budget = self.calculate_budget(destination, trip_type, duration)

        return {
            'destination': destination,
            'trip_type': trip_type,
            'duration': duration,
            'weather': weather,
            'packing': packing,
            'budget': budget,
            'activities': self.cities_data.get_activities(destination, weather),
            'culture': self.cities_data.get_culture_info(destination)
        }

    def generate_packing_list(self, destination, trip_type, weather, duration):
        """Function 2: Generate smart packing list"""
        packing = {
            'Essentials': ['passport', 'visa', 'money', 'phone charger', 'medicines'],
            'Clothes': [],
            'Accessories': []
        }

        # Weather-based items
        avg_temp = sum(d['temp'] for d in weather) / len(weather)
        if avg_temp > 25:
            packing['Clothes'].extend(['shorts', 't-shirts', 'sandals'])
            packing['Accessories'].extend(['sunscreen', 'sunglasses', 'hat'])
        elif avg_temp < 15:
            packing['Clothes'].extend(['jacket', 'warm clothes', 'boots'])
            packing['Accessories'].extend(['gloves', 'scarf'])

        # Trip type items
        trip_items = {
            'Beach': ['swimsuit', 'beach towel'],
            'Business': ['formal wear', 'laptop'],
            'Adventure': ['hiking boots', 'backpack']
        }
        if trip_type in trip_items:
            packing['Accessories'].extend(trip_items[trip_type])

        # Add quantities
        packing['Clothes'].append(f'{min(duration, 7)} days of clothes')

        return packing

    def calculate_budget(self, destination, trip_type, duration):
        """Function 3: Calculate trip budget"""
        # Base costs per day
        base_costs = {
            'Budget': 60,
            'Standard': 120,
            'Luxury': 300,
            'Business': 200
        }

        daily_cost = base_costs.get(trip_type, 120)

        # City multipliers
        expensive_cities = ['Paris', 'London', 'Tokyo', 'New York', 'Dubai']
        cheap_cities = ['Bangkok', 'Cairo', 'Delhi', 'Budapest']

        city = destination.split(',')[0]
        if city in expensive_cities:
            daily_cost *= 1.5
        elif city in cheap_cities:
            daily_cost *= 0.7

        total = daily_cost * duration

        return {
            'daily': round(daily_cost),
            'total': round(total),
            'accommodation': round(total * 0.4),
            'food': round(total * 0.3),
            'activities': round(total * 0.2),
            'transport': round(total * 0.1)
        }

def main():
    """Main function - Entry point"""
    root = tk.Tk()
    planner = SmartTravelPlanner()
    app = TravelPlannerUI(root, planner)
    root.mainloop()

if __name__ == "__main__":
    main()