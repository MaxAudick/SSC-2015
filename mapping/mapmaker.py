__author__ = 'max'

import csv
import os
import numpy as np
import MySQLdb as mdb
from datetime import datetime as dt


class MyMap:
    def __init__(self, database='test', host='localhost', user='root', passwd='cats'):
        self.database = database
        self.host = host
        self.user = user
        self.passwd = passwd
        self.constraints = {}

    def change_database(self, database, host='localhost', user='root', passwd='cats'):
        self.database = database
        self.host = host
        self.user = user
        self.passwd = passwd

    def update_points(self, table_name, source_path, source_name, unique_vals=[]):
        data_lst = csv_to_lst(source_path, source_name)
        update_database(data_lst, table_name, unique_vals, self.database, self.host, self.user, self.passwd)

    def update_map(self, table_name, write_path, write_name):
        if len(self.constraints) == 0:
            data_lst = retrieve_entire_table(table_name, self.database, self.host, self.user, self.passwd)
        else:
            data_lst = retrieve_table(table_name, self.database, self.host, self.user, self.passwd, self.constraints)
        write_jsvar(data_lst, write_path, write_name)

    def add_constraint(self, constraint_type, constraint):
        if constraint_type in get_constraint_types(self.database, self.host, self.user, self.passwd):
            if constraint_type != 'lat' and constraint_type != 'lon':
                self.constraints[constraint_type] = constraint
        elif constraint_type == 'latlon':
            self.constraints[constraint_type] = constraint
        elif constraint_type == 'time_range':
            self.constraints[constraint_type] = constraint


class LatLonConstraint:
    def __init__(self, lat1=None, lat2=None, lon1=None, lon2=None):
        if lat1 is not None or lat2 is not None:
            if lat1 > lat2:
                self.max_lat = lat1
                self.min_lat = lat2
            else:
                self.max_lat = lat2
                self.min_lat = lat1
        else:
            self.max_lat = None
        if lon1 is not None and lon2 is not None:
            if lon1 > lon2:
                self.max_lon = lon1
                self.min_lon = lon2
            else:
                self.max_lon = lon2
                self.min_lon = lon1
        else:
            self.max_lon = None

    def get_sql_constraint(self):
        sql_str = "("
        if self.max_lat is not None:
            sql_str += "lat>{minlat} AND lat<{maxlat}".format(minlat=self.min_lat,maxlat=self.max_lat)
        if self.max_lat is not None and self.max_lon is not None:
            sql_str += " AND "
        if self.max_lon is not None:
            sql_str += "lon>{minlon} AND lon<{maxlon}".format(minlon=self.min_lon,maxlon=self.max_lon)
        sql_str += ")"
        return sql_str


def csv_to_lst(path, filename):
    lst_data = []
    name_data = {}
    with open(os.path.join(path, filename), 'r') as csv_data:
        rdr = csv.reader(csv_data, csv.Dialect.delimiter)
        first = True
        for line in rdr:
            if first:
                line.append('color')
                first = False
            else:
                if line[6] not in name_data:
                    name_data[line[6]] = random_color()
                line.append(name_data[line[6]])
            lst_data.append(line)
    return lst_data


def lst_to_jsvar(data_lst):
    data_str = 'var dataPoints = ['
    try:
        for line in data_lst:
            data_str += '[{lon}, {lat}, "<p><b>Time:</b> {t}</p><p><b>Course:</b> {crs}</p><p><b>Speed:</b> {spd}</p><p><b>MMSI:</b> {mmsi}</p><p><b>Name:</b> <i>{name}</i></p>", "{color}"], '.format(lat=line[2], lon=line[3], t=str(dt.fromtimestamp(int(line[1]))), crs=line[4], spd=line[5], mmsi=line[6], name=line[7], color=line[8])
    except TypeError, e:
        line = data_lst
        data_str += '[{lon}, {lat}, "<p><b>Time:</b> {t}</p><p><b>Course:</b> {crs}</p><p><b>Speed:</b> {spd}</p><p><b>MMSI:</b> {mmsi}</p><p><b>Name:</b> <i>{name}</i></p>", "{color}"], '.format(lat=line[2], lon=line[3], t=line[1], crs=line[4], spd=line[5], mmsi=line[6], name=line[7], color=line[8])
    data_str = data_str[:len(data_str) - 2] + '];'
    return data_str


def write_jsvar(data_lst, write_path, write_filename):
    data_str = lst_to_jsvar(data_lst)
    with open(os.path.join(write_path, write_filename), 'w') as js:
        js.write(data_str)


def random_color():
    color = "#"
    for i in range(3):
        color_val = np.random.randint(0, 16)
        if color_val > 9:
            color_val = chr(color_val + 87)
        color += str(color_val)
    return color


def get_constraint_types(table_name, database='test', host='localhost', user='root', passwd='cats'):
    db = mdb.connect(host, user, passwd, database)
    cursor = db.cursor()
    cursor.execute("SHOW COLUMNS FROM {table}".format(table_name))
    data_lst = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    return data_lst


def retrieve_entire_table(table_name, database='test', host='localhost', user='root', passwd='cats'):
    db = mdb.connect(host, user, passwd, database)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM {table}".format(table=table_name))
    data_lst = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    return data_lst


def retrieve_table(table_name, database='test', host='localhost', user='root', passwd='cats', cols = [], constraints={}):
    exec_str = "SELECT "
    val1 = True
    for constraint in cols:
        if val1:
            exec_str += str(constraint)
            val1 = False
        else:
            exec_str += "," + str(constraint)
    exec_str += " FROM {table} WHERE ".format(table=table_name)
    val1 = True
    for constraint_type in constraints.keys():
        if constraint_type == 'latlon' or constraint_type == 'time_range':
            val2 = True
            for constraint in constraints[constraint_type]:
                if val2:
                    exec_str += constraint.get_sql_constraint
                    val2 = False
                else:
                    exec_str += " OR "
        else:
            exec_str += "("
            val2 = True
            for constraint in constraints[constraint_type]:
                if val2:
                    exec_str += str(constraint_type) + "=" + str(constraint)
                    val2 = False
                else:
                    exec_str += str(constraint_type) + "=" + str(constraint) + " OR "
            exec_str += ")"
        exec_str += "X"


def update_database(data_lst, table_name, unique_lst=[], database='test', host='localhost', user='root', passwd='cats'):
    db = mdb.connect(host, user, passwd, database)
    cursor = db.cursor()
    val1 = True
    for line in data_lst:
        if val1:
            create_table(cursor, table_name, data_lst[0], data_lst[1], unique_lst)
            val1 = False
        else:
            insert_row(cursor, table_name, data_lst[0], line)
    db.commit()
    cursor.close()
    db.close()


def create_table(cursor, table_name, cols, first_data_lst, unique_lst):
    exec_str = "CREATE TABLE IF NOT EXISTS {name} (ID int NOT NULL AUTO_INCREMENT".format(name=table_name)
    for i in range(len(cols)):
        exec_str += ", {title} {type}".format(title=cols[i], type=get_sql_type(first_data_lst[i]))
    exec_str += ", PRIMARY KEY (ID)"
    if len(unique_lst) > 0:
        exec_str += ", CONSTRAINT unique_set UNIQUE ("
        val1 = True
        for value in unique_lst:
            if val1:
                exec_str += "{val}".format(val=value)
                val1 = False
            else:
                exec_str += ", {val}".format(val=value)
        exec_str += ")"
    exec_str += ")"
    cursor.execute(exec_str)


def insert_row(cursor, table_name, type_lst, data_lst):
    try:
        exec_str = "INSERT INTO {name} (".format(name=table_name)
        val1 = True
        for value in type_lst:
            if val1:
                exec_str += "{val}".format(val=value)
                val1 = False
            else:
                exec_str += ", {val}".format(val=value)
        exec_str += ") VALUE ("
        val1 = True
        for value in data_lst:
            if val1:
                exec_str += "'{val}'".format(val=value)
                val1 = False
            else:
                exec_str += ", '{val}'".format(val=value)
        exec_str += ")"
        cursor.execute(exec_str)
    except:
        return 0


def get_sql_type(val):
    sql_type = str(type(val))
    sql_type = sql_type[7:len(sql_type) - 2]
    if sql_type == 'str':
        if val[0] == '#':
            sql_type = 'char(4)'
        else:
            sql_type = 'varchar(255)'
    return sql_type.upper()


def main():
    map = MyMap('ais_db')
    map.update_points('AISData', '/home/max/internship/mapping', 'aisdata.csv')
    map.update_map('AISData', '/home/max/internship/mapping', 'aisjsvar.js')

main()