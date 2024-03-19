from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from filter.models import File
import csv
import pandas as pd
import os
from io import TextIOWrapper
from utils.infer_data_types import infer_and_convert_data_types
from django.db import IntegrityError, transaction
import time
import json
import ast

SAVE_PATH='./static/'
STATIC_PATH='http://127.0.0.1:8000/static/'

# Create your views here.
# list all file uploaded
def listRecord(request):
    qs=File.objects.values()
    retlist = list(qs)
    return JsonResponse({'success': 1, 'data': retlist})

# get csv content and types by id
def fileDetail(request):
    if request.method == 'GET' and request.GET['id']:
        file_id = request.GET['id']
    
    try:
        file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return  JsonResponse({'sucress': 0,'msg': f'file with id `{file_id}` does not exist'})
    
    return JsonResponse({'success': 1, 'data': {"id":file.id, "type":ast.literal_eval(file.types),"content":read_csv(SAVE_PATH+file.path),"file":STATIC_PATH+file.path}})

# delete csv by id
def delFile(request):
    file_id=None
    if request.method == 'POST' and json.loads(request.body)['id']:
        file_id = json.loads(request.body)['id']
    
    try:
        with transaction.atomic():
            file = File.objects.get(id=file_id)
            file.delete()
            os.remove(SAVE_PATH+file.path)
    except File.DoesNotExist:
        return  JsonResponse({'success': 0,'data': f'file with id `{file_id}` does not exist'})

    qs=File.objects.values()
    retlist = list(qs)
    return JsonResponse({'success': 1,'data':retlist})

# upload file, process, save
# return types, processed csv and its content
def upload(request):

    # get upload csv
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
    try:
        csv_file_wrapper = TextIOWrapper(file, encoding='unicode_escape')
        df = pd.read_csv(csv_file_wrapper,encoding='unicode_escape')
    except Exception as e:
        JsonResponse({'success': 0, 'data': 'errors when read csv'})

    # process csv
    try:
        df = infer_and_convert_data_types(df)
    except Exception as e:
        JsonResponse({'success': 0, 'data': 'errors when process csv'})
    #write into file
    print("\nData types after inference:")
    print(df.dtypes)
    print(df)

    # save processed data in csv
    file_name=file.name.split(".")[0]+'-'+str(int(time.time()))+'.csv'
    #print(file_name)
    try:
        df.to_csv(SAVE_PATH+file_name, index=False,encoding="utf_8")
    except Exception as e:
        JsonResponse({'success': 0, 'data': 'errors when write processed date into file'})

    #save as a record in db
    try:
        record = File.objects.create(name=file.name,path=file_name,types=dtypes_name(df),create_date=int(time.time()))
    except Exception as e:
        JsonResponse({'success': 0, 'data': 'errors when save in db'})

    return JsonResponse({'success': 1, 'data': {"id":record.id, "type":dtypes_name(df),"content":read_csv(SAVE_PATH+file_name),"file":STATIC_PATH+file_name}})



def df_to_list(df):
    list=[]
    #print(df.index.name)
    try:
        list.append(df.columns.tolist())
        list.append(df.values.tolist())
    except Exception as e:
        print(e)
    return list

def read_csv(file_path):
    content=[]
    try:
        reader = csv.DictReader(open(file_path, encoding = 'unicode_escape'))
        content=[row for row in reader]
        # reader = csv.reader(open(file_path, encoding = 'unicode_escape'))
    except Exception as e:
        print(e)
    return content

def dtypes_name(df):
    content=[]
    content.append(df.dtypes.apply(lambda x: x.name).to_dict())
    return content