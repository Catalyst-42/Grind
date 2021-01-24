import time
import os
from threading import Thread

name = 'Catalyst'
game_exit = 0
money = 0
level = 0
move = ['']

help_text = '''Команды

Команда     - Действие
help        - список действий
enter       - обновить экран
exit        - сохранить игру и выйти
save        - сохранить игру
stats       - статистика
[name]      - показать данные ресурса
sell [name] - продать ресурс
open        - открыть ресурс
up [name]   - улучшение
'''

res_time = {'seconds': 10,
            'minutes': 17,
            'hours': 1,
            'wait_minutes': 0,
            'wait_hours': 0}

res_stone = {'name': 'Камень',
             'count': 50,
             'storage': 100,
             'price': 1,
             'per_s': 0.5,
             'up_cost': 100,
             'level': 0}

res_wood = {'name': 'Дерево',
             'count': 100,
             'storage': 100,
             'price': 5,
             'per_s': 0.5,
             'up_cost': 100,
             'level': 0}

res_coal = {'name': 'Уголь',
             'count': 0,
             'storage': 100,
             'price': 10,
             'per_s': 0.5,
             'up_cost': 100,
             'level': 0}

index = {'Камень': 0,
         'Дерево': 1,
         'Уголь': 2}

buy = [2, 0, 'Камень    : 1 минута; 10 секунд', 'Дерево    : 10 минут; 50 камней', 'Уголь     : 1 час; 100 дерева']
res_all = []

# extension
def pointed_number(number):
    number = round(number)
    if number >= 1000:
        iteration = 3
        iter_dash = 0
        out = str(number)
        while iteration < len(str(number)):
            out = out[:-iteration-iter_dash] + ',' + out[-iteration-iter_dash:]
            iteration += 3
            iter_dash += 1
        return out
    else: return str(number)

def gap(name):
    return (' ' * (15 - len(pointed_number(name))))

def draw_storage(count, max_count):
    percents = round(count / max_count * 100)
    out = '['
    iteration = 0
    for i in range(0, percents // 10):
        iteration += 1
        out += '#'

    while iteration < 10:
        out += '.'
        iteration += 1

    return out+'] ' + str(percents) + '%' + ' ' * (3 - len(str(percents)))

def upgradable(up_cost):
    if money >= up_cost:
        return '|\033[32mo\033[0m|'
    else: return '|\033[31mx\033[0m|'

def draw_name(name):
    return name + ' ' * (10 - len(name)) + ':'

def sell(move):
    global money
    res_id = -1
    if move == 'all':
        for i in res_all:
            money += i['count'] * i['price']
            i['count'] = 0
    else:
        for i in index:
            if move == i:
                res_id = index[i]
                break
    
        for i in index:
            i = index[i]
            if move == str(i + 1):
                res_id = int(i)
                break

        if len(res_all) > res_id and res_id != -1:
            money += res_all[res_id]['count'] * res_all[res_id]['price']
            res_all[res_id]['count'] = 0

# functions
def draw_header():
    os.system('clear')
    print('Секунды   :', pointed_number(res_time['seconds']), gap(res_time['seconds']) + '| Профиль :', name)
    print('Минуты    :', pointed_number(res_time['minutes']), gap(res_time['minutes']) + '| Уровень :', pointed_number(level))
    print('Часы      :', pointed_number(res_time['hours']), gap(res_time['hours']) + '| $       :', pointed_number(money))

def draw_buy():
    if buy[0] <= 3 + 1:
        print('\n' + buy[buy[0]])
        buy[1] = 0
        if buy[0] == 2:
            if res_time['seconds'] >= 10 and res_time['minutes'] >= 1:
                buy[1] = 1
        if buy[0] == 3:
            if res_time['minutes'] >= 10 and res_all[0]['count'] >= 50:
                buy[1] = 1
        if buy[0] == 4:
            if res_time['hours'] >= 1 and res_all[1]['count'] >= 100:
                buy[1] = 1

def draw_res():
    if res_all:
        print('')
        for i in res_all:
            print(draw_name(i['name']), pointed_number(i['count']), gap(i['count']) + '|', draw_storage(i['count'], i['storage']), upgradable(i['up_cost']), pointed_number(i['price'] * i['count']) + '$')

# game loops
def progress():
    global res_time
    while 1:
        time.sleep(1)
        res_time['wait_minutes'] += 1     
        res_time['wait_hours'] += 1    
        res_time['seconds'] += 1

        if res_time['wait_minutes'] == 60:
            res_time['wait_minutes'] = 0
            res_time['minutes'] += 1  

        if res_time['wait_hours'] == 3600:
            res_time['wait_hours'] = 0  
            res_time['hours'] += 1  

        if res_all:
            for i in res_all:
                i['count'] += i['per_s']
                if i['count'] > i['storage']:
                    i['count'] = i['storage']
                i['count'] = round(i['count'], 1)

        if game_exit == 1:
            os._exit(1)

def game_render():
    while 1:
        global money, move

        draw_header()
        draw_res()
        draw_buy()

        if move == ['']:
            move = input('\nДействие  : ').split(' ')
        else:
            print('\nДействие  :', move[0])

        if move[0] == 'quit' or move[0] == 'exit' or move[0] == 'e':
            game_exit = 1
            os.system('clear')
            os._exit(1)
            move = ['']
        elif move[0] == 'help':
            os.system('clear')
            print(help_text)
            move = input('\nДействие  : ').split(' ')
        elif move[0] == 'open' and buy[1] == 1:
            if buy[0] == 2:
                res_time['seconds'] -= 10
                res_time['minutes'] -= 1
                res_all.append(res_stone)

            if buy[0] == 3:
                res_time['minutes'] -= 10
                res_all[0]['count'] -= 50
                res_all.append(res_wood)

            if buy[0] == 4:
                res_time['hours'] -= 1
                res_all[1]['count'] -= 100
                res_all.append(res_coal)

            buy[1] == 0
            buy[0] += 1
            move = ['']
        elif move[0] == 'sell' and move[-1] != 'sell':
            sell(move[1])
            move = ['']
        elif move != ['']: # res stats
            i = 0
            try: 
                res_id = index[move[0]]
                i = res_all[res_id]
                os.system('clear')
                print(str(res_id+1)+'.', move[0] + '\n')
            except Exception:
                try:
                    i = res_all[int(move[0]) - 1]
                    os.system('clear')
                    print(move[0]+'.', i['name'] + '\n')
                except Exception: pass
            try:
                print('Колличество :', pointed_number(i['count']), '\nХранилище   :', i['storage'],'\nСтоимость 1 :', pointed_number(i['price']) + '$', '\nВ секунду   :', i['per_s'], '\nУровень     :', pointed_number(i['level']), '\n\nУлучшение', upgradable(i['up_cost']),'\nВ секунду   :', '???')
            except Exception: pass
            
            if i != 0:
                move = input('\nДействие  : ').split(' ')
            
            else: move = ['']

time_l = Thread(target=progress)
render_l = Thread(target=game_render)

time_l.start()
render_l.start()

time_l.join()
render_l.join()
