import json
import MySQLdb
import pandas as pd
from flask import request

from utils import df_to_geojson
import sqlite3

dbpath = 'data.sqlite'
db = MySQLdb

def get_connection():
    connection = sqlite3.connect(dbpath)
    connection.text_factory = lambda b: b.decode(errors = 'ignore')
    # connection = db.connect(host='localhost',
    #                         user='root',
    #                         password='welcome2020',
    #                         db='c19_rest')
    return connection


def getgovcenters(options):
    if ('geo' in options):
        connection = get_connection()

        df = pd.read_sql(
            "SELECT hospital,address,contact_person,email,phone,state,latitude,longitude FROM gov_test_centers",
            connection)

        cols = ['hospital', 'address', 'contact_person', 'email', 'phone', 'state']
        j1 = df_to_geojson(df, cols)
        print(j1)
        j = json.dumps(j1)
        connection.close()
        return j
    else:
        connection = get_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM gov_test_centers;")
        rows = cursor.fetchall()
        j = json.dumps(rows)

        connection.close()
        return j


def getpricenters(options):
    if ('geo' in options):
        connection = get_connection()

        df = pd.read_sql("SELECT hospital,address,phone,state,latitude,longitude FROM private_test_centers",
                         connection)

        cols = ['hospital', 'address', 'phone', 'state']
        j1 = df_to_geojson(df, cols)
        j = json.dumps(j1)
        connection.close()
        return j
    else:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM private_test_centers;")

        rows = cursor.fetchall()

        j = json.dumps(rows)
        print(j)
        connection.close()
        return j


def addgovcenters():
    connection = get_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        details = request.form
        state = details['state']
        hospital = details['hospital']
        address = details['address']
        contact_person = details['contact_person']
        email = details['email']
        phone = details['phone']
        latitude = details['latitude']
        longitude = details['longitude']

        print(details)
        cursor.execute(
            'INSERT INTO gov_test_centers (state, hospital, address, contact_person, email, phone, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (state, hospital, address, contact_person, email, phone, latitude, longitude))
        connection.commit()
        cursor.close()


def addpricenters():
    connection = get_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        details = request.form
        state = details['state']
        hospital = details['hospital']
        address = details['address']
        phone = details['phone']
        latitude = details['latitude']
        longitude = details['longitude']

        print(details)
        cursor.execute(
            'INSERT INTO private_test_centers (state, hospital, address, phone, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s)',
            (state, hospital, address, phone, latitude, longitude))
        connection.commit()
        cursor.close()
