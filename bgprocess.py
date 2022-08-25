from rembg import remove
import json
from PIL import Image
import requests
from io import BytesIO
from abo5s3 import save_uploadedfile
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
import mimetypes
import s3fs
import os
import datetime
import psycopg2
import gc

conn=psycopg2.connect("postgresql://hkmuctkbhmlhsr:59563300aab6c650f8bbc9cc4153df6a42054b71e9be00dda420f40bbbf791b2@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dd8a5bspvhrk8c") 
curr=conn.cursor()

os.environ["AWS_DEFAULT_REGION"] = 'us-east-2'
os.environ["AWS_ACCESS_KEY_ID"] = 'AKIARLFEN3ZYTWBVYNX7'
os.environ["AWS_SECRET_ACCESS_KEY"] = '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'


s3 = boto3.client('s3')
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='AKIARLFEN3ZYTWBVYNX7',
    aws_secret_access_key='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'
)


Purl=[]

s3_url="https://abo5.s3.eu-central-1.amazonaws.com/"
print(Purl)
print(Purl)

#function to remove BG from images and return image format to be uploaded in s3 
def addwhitebg(img):
            img1 = Image.open(r"bgimage.png")
            #BG Removal
            img2 = img
            og=img.copy()

            img2 = img2.crop(img2.getbbox())

            maxsize=int(max(img2.size)*1.5)
            img1=(img1.resize((maxsize,maxsize),Image.ANTIALIAS))
            img_w, img_h = img2.size
            bg_w, bg_h = img1.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
            img1.paste(img2, offset, mask = img2)
            img1=img1.resize((1000,1000),Image.ANTIALIAS)
            img1.save("converted.png", format="png")
            return(img1)

def pushtos3(img):
    #name for the image
     img.save("temp.png")
     name="R"+str(datetime.datetime.now())
     name=name.replace(".","")
     name=name.replace(":","")
     name=name.replace(" ","")
     name=name+"."+"png"
     #push the image to s3
     s3.Bucket('abo5').upload_file(Filename="temp.png", Key=name)
     print("pushtos3")
     return(s3_url+name)



def pushdbupdate(Rurls,purl):
    sql_select_query = """UPDATE master_product_table SET "Product_image_P_url" = %s WHERE "Product_image_R_url" = %s"""
    print("__Purl__")
    purl=",".join(purl)
    curr.execute(sql_select_query, (purl,Rurls,))
    conn.commit()
    print("pushdb completed")



def bgremove(urls):
    print(urls)
    Purl=[]
    for url in urls:
        response = requests.get(url)
        img=Image.open(BytesIO(response.content))
        img=remove(img) 
        img=addwhitebg(img)
        link=pushtos3(img)
        del(img)
        Purl.append(link)
    print("bgremove completed")
    return(Purl)   
        #add white BG

def bgprocess(rurl):
    print("rurl  :")
    print(rurl)
    print("_________rurl__________")
    print(rurl)
    Rurls=rurl
    print("_________Rurl__________")
    print(Rurls)
    urls=Rurls.split(", ")
    Purl=bgremove(urls)
    print("_________PURL_________")
    print(Purl)
    pushdbupdate(Rurls,Purl)
    gc.collect()

    print("completed operation")
    return("done")
    
