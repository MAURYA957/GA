import requests


def fetch_countries_from_api():
    try:
        # Fetch country data from the REST Countries API
        response = requests.get('https://restcountries.com/v3.1/all')
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)
        countries = response.json()
        country_choices = [(country['name']['common'], country['name']['common']) for country in countries]
        return country_choices
    except Exception as e:
        print(f"Error fetching countries: {e}")
        return []


"""def fetch_states_from_api(country_name):
    try:
        # Fetch state data from the State and District Info API for the given country
        response = requests.get(f'https://restcountries.com/v3.1/all/{country_name}')
        response.raise_for_status()
        states = response.json()
        state_choices = [(state['name'], state['name']) for state in states]
        return state_choices
    except Exception as e:
        print(f"Error fetching states: {e}")
        return []


def fetch_districts_from_api(country_name, state_name):
    try:
        # Fetch district data from the State and District Info API for the given country and state
        response = requests.get(
            f'https://restcountries.com/v3.1/all/{country_name}/{state_name}')
        response.raise_for_status()
        districts = response.json()
        district_choices = [(district['name'], district['name']) for district in districts]
        return district_choices
    except Exception as e:
        print(f"Error fetching districts: {e}")
        return []
        """

State = (
    ("1", "Andhra Pradesh"),
    ("2", "Arunachal Pradesh"),
    ("3", "Assam"),
    ("4", "Bihar"),
    ("5", "Chhattisgarh"),
    ("6", "Goa"),
    ("7", "Gujarat"),
    ("8", "Haryana"),
    ("9", "Himachal Pradesh"),
    ("10", "Jharkhand"),
    ("11", "Karnataka"),
    ("12", "Kerala"),
    ("13", "Madhya Pradesh"),
    ("14", "Maharashtra"),
    ("15", "Manipur"),
    ("16", "Meghalaya"),
    ("17", "Mizoram"),
    ("18", "Nagaland"),
    ("19", "Odisha"),
    ("20", "Punjab"),
    ("21", "Rajasthan"),
    ("22", "Sikkim"),
    ("23", "Tamil Nadu"),
    ("24", "Telangana"),
    ("25", "Tripura"),
    ("26", "Uttar Pradesh"),
    ("27", "Uttarakhand"),
    ("28", "West Bengal"),

)