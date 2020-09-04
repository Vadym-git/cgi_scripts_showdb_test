#!/usr/bin/env python3
import sqlite3 as s
import cgi
import os
from tkinter import filedialog

program_name = "Simple reader DB"
version = " v 1.01"
linkfile = "path.txt"


def get_file_link(newpath):
    if newpath == "Choose File":
        global file
        file = filedialog.askopenfilename(filetypes=(("DB files", "*.db"), ("all files", "*.*")))
        file = os.path.normcase(file)
        if file.endswith('.db'):
            wright_newpath(file)
        newpath = os.path.split(file)[-1]
        return newpath


def read_link_file():
    paths = []
    f = open(f"{linkfile}", "r")
    for i in f:
        paths.append(i)
    f.close()
    if len(paths) >= 1:
        paths = (paths[0]).replace("\n", "")
        if os.path.isfile(paths) is True and paths.endswith('.db'):
            return paths
        return False
    return False


def open_DB(path):
    db = s.connect(path)
    cursor = db.cursor()
    data = cursor.execute("""SELECT name FROM sqlite_master WHERE type = 'table'""")
    data = [i for i in data]
    return data, cursor


def print_tables(data, cursor):
    print(f"""<form name='forma1' action='index.py'>Table select:<br>""")
    [print(f'<input type="radio" name="table" value="{i[0]}" checked>{i[0]}<br>') for i in data]
    print("""<input type="submit" name="submit1" value="Submit">
            </form>
        """)
    cursor.close()


def reading_table(cursor, table):
    selection_table = table
    table = cursor.execute(f"""pragma table_info({selection_table})""")
    print(
        f"<table id='data' width='100%' border='1' cellspacing='1'>\n<caption>Table name: {selection_table}</caption>")
    print("<tr>", end="")
    [print(f"<th width='10%' height='5%'>{i[1]}</th>", end="") for i in table]
    print("</tr>", end="")
    for i in cursor.execute(f"""SELECT * FROM {selection_table};"""):
        print("<tr id=row>", end="")
        [print(f"<td id='loaddata'>{k}</td>", end="") for k in i]
        print("</tr>")
    print("</table>")
    cursor.close()


def select_new_db(newpath):
    try:
        if newpath.endswith(".db") == False:
            newpath = "FILE ERROR: " + newpath
    except AttributeError:
        pass
    print(f"""
            <form name="forma0" action='index.py'>
            <table  bgcolor="red" align="center" width='430' border="2" cellspacing="2" cellpadding="5">
            <caption>{program_name}{version}</caption>
                <tr>
                    <td align="center" colspan="2">
                        <label for="load">Need to select db file:</label>
                        <input type="submit" name="load" value="Choose File">
                    </td>
                </tr>
                <tr>
                    <td width='50%'>{newpath}
                    </td>
                    <td align="right" colspan="2" width='50%'>
                        <input type="submit" name="Submit" value="Download">
                    </td>
                </tr>
            </table>
            </form>        
            """)


def wright_newpath(file):
    f = open(linkfile, 'w')
    f.write(file)
    f.close()


def main():
    form = cgi.FieldStorage()
    newpath = form.getfirst(f"load", f"NONE")
    newDB = form.getfirst("Submit2", "None")
    if newDB == "Select new DB":
        wright_newpath(newDB)
    if read_link_file() != False:
        first_table, cursor = open_DB(read_link_file())
        selection_table = form.getfirst(f"table", f"{first_table[0][0]}")
        data, cursor = open_DB(read_link_file())
        print("""<!DOCTYPE html>Content-type: text/html""")
        print()
        print(f"""<html>
                <head>
                    <title>{program_name}{version}</title>
                    <link rel="stylesheet" href="/style.css" />
                </head>
                <body>""")
        print("""<table id='general' border='1'>""")
        print(f"""<caption><table id='chengedb'>
                    <tr>   
                        <td>{program_name}{version}.  File: {os.path.split(read_link_file())[-1]}</td>
                        <td>
                            <form name="change_db" action='index.py'>
                                <input type="submit" name="Submit2" value="Select new DB">
                            </form>
                        </td>
                    </tr>
                </table></caption>
                   <tr><td>""")
        reading_table(cursor, selection_table)
        print("""</td><td id='select_table' valign=top>""")
        print_tables(data, cursor)
        print("""</td></tr>""")
        print("""</table>""")
        print(""" </body>
                </html>""")
    else:
        print("""<!DOCTYPE html>Content-type: text/html""")
        print()
        print(f"""<html>
                        <head>
                            <title>{program_name}{version}</title>
                            <link rel="stylesheet" href="/style.css" />
                        </head>
                <body>""")
        newpath = get_file_link(newpath)
        select_new_db(newpath)
        print(""" </body>
                </html>""")


if __name__ == '__main__':
    main()
