import haversine

from functions import image_functions
from modules import Person
from geopy.geocoders import Nominatim

def match_profiles_by_photos(profile1, profile2):
    if len(profile1.facebook) > 0:
        if len(profile2.instagram) > 0:
            if 'profile_photo_path' in profile1.facebook and profile1.facebook['profile_photo_path'] is not None and profile1.facebook['profile_photo_path'] != '':
                if 'profile_photo_path' in profile2.instagram and profile2.instagram['profile_photo_path'] is not None and profile2.instagram['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.facebook['profile_photo_path'], profile2.instagram['profile_photo_path']) is True:
                        return True
                    if len(profile1.facebook['photos_paths']) > 0:
                        for photo in profile1.facebook['photos_paths']:
                            if photo != '' and image_functions.compare_faces(photo, profile2.instagram['profile_photo_path']) is True:
                                return True

                if len(profile2.instagram['posts']) > 0:
                    for post in profile2.instagram['posts']:
                        if 'path' in post and post['path'] is not None and post['path'] != '':
                            if image_functions.compare_faces(profile1.facebook['profile_photo_path'], post['path']) is True:
                                return True
                    if len(profile1.facebook['photos_paths']) > 0:
                        for post in profile2.instagram['posts']:
                            for photo in profile1.facebook['photos_paths']:
                                if 'path' in post and post['path'] is not None and post['path'] != '' and photo != '' and image_functions.compare_faces(post['path'], photo) is True:
                                    return True
        if len(profile2.twitter) > 0:
            if 'profile_img_path' in profile2.twitter and profile2.twitter['profile_img_path'] is not None and profile2.twitter['profile_img_path'] != '':
                if 'profile_photo_path' in profile1.facebook and profile1.facebook['profile_photo_path'] is not None and profile1.facebook['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.facebook['profile_photo_path'], profile2.twitter['profile_img_path']) is True:
                        return True
                    if len(profile1.facebook['photos_paths']) > 0:
                        for photo in profile1.facebook['photos_paths']:
                            if photo != '' and image_functions.compare_faces(profile2.twitter['profile_img_path'], photo) is True:
                                return True

    if len(profile1.twitter) > 0:
        if 'profile_img_path' in profile1.twitter and profile1.twitter['profile_img_path'] is not None and profile1.twitter['profile_img_path'] != '':
            if len(profile2.instagram) > 0:
                if 'profile_photo_path' in profile2.instagram and profile2.instagram['profile_photo_path'] is not None and profile2.instagram['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.twitter['profile_img_path'], profile2.instagram['profile_photo_path']) is True:
                        return True
                    if len(profile2.instagram['posts']) > 0:
                        for post in profile2.instagram['posts']:
                            if 'path' in post and post['path'] is not None and post['path'] != '':
                                if image_functions.compare_faces(profile1.twitter['profile_img_path'], post['path']) is True:
                                    return True
            if len(profile2.facebook) > 0:
                if 'profile_photo_path' in profile2.facebook and profile2.facebook['profile_photo_path'] is not None and profile2.facebook['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.twitter['profile_img_path'], profile2.facebook['profile_photo_path']) is True:
                        return True
                if len(profile2.facebook['photos_paths']) > 0:
                    for photo in profile2.facebook['photos_paths']:
                        if photo != '' and image_functions.compare_faces(profile1.twitter['profile_img_path'], photo) is True:
                            return True
    if len(profile1.instagram) > 0:
        if len(profile2.twitter) > 0:
            if 'profile_img_path' in profile2.twitter and profile2.twitter['profile_img_path'] is not None and profile2.twitter['profile_img_path'] != '':
                if 'profile_photo_path' in profile1.instagram and profile1.instagram['profile_photo_path'] is not None and profile1.instagram['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.instagram['profile_photo_path'], profile2.twitter['profile_img_path']) is True:
                        return True
                if len(profile1.instagram['posts']) > 0:
                    for post in profile1.instagram['posts']:
                        if 'path' in post and post['path'] is not None and post['path'] != '':
                            if image_functions.compare_faces(post['path'], profile2.twitter['profile_img_path']) is True:
                                return True
        if len(profile2.facebook) > 0:
            if 'profile_photo_path' in profile2.facebook and profile2.facebook['profile_photo_path'] is not None and profile2.facebook['profile_photo_path'] != '':
                if 'profile_photo_path' in profile1.instagram and profile1.instagram['profile_photo_path'] is not None and profile1.instagram['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.instagram['profile_photo_path'], profile2.facebook['profile_photo_path']) is True:
                        return True
                    if len(profile2.facebook['photos_paths']) > 0:
                        for photo in profile2.facebook['photos_paths']:
                            if photo != '' and image_functions.compare_faces(profile1.instagram['profile_photo_path'], photo) is True:
                                return True
                if len(profile1.instagram['posts']) > 0:
                    for post in profile1.instagram['posts']:
                        if 'path' in post and post['path'] is not None and post['path'] != '':
                            if image_functions.compare_faces(post['path'], profile2.facebook['profile_photo_path']) is True:
                                return True
                        if len(profile2.facebook['photos_paths']) > 0:
                            for photo in profile2.facebook['photos_paths']:
                                if photo != '' and image_functions.compare_faces(post['path'], photo) is True:
                                    return True
    return False


def fuse_profiles(profile1, profile2):
    new_profile = Person.Person()
    if len(profile1.facebook) > 0:
        new_profile.facebook = profile1.facebook
    if len(profile1.instagram) > 0:
        new_profile.instagram = profile1.instagram
    if len(profile1.twitter) > 0:
        new_profile.twitter = profile1.twitter
    if len(profile2.facebook) > 0:
        new_profile.facebook = profile2.facebook
    if len(profile2.instagram) > 0:
        new_profile.instagram = profile2.instagram
    if len(profile2.twitter) > 0:
        new_profile.twitter = profile2.twitter
    return new_profile


def profile_used(profiles_used, profile):
    for used in profiles_used:
        if profile is used:
            return True
    return False


def match_companies_from_registries(profile, registry):
    if len(profile.facebook) > 0:
        if len(profile.facebook['friends']) > 0 and len(registry.registries) > 0:
            for organization in registry.registries:
                if len(organization['organizations_data']) > 0:
                    for data in organization['organizations_data']:
                        for friend in profile.facebook['friends']:
                            if data is not None and 'ceo' in data and data['ceo']['name'] == friend:
                                return True


def add_registry_data(profile, data):
    if profile.dateOfBirth == '':
        profile.dateOfBirth = data.dateOfBirth
    if len(profile.names) == 0:
        profile.names = data.names
    if data.registries not in profile.registries:
        profile.registries = data.registries
    if profile.rejestrUrl is None or profile.rejestrUrl == '':
        profile.rejestrUrl = data.rejestrUrl


def get_city_coordinates(city):
    try:
        gc = Nominatim(user_agent='Firefox')
        loc = gc.geocode(city)
        longtitude = ''
        if 'lon' in loc.raw:
            longtitude = loc.raw['lon']
        lattitude = ''
        if 'lat' in loc.raw:
            lattitude = loc.raw['lat']
        return (float(longtitude), float(lattitude))
    except:
        return (0,0)


def calculate_distance_between_cities(loc1, loc2):
    return haversine.haversine(loc1, loc2, unit=haversine.Unit.KILOMETERS)



