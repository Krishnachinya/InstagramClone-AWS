import mysql.connector
from flask import Flask, redirect, url_for, request,render_template
import timeit
import hashlib
import random
import csv
import os
from datetime import date, datetime, timedelta

connection = mysql.connector.connect(user='Krishna@cloudassign8', password='arjun123!',
                              host=' cloudassign8.mysql.database.azure.com',port='3306',
                              database='clouddb')

cursor = connection.cursor(buffered=True,dictionary=True)

app = Flask(__name__)

if connection.is_connected():
    print('Connected to MySQL database')
else:exit(0)

Uploadpathcsv = '/Users/KrishnChinya/Desktop/Images/csv'
Uploadimagepath = '/Users/KrishnChinya/Desktop/Images/images'
Downloadpath = '/Users/KrishnChinya/PycharmProjects/assign8/static'

extension = ['csv','PNG','png','jpg']

add_files = ("INSERT INTO image_details "
               "(File_Name, IMAGE, Image_type, Uploaded_time) "
               "VALUES (%s, %s, %s, %s)")

add_csvvalues = ("INSERT INTO details "
               "(File_Name, classification, ingredients, quantity) "
               "VALUES (%s, %s, %s, %s)")

@app.route('/')
def display():
    return render_template("Display.html", Totalcount='0')

@app.route('/upload')
def upload():
    cursor = connection.cursor()
    # cursor = connection.cursor()
    # cursor.execute(""" SELECT count(*) FROM image_details """)
    # count = cursor.fetchall()
    for (dirpath, dirnames, filenames) in os.walk(Uploadpathcsv):
        for fl in filenames:
            row1 = [];row2 = [];row3 = [];count=0;
            if fl.endswith(tuple(extension)):
                with open(dirpath + '/' + fl, 'rb') as csvf:
                    reader = csv.reader(csvf,delimiter=',')
                    for row in reader:
                        if(count == 0):
                            for r in row:
                                row1.append(r);
                            row1 = filter(None, row1)
                            count = count+1;
                        elif(count == 1):
                            for r in row:
                                row2.append(r);
                            row2 = filter(None, row2)
                            count = count + 1;
                        else:
                            for r in row:
                                row3.append(r);
                            row3 = filter(None, row3)

                    rowlen2 = len(row2)
                    for row in row2:
                        if(len(row1) != rowlen2):
                            row1.append(0)
                        if(len(row3) != rowlen2):
                            row3.append(row3[0])

                with open(Uploadimagepath + '/' + os.path.splitext(fl)[0] + '.jpg', 'rb') as imagefile:
                    i=0;
                    data_files = (os.path.splitext(fl)[0], imagefile.read(), os.path.splitext(fl)[1], datetime.now())
                    # Insert new employee
                    cursor.execute(add_files, data_files)
                    # Insert rows
                    for row in row1:
                        csv_files = (os.path.splitext(fl)[0],row3[i],row2[i],row1[i])
                        cursor.execute(add_csvvalues,csv_files)
                        i = i+1;
    #
    # for (dirpath, dirnames, filenames) in os.walk(Uploadimagepath):
    #     for fl in filenames:
    #         with open(fl, 'rb') as f:
    #             data_files = (fl, file.read(), os.path.splitext(fl)[1], datetime.now())
    connection.commit();
    cursor.close()
    return render_template("Display.html",Totalcount='0')



@app.route('/displayimages',methods=['POST','GET'])
def downloader():
    i = 0
    alldetails = {};
    start_time = timeit.default_timer()
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM image_details """)
    # fetch all of the rows from the query
    data = cursor.fetchall()
    if len(data) > 0:
        for row in data:
            with open(Downloadpath + '/' + row[1] + '.jpg', 'w') as download_file:
                download_file.write(row[2])
                download_file.close()

    cursor.execute(""" SELECT ID,File_Name,Image_type,Uploaded_time FROM image_details """)
    # fetch all of the rows from the query
    data = cursor.fetchall()
    if len(data) > 0:
        for row in data:
            alldetails[i] = row[1];
            i=i+1;
            alldetails[i] = row[1] + '.jpg';
            i = i + 1;
    print alldetails
    cursor.close();
    finish_time = timeit.default_timer() - start_time
    return render_template('DownloadImage.html', result2=alldetails,result=finish_time)

@app.route('/displayimgdetails',methods=['POST','GET'])
def displayimgdetails():
    i = 0
    alldetails = {};
    cursor = connection.cursor()
    if request.method == 'GET':
        filename = request.args.get('filename')
        query = " SELECT * FROM details where File_Name = '" + os.path.splitext(filename)[0] + "'"
        cursor.execute(query)
        # fetch all of the rows from the query
        data = cursor.fetchall()
        if len(data) > 0:
            for row in data:
                alldetails[i] = row[0];
                i = i + 1;
                alldetails[i] = row[1];
                i = i + 1;
                alldetails[i] = row[2];
                i = i + 1;
                alldetails[i] = row[3];
                i = i + 1;
        cursor.close();

        return render_template('DisplayImage.html', result=alldetails)


if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)