import requests
from tqdm.notebook import tqdm_notebook as tqdm_
import time

import ipywidgets as widgets
from IPython import display as dsp

name = widgets.Text(
    value='',
    placeholder='Имя',
    description='Имя:',
    disabled=False
)
mail = widgets.Text(
    value='',
    placeholder='mail',
    description='e-mail:',
    disabled=False
)

phone = widgets.Text(
    value='',
    placeholder='телефон',
    description='Телефон:',
    disabled=False
)
btn_access = widgets.Button(
    description='Забронировать',
    disabled=False,
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Забронировать',
    icon='check'
)

btn_reload = widgets.Button(
    description='Заново',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Заново',
    icon='check'
)

btn_send = widgets.Button(
    description='Сохранить',
    disabled=False,
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Сохранить',
    icon='check'
)

def btn_reload_clicked(b):
  dsp.clear_output(wait=True)
  Start_levels(idx)

def btn_access_clicked(b):    
  dsp.clear_output(wait=True)
  booking()  

def btn_send_clicked(b):
  btn_send.disabled = True
  send()

btn_reload.on_click(btn_reload_clicked)
btn_access.on_click(btn_access_clicked)
btn_send.on_click(btn_send_clicked)

bonuses = []
current_cost = []
idx = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def work(progress):
  print('Выбор бонуса')
  total = 100
  for i in range(total):
      time.sleep(0.05)
      progress.value = float(i+1)/total

def booking():
  dsp.clear_output(wait=True)
  print(f'{bcolors.OKGREEN}{bcolors.BOLD}Поздравляем!', end=' ')
  print(f'Ваш список бонусов:{bcolors.ENDC}')
  for b in bonuses:    
      print(f'- {b}')
  print()
  btn_send.disabled = False
  print(f'{bcolors.UNDERLINE}Вам выпало бонусов на {current_cost} руб.{bcolors.ENDC}')
  display(name)
  display(mail)
  display(phone)
  display(btn_send)

def send():  
  res_save= '/save'
  url='https://d5dttm7ipl4ef12lussv.apigw.yandexcloud.net' 
  res = requests.post(f'{url}{res_save}', params={'idx':idx,'email': mail.value, 'name':name.value, 'phone': phone.value, 'bonus': "• "+ "\n• ".join(bonuses)})
  print()
  if res.status_code==200:    
    print(f'{bcolors.HEADER}Отлично, эти подарки теперь забронированы за вами!')
    print('Скоро мы вам позвоним :)')
  else:
    res = requests.post(f'{url}{res_save}', params={'idx':idx, 'email': mail, 'name':name, 'phone': phone, 'bonus': "• "+ "\n• ".join(bonuses)})
    if res.status_code==200:    
      print(f'{bcolors.HEADER}Отлично, эти подарки теперь забронированы за вами!')
      print('Скоро мы вам позвоним :)')
    else:
      res = requests.post(f'{url}{res_save}', params={'idx':idx, 'email': mail, 'name':name, 'phone': phone, 'bonus': "• "+ "\n• ".join(bonuses)})
      if res.status_code==200:    
        print(f'{bcolors.HEADER}Отлично, эти подарки теперь забронированы за вами!')
        print('Скоро мы вам позвоним :)')
      else:
        print(f'{bcolors.FAIL}Ошибка сервера! Обратитесь, пожалуйста, к менеджерам УИИ')

def Start_levels(_idx):
    global idx, bonuses, current_cost    
    btn_reload.disabled = False
    btn_access.disabled = False
    btn_send.disabled = False
    idx = _idx
    dsp.clear_output(wait=True)
    url='https://d5dttm7ipl4ef12lussv.apigw.yandexcloud.net'
    res_url='/numbers'    
    res_save= '/save'
    res = requests.get(f'{url}{res_url}', params={'idx': idx})
    progress = widgets.FloatProgress(value=0.0, min=0.0, max=1.0)
    presents=['']
    cost=0
    if idx==-1:
        presents = ['5 zoom консультаций',
                    '10 zoom консультаций',
                    '20 zoom консультаций',
                    '1 стажировка (3 месяца)',
                    '2 стажировки (6 месяцев)',
                    '4 стажировки (12 месяцев)',
                    'Курс по трейдингу (6 занятий) + стажировка',
                    'Курс по обработке данных и алгоритмам (14 занятий)',
                    'Курс по PyTorch (10 занятий)',
                    'Выкуп стоимости обучения',
                    'Скидка 5.000 рублей',
                    'Скидка 10.000 рублей',
                    'Скидка 20.000 рублей',]
        cost = [9500, 14900, 29800, 14900, 24900, 39900, 39900, 39900, 39900, 39900, 5000, 10000, 20000]    
    elif idx in [0, 10, 40]:
        presents = ['Выкуп стоимости',
                    '5 zoom консультаци',
                    '10 zoom консультации',
                    'Бонусы - 5.000р',
                    'Бонусы - 10.000р',
                    '1 стажировка',]
        cost = [39900, 9500, 14900, 5000, 10000, 14900]    
    elif idx in [1, 11, 41]:
        presents = ['Курс на выбор',
                    'Выкуп стоимости',
                    '5 zoom консультаци',
                    '10 zoom консультации',
                    '20 zoom консультации',
                    'Бонусы - 5.000р',
                    'Бонусы - 10.000р',
                    'Бонусы - 20.000р',
                    '1 стажировка',
                    '2 стажировки',]
        cost = [39900, 39900, 9500, 14900, 29800, 5000, 10000, 20000, 14900, 24900]
    elif idx in [2, 12]:
        presents = ['Курс на выбор',                    
                    '5 zoom консультаци',
                    '10 zoom консультации',
                    '20 zoom консультации',
                    'Бонусы - 5.000р',
                    'Бонусы - 10.000р',
                    'Бонусы - 20.000р',
                    '1 стажировка',
                    '2 стажировки',]
        cost = [39900, 9500, 14900, 29800, 5000, 10000, 20000, 14900, 24900]
    elif idx in [33]:
        presents = ['2 zoom консультации',                    
                    '5 zoom консультаций',
                    '10 zoom консультаций',
                    '20 zoom консультаций',
                    '1 стажировка',
                    '2 стажировки',
                    'Бонусы - 5.000р',
                    'Бонусы - 10.000р',
                    'Бонусы - 20.000р',]
        cost = [5800, 9500, 14900, 24900, 19900, 24900, 5000, 10000, 20000]
    elif idx in [50, 60, 70]:
        presents = ['Выкуп стоимости',
                    '5 zoom консультаци',
                    '10 zoom консультации',
                    'Бонусы - 5.000р',
                    'Бонусы - 10.000р',
                    '1 стажировка',
                    'Скидка на курс']
        cost = [39900, 9500, 14900, 5000, 10000, 14900, 5000] 
    elif idx in [51, 61, 71]:
        presents = ['Выкуп стоимости',
                    '5 zoom консультаци',
                    '10 zoom консультации',
                    '20 zoom консультации',
                    'Бонусы - 5.000р',
                    'Бонусы - 10.000р',
                    'Бонусы - 20.000р',
                    '1 стажировка',
                    '2 стажировки',
                    'Скидка на курс']
        cost = [39900, 9500, 14900, 29800, 5000, 10000, 20000, 14900, 24900, 10000]

    current_variant =  [int(value)  for value in res.json().values()]
    bonuses = []
    num_bonus = 1
    print(f'{bcolors.BOLD}Готовимся выбирать бонусы...{bcolors.ENDC}')
    time.sleep(1)
    dsp.clear_output(wait=True)
    current_cost = 0
    for i, elem in enumerate(current_variant):
        if elem:          
          #for _ in tqdm_(range(60), desc=f'Выбор бонуса №{num_bonus}', ncols=500):
          #    time.sleep(0.05)
          dsp.display(progress)
          work(progress)
          num_bonus+=1
          current_cost += cost[i]
          current_present = f'{bcolors.OKBLUE}Бонус:{bcolors.ENDC} {presents[i]} ({cost[i]} руб.)'
          print(current_present)
          time.sleep(1)
          dsp.clear_output(wait=True)
          bonuses.append(f'{presents[i]} ({cost[i]} руб)')
          print(f'{bcolors.OKGREEN}{bcolors.BOLD}Поздравляем!', end=' ')
          print(f'Ваш список бонусов:{bcolors.ENDC}')
          for b in bonuses:    
              print(f'- {b}')
    print()
    print(f'{bcolors.UNDERLINE}Вам выпало бонусов на {current_cost} руб.{bcolors.ENDC}')
    print()
    print()
    print(f'Вам нравится такой бонус?')
    display(widgets.HBox((btn_access, btn_reload)))   
