__author__ = 'max'

import csv
import os
import numpy as np
import MySQLdb as mdb
from datetime import datetime as dt


class MyMap:
    def __init__(self, database='test', host='localhost', user='root', passwd='cats'):
        self.constraints = {}
        self.db = mdb.connect(host, user, passwd, database)

    def open_database(self, database, host='localhost', user='root', passwd='cats'):
        self.db = mdb.connect(host, user, passwd, database)

    def update_points(self, table_name, source_path, source_name, unique_vals=[]):
        data_lst = csv_to_lst(source_path, source_name)
        update_database(data_lst, table_name, self.db, unique_vals)

    def update_map(self, table_name, write_path, write_name):
        if len(self.constraints) == 0:
            data_lst = retrieve_entire_table(table_name, self.db)
        else:
            data_lst = retrieve_table(table_name, self.db, self.constraints)
        write_jsvar(data_lst, write_path, write_name)

    def add_constraint(self, constraint_type, constraint):
        if constraint_type in get_constraint_types('AISData', self.db):
            if constraint_type != 'lat' and constraint_type != 'lon':
                try:
                    len(self.constraints[constraint_type])
                    self.constraints[constraint_type].append(constraint)
                except KeyError:
                    self.constraints[constraint_type] = [constraint]
        elif constraint_type == 'latlon':
            try:
                len(self.constraints[constraint_type])
                self.constraints[constraint_type].append(constraint)
            except KeyError:
                self.constraints[constraint_type] = [constraint]
        elif constraint_type == 'time_range':
            try:
                len(self.constraints[constraint_type])
                self.constraints[constraint_type].append(constraint)
            except KeyError:
                self.constraints[constraint_type] = [constraint]

    def close_database(self):
        self.db.close()



class TimeRangeConstraint:
    def __init__(self, starttime, endtime):
        self.start = starttime
        self.end = endtime

    def get_sql_constraint(self):
        sql_str = "("
        if self.start is not None:
            sql_str += "unixtime>=" + str(self.start)
            if self.end is not None:
                sql_str += " AND "
        if self.end is not None:
            sql_str += "unixtime<=" + str(self.end)
        sql_str += ")"
        return sql_str


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
    """
    Returns a list version of a .csv file, given that file's path and name.
    """
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
    """
    Returns a string that can be read as a javascript variable based on data in a list.  Tuned specifically for ships.
    """
    data_str = 'var dataPoints = ['
    try:
        for line in data_lst:
            data_str += '[{lon}, {lat}, "<p><b>Time:</b> {t}</p><p><b>Course:</b> {crs}</p><p><b>Speed:</b> {spd}</p><p><b>MMSI:</b> {mmsi}</p><p><b>Name:</b> <i>{name}</i></p>", "{color}"], '.format(lat=line[2], lon=line[3], t=str(dt.fromtimestamp(int(line[1]))), crs=line[4], spd=line[5], mmsi=line[6], name=line[7], color=line[8])
    except TypeError:
        line = data_lst
        data_str += '[{lon}, {lat}, "<p><b>Time:</b> {t}</p><p><b>Course:</b> {crs}</p><p><b>Speed:</b> {spd}</p><p><b>MMSI:</b> {mmsi}</p><p><b>Name:</b> <i>{name}</i></p>", "{color}"], '.format(lat=line[2], lon=line[3], t=line[1], crs=line[4], spd=line[5], mmsi=line[6], name=line[7], color=line[8])
    data_str = data_str[:len(data_str) - 2] + '];'
    return data_str


def write_jsvar(data_lst, write_path, write_filename):
    data_str = lst_to_jsvar(data_lst)
    with open(os.path.join(write_path, write_filename), 'w') as js:
        js.write(data_str)


def random_color():
    """
    Generates and returns the string of a random color.  Color code is in hex values.
    """
    color = "#"
    for i in range(3):
        color_val = np.random.randint(0, 16)
        if color_val > 9:
            color_val = chr(color_val + 87)
        color += str(color_val)
    return color


def get_constraint_types(table_name, db):
    """
    Returns a list of the column names from a table on a database.
    """
    cursor = db.cursor()
    cursor.execute("SHOW COLUMNS FROM {table}".format(table=table_name))
    data_lst = cursor.fetchall()
    db.commit()
    cursor.close()
    data_lst_out = [val[0] for val in data_lst]
    return data_lst_out


def retrieve_entire_table(table_name, db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM {table}".format(table=table_name))
    data_lst = cursor.fetchall()
    db.commit()
    cursor.close()
    return data_lst


def retrieve_table(table_name, db, constraints={}):
    exec_str = "SELECT "
    val1 = True
    is_cols = True
    try:
        cols = constraints['cols']
    except Exception:
        is_cols = False
    if is_cols:
        for constraint in cols:
            if val1:
                exec_str += str(constraint)
                val1 = False
            else:
                exec_str += "," + str(constraint)
    else:
        exec_str += "*"
    exec_str += " FROM {table} WHERE ".format(table=table_name)
    val1 = True
    for constraint_type in constraints.keys():
        if val1:
            val1 = False
            exec_str = add_constraints_sql(exec_str, constraint_type, constraints)
        else:
            exec_str += " AND "
            exec_str = add_constraints_sql(exec_str, constraint_type, constraints)
    cursor = db.cursor()
    cursor.execute(exec_str)
    data_lst = cursor.fetchall()
    db.commit()
    cursor.close()
    return data_lst


def update_database(data_lst, table_name, db, unique_lst=[]):
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


def create_table(cursor, table_name, cols, first_data_lst, unique_lst):
    """
    Creates a table in a database if that table does not already exist.  Will not modify an already existing table.
    """
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
        return None


def add_constraints_sql(exec_str, constraint_type, constraints):
    """
    Return SQL version of a given constraint.
    """
    exec_str += "("
    if constraint_type == 'latlon' or constraint_type == 'time_range':
        val1 = True
        for constraint in constraints[constraint_type]:
            if val1:
                next_constraint = constraint.get_sql_constraint()
                exec_str += next_constraint
                val1 = False
            else:
                next_constraint = constraint.get_sql_constraint()
                exec_str += " OR " + next_constraint
    else:
        val1 = True
        for constraint in constraints[constraint_type]:
            if val1:
                exec_str += str(constraint_type) + "='" + str(constraint) + "'"
                val1 = False
            else:
                exec_str += " OR " + str(constraint_type) + "='" + str(constraint) + "'"
    exec_str += ")"
    return exec_str


def get_sql_type(val):
    """
    Obtain a value's type, convert it to its SQL equivalent type, and return that SQL equivalent type.
    """
    sql_type = str(type(val))
    sql_type = sql_type[7:len(sql_type) - 2]
    if sql_type == 'str':
        if val[0] == '#':
            if len(val) == 4:
                sql_type = 'char(4)'
            elif len(val) == 16:
                sql_type = 'char(16)'
            else:
                return None
        else:
            if len(val) < 256:
                sql_type = 'varchar(255)'
            else:
                sql_type = 'text'
    return sql_type.upper()


def main():
    mymap = MyMap('ais_db')
    mymap.update_points('AISData', '/home/max/internship/mapping', 'aisdata.csv')
    mymap.add_constraint('shipname', 'SLAVE I')
    mymap.add_constraint('time_range', TimeRangeConstraint(None, 1403713500))
    mymap.add_constraint('time_range', TimeRangeConstraint(1403714500, None))
    mymap.add_constraint('shipname', 'MILLENIUM FALCON')
    mymap.update_map('AISData', '/home/max/internship/mapping', 'aisjsvar.js')
    mymap.close_database()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
