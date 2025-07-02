"""
Cities and destinations data
"""

class CitiesData:
    """All cities and travel data"""

    def __init__(self):
        self.destinations = {
            'Middle East': {
                'Lebanon': ['Beirut', 'Tripoli', 'Sidon', 'Tyre', 'Byblos', 'Baalbek'],
                'UAE': ['Dubai', 'Abu Dhabi', 'Sharjah'],
                'Jordan': ['Amman', 'Petra', 'Aqaba'],
                'Egypt': ['Cairo', 'Alexandria', 'Luxor', 'Sharm El Sheikh']
            },
            'Europe': {
                'France': ['Paris', 'Nice', 'Lyon', 'Marseille'],
                'UK': ['London', 'Edinburgh', 'Manchester', 'Liverpool'],
                'Italy': ['Rome', 'Venice', 'Florence', 'Milan'],
                'Spain': ['Madrid', 'Barcelona', 'Seville', 'Valencia'],
                'Germany': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg']
            },
            'Asia': {
                'Japan': ['Tokyo', 'Kyoto', 'Osaka'],
                'Thailand': ['Bangkok', 'Phuket', 'Chiang Mai'],
                'India': ['Delhi', 'Mumbai', 'Bangalore', 'Goa'],
                'China': ['Beijing', 'Shanghai', 'Hong Kong']
            },
            'Americas': {
                'USA': ['New York', 'Los Angeles', 'Miami', 'Las Vegas', 'San Francisco'],
                'Canada': ['Toronto', 'Vancouver', 'Montreal'],
                'Brazil': ['Rio de Janeiro', 'Sao Paulo'],
                'Mexico': ['Mexico City', 'Cancun', 'Cabo']
            },
            'Africa': {
                'South Africa': ['Cape Town', 'Johannesburg'],
                'Morocco': ['Marrakech', 'Casablanca'],
                'Kenya': ['Nairobi', 'Mombasa']
            },
            'Oceania': {
                'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth'],
                'New Zealand': ['Auckland', 'Wellington', 'Queenstown']
            }
        }

        self.activities = {
            'beach': ['Swimming', 'Snorkeling', 'Beach volleyball', 'Sunset watching'],
            'city': ['City tour', 'Museums', 'Local cuisine', 'Shopping'],
            'adventure': ['Hiking', 'Rock climbing', 'Zip-lining', 'Safari'],
            'cultural': ['Historical sites', 'Local markets', 'Temples', 'Art galleries']
        }

        self.culture_tips = {
            'Lebanon': ['Try mezze and local shawarma', 'Visit souks', 'Respect religious sites'],
            'Japan': ['Remove shoes indoors', 'No tipping', 'Bow when greeting'],
            'France': ['Greet with Bonjour', 'Dress well', 'Late dinners'],
            'default': ['Research local customs', 'Learn basic phrases', 'Respect dress codes']
        }

    def get_all_destinations(self):
        """Get all cities formatted"""
        cities = []
        for region, countries in self.destinations.items():
            for country, city_list in countries.items():
                for city in city_list:
                    cities.append(f"{city}, {country}")
        return sorted(cities)

    def get_activities(self, destination, weather):
        """Get activities for destination"""
        activities = []

        # Beach cities
        beach_cities = ['Miami', 'Phuket', 'Goa', 'Sharm El Sheikh', 'Cancun']
        if any(city in destination for city in beach_cities):
            activities.extend(self.activities['beach'])
        else:
            activities.extend(self.activities['city'])

        # Weather-based
        for day in weather:
            if day['temp'] > 25 and 'rain' not in day['description']:
                activities.append('Outdoor dining')
            elif 'rain' in day['description']:
                activities.append('Indoor shopping')

        return activities[:7]  # Max 7 activities

    def get_culture_info(self, destination):
        """Get cultural information"""
        for country, tips in self.culture_tips.items():
            if country in destination:
                return tips
        return self.culture_tips['default']