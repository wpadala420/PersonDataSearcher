from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import requests
from geopy.geocoders import Here
import shutil

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


print(get_exif('/home/wojciech/osint/PersonDataSearcher/tmp/fbmeta.jpg'))