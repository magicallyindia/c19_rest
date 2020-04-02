import datetime

from dateutil.relativedelta import relativedelta
from pytz import timezone
from tabulate import tabulate


def get_relative_date(zone='UTC', format='%Y-%m-%d', **kwargs):
    tz = timezone(zone)
    time = datetime.datetime.now(tz)
    time_relative = time + relativedelta(**kwargs)
    return time_relative.strftime(format)


def get_clean_table(df):
    message = tabulate(df, headers='keys',
                       tablefmt='html', numalign="center")
    return '<pre>' + message + '</pre>'


def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': 'Point',
                                'coordinates': []}}
        feature['geometry']['coordinates'] = [row[lon], row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson
