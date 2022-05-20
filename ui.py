from bokeh.layouts import widgetbox, layout
from bokeh.layouts import widgetbox as wb, layout
from bokeh.plotting import curdoc
from bokeh.io import show, curdoc
from bokeh.models.widgets import Select, RadioButtonGroup, TextInput, Button
from bokeh.models import widgets as wd, ColumnDataSource
from bokeh.core.properties import value

import string
import mysql.connector

# SQL FIELD
sqlConn = mysql.connector.connect(user='root',
                                  password='erg3010',
                                  host='localhost',
                                  database='newdb')

tsql = "SELECT * FROM newdb.bridge_condition"
with sqlConn.cursor(dictionary=True) as cursor:
    cursor.execute(tsql)
    columns = cursor.fetchall()
col = []
for column in columns:
    key_list = list(column)
for key in key_list:
    col.append(wd.TableColumn(field=key, title=key))
table = wd.DataTable(source=ColumnDataSource(), columns=col, width=1200)
rowData = dict()
for key in key_list:
    rowData[key] = [column[key] for column in columns]
table.source.data = rowData

def getTableDropdown():
    tsql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='newdb'"
    with sqlConn.cursor(dictionary=True) as cursor:
        cursor.execute(tsql)
        rows = cursor.fetchall()
    dropList = []
    for row in rows:
        dropList.append(row["TABLE_NAME"])
    drop.options = dropList 

drop = Select(title = "Select Table Here", options = [], name="", value = "bridge_condition")

def onChange(attr, old, new, name = None):
    if (drop.value == "bridge_condition"):
        tsql = "SELECT * FROM newdb.bridge_condition"
    elif (drop.value == "bridge_desc"):
        tsql = "SELECT * FROM newdb.bridge_desc"
    elif (drop.value == "bridge_improvement"):
        tsql = "SELECT * FROM newdb.bridge_improvement"
    elif (drop.value == "bridge_location"):
        tsql = "SELECT * FROM newdb.bridge_location"
    elif (drop.value == "bridge_span"):
        tsql = "SELECT * FROM newdb.bridge_span"
    elif (drop.value == "owner_info"):
        tsql = "SELECT * FROM newdb.owner_info"
    elif (drop.value == "span_design_info"):
        tsql = "SELECT * FROM newdb.span_design_info"
    elif (drop.value == "span_material_info"):
        tsql = "SELECT * FROM newdb.span_material_info"
    elif (drop.value == "state_info"):
        tsql = "SELECT * FROM newdb.state_info"
    with sqlConn.cursor(dictionary=True) as cursor:
        cursor.execute(tsql)
        columns = cursor.fetchall()
    col = []
    for column in columns:
        key_list = list(column)
    for key in key_list:
        col.append(wd.TableColumn(field=key, title=key))
    table.columns = col
    rowData = dict()
    for key in key_list:
        rowData[key] = [column[key] for column in columns]
    table.source.data = rowData
    return table.source.data

getTableDropdown()
drop.on_change("value",onChange)

page = layout(
    children = [[wb(drop),[wb(table)]]],
    sizing_mode = "fixed"
)

curdoc().add_root(page)
