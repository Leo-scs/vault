#! /usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import json
import os
import os.path
import re
import subprocess


pwd = os.getcwd()


def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    with open(csvFilePath, encoding="ISO-8859-1") as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            jsonArray.append(row)

    with open(jsonFilePath, 'w', encoding="ISO-8859-1") as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)


def create_file(name):
    if(os.path.isfile(f'{pwd}/{name}.csv')):
        if os.path.exists(f'{pwd}/{name}.json'):
            os.remove(f'{pwd}/{name}.json')
        csvFilePath = r'{}/{}.csv'.format(pwd, name)
        jsonFilePath = r'{}/{}.json'.format(pwd, name)
        csv_to_json(csvFilePath, jsonFilePath)
    else:
        print("File is not present!")


def password_format(password):
    new_password = ''
    for caracter in password:
        if "\'" in caracter:
            new_password += caracter.replace("\'", "\'\"\'\"\'")
        else:
            new_password += caracter

    if re.match(r'', new_password):
        new_pass = re.sub(r'^@', '\@', new_password)

    return new_pass


def create_ipmi(name):
    with open(f'{pwd}/{name}.json', 'r') as arq_json:
        data_dict = json.load(arq_json)
        for line in range(len(data_dict)):
            password = password_format(data_dict[line]['Password'])
            output = subprocess.getoutput("vault kv put devices/{}/{} TAG='{}' USER='{}' PASSWORD='{}' IP_IPMI='{}'".format(
                name,
                data_dict[line]['TAG'],
                data_dict[line]['TAG'],
                data_dict[line]['Username'],
                password,
                data_dict[line]['IP IPMI']
            ))
            print(output)


def create_ilo(name):
    with open(f'{pwd}/{name}.json', 'r') as arq_json:
        data_dict = json.load(arq_json)
        for line in range(len(data_dict)):
            password = password_format(data_dict[line]['Password'])
            output = subprocess.getoutput("vault kv put devices/{}/{} TAG='{}' USER='{}' PASSWORD='{}' IP_ILO='{}'".format(
                name,
                data_dict[line]['TAG'],
                data_dict[line]['TAG'],
                data_dict[line]['Username'],
                password,
                data_dict[line]['IP da ILO']
            ))
            print(output)


def create_pdu(name):
    with open(f'{pwd}/{name}.json', 'r') as arq_json:
        data_dict = json.load(arq_json)
        for line in range(len(data_dict)):
            password = password_format(data_dict[line]['Password'])
            output = subprocess.getoutput("vault kv put devices/{}/{}-{}-{} USER='{}' PASSWORD='{}' IP='{}'".format(
                name,
                data_dict[line]['Localidade'],
                data_dict[line]['Rack'],
                data_dict[line]['PDU'],
                data_dict[line]['Username'],
                password,
                data_dict[line]['IP']
            ))
            print(output)


if __name__ == "__main__":
    
    
#    create_asus = subprocess.getoutput("vault secrets enable -path=devices/asus -version=2 kv")
#    print(create_asus)
#    create_file('asus')
#    create_ipmi('asus')

#    create_cisco = subprocess.getoutput("vault secrets enable -path=devices/cisco -version=2 kv")
#    print(create_cisco)
#    create_file('cisco')
#    create_ipmi('cisco')
    
#    create_dell = subprocess.getoutput("vault secrets enable -path=devices/dell -version=2 kv")
#    print(create_dell)
#    create_file('dell')
#    create_ipmi('dell')
    
#    create_huawei = subprocess.getoutput("vault secrets enable -path=devices/huawei -version=2 kv")
#    print(create_huawei)
#    create_file('huawei')
#    create_ipmi('huawei')
    
#    create_lenovo = subprocess.getoutput("vault secrets enable -path=devices/lenovo -version=2 kv")
#    print(create_lenovo)
#    create_file('lenovo')
#    create_ipmi('lenovo')
    
#    create_supermicro = subprocess.getoutput("vault secrets enable -path=devices/supermicro -version=2 kv")
#    print(create_supermicro)
#    create_file('supermicro')
#    create_ipmi('supermicro')
    
#    create_hp = subprocess.getoutput("vault secrets enable -path=devices/hp -version=2 kv")
#    print(create_hp)
#    create_file('hp')
#    create_ilo('hp')
    
#    create_pdus = subprocess.getoutput("vault secrets enable -path=devices/pdus -version=2 kv")
#    print(create_pdus)
#    create_file('pdus')
#    create_pdu('pdus')
