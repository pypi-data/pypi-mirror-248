from starco.utils import path_maker,zipfolder,unziper
import os,shutil
from starco.tlg.app.utils import get_number
from starco.tlg.bot.util.enum import *
import time
from starco.tlg.app import TlgApp

def SpamBot_req(number):
    tlg = TlgApp(number)
    time.sleep(1)
    status,_=tlg.get_account_status()
    if status!='ban':
        tlg.disconnect()
        return
    time.sleep(2)
    tlg.get_telegram_code
    tlg.send_message('SpamBot','Submit a complaint')
    time.sleep(2)
    tlg.send_message('SpamBot','No, I’ll never do any of this!')
    time.sleep(7)
    pm='Dear Telegram Support!\nMy Telegram Account has been spammed suddenly and I cannot sent message to any contacts whom I don’t have their number and I want you to help me and fix the issue and remove my number from blacklist.'
    tlg.send_message('SpamBot',pm)
    tlg.disconnect()

def backup_database(self,chat_id=''):
    path = self.db.path
    database_dir = path_maker(['database'])
    shutil.copy2(path,database_dir)
    zip_path = path_maker([],'.')+'/database.zip'
    zipfolder(zip_path,database_dir)
    with open(zip_path,'rb') as f:
        if chat_id=='':chat_id = self.super_admin
        self.bot.send_document(chat_id, f)
    try:os.remove(zip_path)
    except:pass
    try:shutil.rmtree(database_dir)
    except:pass

def copy_ready_session(zip_path,saved_before):
    rootdir=path_maker(['zipdir'],'.')
    unziper(zip_path,rootdir)
    sessions={}
    for root, subdirs, files in os.walk(rootdir):
        for filename in files:
            number = get_number(filename)
            if number in saved_before:
                print('duplicated')
                continue
            if number and number>0:
                file_path = os.path.join(root, filename)
                sessions[number]=sessions.get(number,{})
                if filename.endswith('.session'):
                    sessions[number]['session']=file_path
                elif filename.endswith('.json'):
                    sessions[number]['json']=file_path
    ow_path=lambda number,x:os.path.join(path_maker(['accounts',number],'.'),f"+{(x.split('/')[-1]).lstrip('+')}")
    print(sessions)
    for number , values in sessions.items():
        if 'session' not in values or 'json' not in values:continue
        print(values['session'],ow_path(number,values['session']))
        print(values['json'],ow_path(number,values['json']))
        shutil.move(values['session'],ow_path(number,values['session']))
        shutil.move(values['json'],ow_path(number,values['json']))

    shutil.rmtree(rootdir)
    os.remove(zip_path)
    return list(sessions.keys())

def get_product(self,id:int,status=CONFIRMED):
    try:
        return self.db.do('products',condition=f"id={id} AND status={status}")[0]
    except:return {}

def get_orders_by_pid(self,pid:int,status=WAITING):
    try:
        return self.db.do('orders',condition=f"pid={pid} AND status={status}")
    except:return []

def get_order(self,id:int,status=WAITING):
    try:
        return self.db.do('orders',condition=f"id={id} AND status={status}")[0]
    except:return {}


