from googleplaces import GooglePlaces, types, lang
import pprint

pp = pprint.PrettyPrinter(indent=4)

YOUR_API_KEY = 'AIzaSyB8Yg8zsqZfUwinu2c_V8PP7mgBNrp0h8A'

google_places = GooglePlaces(YOUR_API_KEY)

# You may prefer to use the text_search API, instead.
query_result = google_places.nearby_search(location='London')


if query_result.has_attributions:
    print query_result.html_attributions


for place in query_result.places:
    # Returned places from a query are place summaries.
    pp.pprint(place.name)
    pp.pprint(place.geo_location)
    # print place.place_id

    # # The following method has to make a further API call.
    # place.get_details()
    # # Referencing any of the attributes below, prior to making a call to
    # # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    # print place.details # A dict matching the JSON response from Google.
    # print place.local_phone_number
    # print place.international_phone_number
    # print place.website
    # print place.url

