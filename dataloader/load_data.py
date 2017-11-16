# -*- coding: utf-8 -*-
import sys
sys.path.append('../img_query_annotation')

import psycopg2
import settings
import numpy as np


###################  DATABASE CONNECTOR ###################################

dbname = settings.DATABASES['default']['NAME']
user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
host = settings.DATABASES['default']['HOST']


conn_str = "dbname='%s' user='%s' host='%s' password='%s'" % (
    dbname, user, host, password)

conn = None
try:
    conn = psycopg2.connect(conn_str)
except:
    print "I am unable to connect to the database"


###################  LOAD IMAGE DATA ###################################
# images_data = open("file_names.csv").readlines()

# np.random.shuffle(images_data)
# cur = conn.cursor()
# for img in images_data[:30000]:
#     img_path = "dataset/%s" % (img.strip())
#     query = "INSERT INTO annotation_image (img_path) VALUES ('%s')" % (
#         img_path)
#     cur.execute(query)

# conn.commit()

################# CREATE POOL ########################################
cur = conn.cursor()


cur.execute("select id from auth_user where username <> 'admin' ")
users_id = [el[0] for el in cur.fetchall()]

cur.execute("select id from annotation_image")
images_id = [el[0] for el in cur.fetchall()]


posi = 0
num_images_per_user = len(images_id) / len(users_id)


for user_id in users_id[:-1]:
    user_images = images_id[posi: posi + num_images_per_user]

    for user_image in user_images:
        query = "INSERT INTO annotation_poolitem (image_id, user_id, is_done) VALUES (%d,%d,false)" % (
            user_image, user_id)
        cur.execute(query)

    conn.commit()
    posi += num_images_per_user

# last user
for user_image in images_id[posi:]:
    query = "INSERT INTO annotation_poolitem (image_id, user_id, is_done) VALUES (%d,%d,false)" % (
        user_image, users_id[-1])
    cur.execute(query)

conn.commit()


cur.close()
conn.close()
