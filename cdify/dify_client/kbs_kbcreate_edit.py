import os
import sys
import json

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger


def edit_db(dataset_id, data):
    url = SERVER_BASE_URL + f"/datasets/{dataset_id}"
    response = requests.patch(url, headers=db_hearders, json=data)
    
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    return response


def create_db_new(db_name):
    url = SERVER_BASE_URL + "/datasets"
    response = requests.post(url, headers=db_hearders, json={"name":db_name})

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response


def create_db_old(data):
    # SERVER_BASE_URL = 'http://10.30.30.97/v1'
    url = SERVER_BASE_URL + "/datasets"
    response = requests.post(url, headers=db_hearders, json=data)
    # print(11111)
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    return response
