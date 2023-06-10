from pymongo import MongoClient
from hashlib import sha256
from bson import ObjectId
import json

from app import app,db

def criptografar(senha):
    hash_senha=sha256(senha.encode())
    return hash_senha.digest()

def novo_usuario(email,nome,senha,db):
    try:
        banco=db['usuario']
        return banco.insert_one(
            {
                'Email':email,
                'Nome':nome,
                'Senha':criptografar(senha)
            }
        )
        return True
    except:
        return False
    
def cria_alarme(email,db):
    try:
        banco=db['alarme']
        return banco.insert_one(
            {
                'Email':email,
                'Sensor':'Desligado',
                'Buzzer':'Desligado',
                'Status':'Desligado'
            }
        )
        return True
    except:
        return False
    
def atualiza_alarme(Email,estado_status,estado_sensor,estado_buzzer,db):
    try:
        banco=db['alarme']
        banco.update_one(
            {
                'Email':Email
            },
            {'$set':
                {
                    'Sensor':estado_sensor,
                    'Buzzer':estado_buzzer,
                    'Status':estado_status,
                }
            }
        )
        return True
    except:
        return False
    
def valida_usuario(email,senha,db):
    try:
        banco=db['usuario']
        resultado=banco.find({'Email':email,'Senha':criptografar(senha)})
        if resultado!=None:
            return True
        return False
    except:
        return False

def busca_alarme(email, db):
    banco = db['alarme']
    resultado = banco.find({'Email': email})
    if resultado is not None:
        return list(resultado)  
    return []

def alarme(id, db):
    banco = db['alarme']
    resultado = banco.find({'_id': id})
    if resultado is not None:
        return list(resultado)  
    return []