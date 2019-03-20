# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.wildworld
users=db.users
world=db.world

globaladmins=[441399484]
admins=[]


try:
    pass

except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(441399484, traceback.format_exc())
    

@bot.message_handler(commands=['start'])
def start(m):
    user=users.find_one({'id':m.from_user.id})
    if user==None:
        users.insert_one(createuser(m.from_user))
        bot.send_message(m.chat.id, 'Игра в разработке. Автор - @Loshadkin.')
    
@bot.message_handler(commands=['myspecies'])
def myspecies(m):
    user=users.find_one({'id':m.from_user.id})
    if user!=None:
        pass
      
@bot.message_handler(commands=['createworld'])
def createworldmessage(m):
    if m.from_user.id in globaladmins:
        try:
            x=int(m.text.split(' ')[1])
            y=int(m.text.split(' ')[2])
            try:
                world.remove({})
                bot.send_message(m.chat.id, 'Старый мир был удалён!')
            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
                bot.send_message(441399484, traceback.format_exc())
            world.insert_one(createworld(x, y))
            msg=bot.send_message(m.chat.id, 'Новый мир (x='+str(x)+', y='+str(y)+') был успешно сгенерирован!')
            if m.chat.id!=441399484:
                bot.send_message(441399484, msg.text)
        except:
            bot.send_message(m.chat.id, 'Неправильно введены аргументы *х* и *у*!\n`/createworld 500 500`', parse_mode='markdown')
    
    
@bot.message_handler(commands=['showpoint'])
def showp(m):
    try:
        x=int(m.text.split(' ')[1])
        y=int(m.text.split(' ')[2])
        drawworld(m.from_user, [x, y])
    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())
        bot.send_message(441399484, traceback.format_exc())
        bot.send_message(m.chat.id, 'Ошибка! Возможны следующие варианты:\n1. Вы указали крайнюю точку, я не смог нарисовать мир вокруг '+
                         'неё в радиусе 2х блоков;\n2. Указаны неверные аргументы. Пример:\n`/showpoint 30 40`', parse_mode='markdown')
    
    
def drawworld(user, point):
    cworld=world.find_one({})
    tree='🌳'
    rock='⚫️'
    hill='⛰'
    hole='🕳'
    bush='☘️'
    lake='🌊'
    null='n'
    symbol=null
    kb=types.InlineKeyboardMarkup()
    x=point[0]
    y=point[1]
    currentx=x-2
    while currentx<x+2:
        buttons=[]
        currenty=y-2
        while currenty<y+2:
            cpos=str(currentx)+' '+str(currenty)
            if cworld[cpos]['object']=='tree':
                symbol=tree
            if cworld[cpos]['object']=='rock':
                symbol=rock
            if cworld[cpos]['object']=='hill':
                symbol=hill
            if cworld[cpos]['object']=='hole':
                symbol=hole
            if cworld[cpos]['object']=='bush':
                symbol=bush
            if cworld[cpos]['object']=='lake':
                symbol=lake
            buttons.append(types.InlineKeyboardButton(text=symbol, callback_data='none'))
            currenty+=1
        kb.add(*buttons)
        currentx+=1
    bot.send_message(user.id, 'Центральная клетка:\nx='+str(x)+', y='+str(y), reply_markup=kb)
    
            
            
def createworld(x, y):
    currentworld={}
    currentx=1
    chance=20
    while currentx<=x:
        currenty=1
        while currenty<=y:
            currentplace=None
            if random.randint(1,100)<=chance:
                currentplace=choiceobject()
            index=str(currentx)+' '+str(currenty)
            place={'object':currentplace,
                  'index':index}
            currentworld.update({index:place})
            currenty+=1
        currentx+=1
        print('x='+str(currentx))
    return currentworld


def choiceobject():
    objects=['tree', 'rock', 'hill', 'hole', 'bush', 'lake'] # bush = куст
    x=random.choice(objects)
    return x

def createuser(user):
    return {
        'name':user.first_name,
        'username':user.username,
        'id':user.id,
        'selfworld':None,
        'species':{},
        'dna':0
    }
        
        

print('7777')
bot.polling(none_stop=True,timeout=600)

