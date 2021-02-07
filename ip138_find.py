#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://user.ip138.com/ 获取token
import requests
import httplib2
from urllib.parse import urlencode  # python3
import re
import json

def parse_jsonp(jsonp_str):
    try:
        return re.search('^[^(]*?\((.*)\)[^)]*$', jsonp_str).group(1)
    except:
        raise ValueError('Invalid JSONP')

def open_ip():
    ip_list = list()
    with open('ips.txt', 'r') as f:
        url = f.readlines()
        for ip in url:
            ip_list.append(ip.replace('\n', ''))
    return ip_list

def open_code():
    code_list = list()
    with open('codes.txt', 'r') as f:
        codes = f.readlines()
        for code in codes:
            code_list.append(code.replace('\n', ''))
    return code_list

def find_information(ip,token):
    params = urlencode({'ip':''+ip+'','datatype':'txt','callback':'find'})
    url = 'https://api.ip138.com/ip/?' + params
    headers = {"token": token}  # token为示例
    response = requests.get(url = url, headers = headers)
    return response.text

def find_weather(code,token):
    params = urlencode({'code': ''+code+'', 'type': '1', 'callback': 'find'})
    url = 'https://api.ip138.com/weather/?' + params
    headers = {"token": token}  # token为示例
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers=headers)
    result_weaher = parse_jsonp(content.decode("utf-8"))
    return result_weaher

if __name__ == '__main__':
    while True:
        choose = str(input("1. 查询ip\n2. 查询天气\n0. 退出\n请输入选择的功能: "))
        if choose == "1":
            token = str(input("输入查询ip的token: "))
            ip_list_find = open_ip()
            for ip in ip_list_find:
                result = find_information(ip,token)
                with open('result_ip.txt','a+',encoding='utf8') as f:
                    f.write(result + '\n')
                    f.close()
            print("-" * 50)
            print('\n')

        if choose == "2":
            token = str(input("输入查询天气的token: "))
            code_list_find = open_code()
            for code in code_list_find:
                result = json.loads(find_weather(code,token))
                with open('result_weather.txt','a+',encoding='utf8') as f:
                    f.write(result['province'] + ' ' + result['city'] + ' ' + result['area'] + ' ' + '\n' + '白天天气: ' + result['data']['dayWeather'] + ' ' + result['data']['dayTemp'] + '度' +' ' + '风力' +result['data']['dayWind'] + '\n' + '夜晚天气: ' + result['data']['nightWeather'] + ' ' + result['data']['nightTemp'] + '度' + ' ' + '风力' + result['data']['nightWind'] + '\n')
                    f.write('实时天气: ' + result['data']['weather'] + ' ' + '风力' + result['data']['wind'] + '\n\n')
                    f.close()
            print("-" * 50)
            print('\n')
        if choose == "0":
            break


