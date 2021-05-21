from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import requests
from geopy.geocoders import Here
import shutil
import face_recognition
import os

HERE_APIKEY = 'iRjYiufvBGmhk6OvJY0lPcVtvF7aFAe6jTgpXEvO8-s'

def get_exif(path):
    image = Image.open(path)
    image.verify()
    try:
        return image.info['parsed_exif']
    except:
        pass

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val
    return labeled

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")
    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")
            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]
    return geotagging

def get_decimal_from_dms(dms, ref):
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0
    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds
    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    return (lat,lon)


def download_image(url, filename):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(filename, 'wb') as image:
                shutil.copyfileobj(r.raw, image)
    except:
        pass


def get_location_info(filename):
    exif = get_exif(filename)
    if exif:
        geotags = get_geotagging(exif)
        if geotags:
            coords = get_coordinates(geotags)
            if coords:
                geocoder = Here(apikey=HERE_APIKEY)
                return geocoder.reverse("%s,%s" % coords)


def compare_faces(known_image_url, unknown_image_url):
    known_image = face_recognition.load_image_file(known_image_url)
    unknown_image = face_recognition.load_image_file(unknown_image_url)
    known_encodings = face_recognition.face_encodings(known_image)
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    if len(known_encodings) > 0 and len(unknown_encodings) > 0:
        for known in known_encodings:
            for unknown in unknown_encodings:
                results = face_recognition.compare_faces([known], unknown)
                for result in results:
                    if bool(result) is True:
                        return True
    return False


def download_photo(directory, url, filename):
    if url is not None and url != '':
        if os.path.isdir(directory) is False and os.path.exists(directory) is False:
            os.mkdir(directory)
        response = requests.get(url)
        with open(directory + '/' + filename, 'wb') as photo:
            photo.write(response.content)
        return directory + '/' + filename
    else:
        return ''

