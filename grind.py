import time
import os
from threading import Thread
import os.path

name = 'Catalyst'
game_exit = 0
money = 0
level = 0
move = ['']
i = 0
page = 'start'

help_text = '''\033[35mКоманды\033[0m

\033[36mhelp\033[0m
выводит список доступных команд, где 
наименования в скобках - число или имя
прдмета, сами скобки указывать не надо.
        
пример вида команды и его исполнение
\033[36mup [id] [level]\033[0m
\033[36mup 1 10\033[0m
улучшить первый предмет на 10 уровней

пример сокращенного имени
\033[36mexit\033[0m
\033[36me\033[0m
кажда из команд будет выполнять одну,
указанную в описании функцию

\033[36menter\033[0m
обновление текущего экрана, допустимо 
нажатие клавиши enter

\033[36mexit\033[0m
\033[36me\033[0m
выйти из игры, сохранив ее

\033[36msave\033[0m
сохранить игру

\033[36m[name]\033[0m
\033[36m[id]\033[0m
показать данные ресурса, его id,
число ресурсов, цену одного ресурса,
цену улучшения и его бонусы

\033[36msell [name]\033[0m
\033[36msell [id]\033[0m
продать весь указанный ресурс, 
допустим ключь all в поле id для 
продажи всех ресурсов

\033[36mopen\033[0m
открыть ресурс, если у вас хватает 
ресурсов для открытия, после колонки 
откртых ресурсов появиться стоимость покупки

\033[36mup [name] [level]\033[0m
\033[36mup [id] [level]\033[0m
улучшение уровня ресурса,
допустим ключ max для улучшения 
на максимальный возможный уровень 
ресурса или пустой ключ в значение 
level для улучшения на 1 уровень

\033[36mmain\033[0m
\033[36mm\033[0m
венуться на главную станицу

\033[36mname [name]\033[0m
изменить имя профиля, допустим ввод
любых символов кроме пробела, рекомендуемо 
использовать имя профиля меньше 24 символов

\033[36mdelete save [name]\033[0m
Удалить сохранение, в качестве подтверждения 
укажите актуальное имя игрока, восстановить 
данные невозможно

\033[35mСправка\033[0m

Игра не обновляется динамически, управляется 
командами, значения которых разделяются пробелами,
enter для подтверждения ввода

Создал: Catalyst
Версия: release 1.1 fabric copper'''

res_time = {'seconds': 0,
            'minutes': 0,
            'hours': 0,
            'wait_minutes': 0,
            'wait_hours': 0}

res_stone = {'name': 'Камень',
             'count': 0,
             'price': 1,
             'price_start': 1,
             'up_cost': 10,
             'storage': 100,
             'per_s': 0.5,
             'level': 1}

res_wood = {'name': 'Дерево',
             'count': 0,
             'price': 5,
             'price_start': 5,
             'up_cost': 100,
             'storage': 100,
             'per_s': 0.5,
             'level': 1}

res_coal = {'name': 'Уголь',
             'count': 0,
             'price': 50,
             'price_start': 50,
             'up_cost': 500,
             'storage': 100,
             'per_s': 0.5,
             'level': 1}

res_fabric = {'name': 'Ткань',
              'count': 0,
              'price': 100,
              'price_start': 100,
              'up_cost': 1000,
              'storage': 100,
              'per_s': 0.5,
              'level': 1}

res_copper = {'name': 'Медь',
              'count': 0,
              'price': 200,
              'price_start': 200,
              'up_cost': 2000,
              'storage': 100,
              'per_s': 0.5,
              'level': 1}

res_steel = {'name': 'Железо',
             'count': 0,
             'price': 500,
             'price_start': 500,
             'up_cost': 4000,
             'storage': 100,
             'per_s': 0.5,
             'level': 1}

res_gold = {'name': 'Золото',
            'count': 0,
            'price': 1000,
            'price_start': 1000,
            'up_cost': 10000,
            'storage': 100,
            'per_s': 0.5,
            'level': 1}

res_uranium = {'name': 'Уран',
               'count': 0,
               'price': 2000,
               'price_start': 2000,
               'up_cost': 50000,
               'storage': 100,
               'per_s': 0.5,
               'level': 1}

res_klit = {'name': 'Крмнелит',
            'count': 0,
            'price': 5000,
            'price_start': 5000,
            'up_cost': 100000,
            'storage': 100,
            'per_s': 0.5,
            'level': 1}

res_chromium = {'name': 'Хром',
               'count': 0,
               'price': 10000,
               'price_start': 10000,
               'up_cost': 500000,
               'storage': 100,
               'per_s': 0.5,
               'level': 1}

index = {'Камень': 0,
         'Дерево': 1,
         'Уголь': 2,
         'Ткань': 3,
         'Медь': 4,
         'Железо': 5,
         'Золото': 6,
         'Уран': 7,
         'Кремнелит': 8,
         'Хром': 9}

buy = [2, 0, 'Камень    : 1 минута; 10 секунд', 
             'Дерево    : 10 минут; 50 камней', 
             'Уголь     : 5 часов; 30,000 дерева', 
             'Ткань     : 100,000,000$; 10,000 угля; 600 минут', 
             'Медь      : 10,000,000,000$; 15 часов; 50,000 ткани', 
             'Железо    : 24 часа', 
             'Золото    : unset', 
             'Уран      : unset',
             'Кремнелит : unset',
             'Хром      : unset']

res_all = []

# extension
def draw_name(name):
    return name + ' ' * (10 - len(name)) + ':'

def pn(number):
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
    return (' ' * (17 - len(pn(name))))

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

def upgradable(up_cost, level):
    level = str(level)
    if money >= up_cost: return '\033[32ml: ' + str(level) + '\033[0m' + ' '*(5-len(level)) + '|'
    else: return '\033[31ml: ' + str(level) + '\033[0m' + ' '*(5-len(level)) + '|'

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

def res_stat():
    global move, page, previous
    i = 0
    if page != 'main': move[0] = page
    try: 
        os.system('clear')
        res_id = index[move[0]]
        i = res_all[res_id]
        print(str(res_id+1)+'.', move[0] + '\n')
    except Exception:
        try:
            os.system('clear')
            i = res_all[int(move[0]) - 1]
            print(move[0]+'.', i['name'] + '\n')
        except Exception: pass
    if i:
        print('Колличество :', pn(i['count']), '\nХранилище   :', pn(round(i['storage'])),'\nСтоимость 1 :', pn(i['price']) + '$', '\nВ секунду   :', round(i['per_s'], 2), '\nУровень     :', pn(i['level']), '\n\nУлучшение\n')
        if money >= i['up_cost']: print('\033[32m', end='')
        else: print('\033[31m', end='')
        if (i['level'] + 1) % 50 == 0: print('Хранилище   :', '+' + pn(i['storage']))
        else: print('Хранилище   :', '+' + pn(i['level'] * 1.5))
        if (i['level'] + 1) % 100 == 0: print('Стоимость 1 :', '+' + str(i['price'] + i['price_start']*2))
        else: print('Стоимость 1 :', '+' + str(i['price_start']))
        print('В секунду   :', '+0.1')
        print('\nЦена улучшения :', pn(i['up_cost']) + '$')
        print('Деньги         :', pn(money) + '$')
        print('\033[0m', end='')

        page = i['name']

    else: move = ['']

# save and load
def save_res_update(res, offset):
    offset = offset * 7
    res['count'] = float(save[10 + offset])
    res['price'] = int(save[11 + offset])
    res['price_start'] = int(save[12 + offset])
    res['up_cost'] = float(save[13 + offset])
    res['storage'] = float(save[14 + offset])
    res['per_s'] = float(save[15 + offset])
    res['level'] = int(save[16 + offset])

if os.path.exists('./save.dat'):
    with open('save.dat', 'r') as f:
        save = f.read().splitlines()
        
        name = save[0]
        money = float(save[1])
        level = int(save[2])

        # offline encounter
        timestamp = float(save[3])

        res_time['seconds'] = int(save[4])
        res_time['minutes'] = float(save[5])
        res_time['hours'] = int(save[6])

        res_time['wait_minutes'] = int(save[7])
        res_time['wait_hours'] = int(save[8])
        save[8] = int(save[9])

        # res loop
        buy[0] = save[8]
        for i in range(buy[0] - 2):
            j = [res_stone, res_wood, res_coal, res_fabric, res_copper, res_steel, res_gold, res_uranium, res_klit, res_chromium]
            save_res_update(j[i], i)
            res_all.append(j[i])


        # offline encounter
        os.system('clear')
        timestamp = time.time() - timestamp
        timestamp = round(timestamp)
        print('С возвращением, ' + name + '\nВас не было в игре:\n')
        offline_sec = timestamp
        offline_min = 0
        offline_hrs = 0

        while offline_sec - 3600 >= 1:
            offline_hrs += 1
            offline_sec -= 3600

        while offline_sec - 60 >= 1:
            offline_min += 1
            offline_sec -= 60
        
        print('Секунд:', offline_sec)
        print('Минут :', offline_min)
        print('Часов :', offline_hrs)
        print('\nВы получили:\n')
        print(draw_name('Секунд'), pn(timestamp))
        if timestamp//60>=1000: print(draw_name('Минут'), pn(timestamp//60)) 
        else: print(draw_name('Минут'), timestamp//60)
        if timestamp//3600>=1000: print(draw_name('Часов'), pn(timestamp//3600))
        else: print(draw_name('Часов'), timestamp//3600)
        print(draw_name('Уровней'), timestamp//3600, end='\n\n')
        for i in res_all:
            if i['per_s'] * timestamp + i['count'] < i['storage']: print(draw_name(i['name']), pn(i['per_s'] * timestamp))
            else: print('\033[31m'+draw_name(i['name']), pn(i['storage'] - i['count']) + '\033[0m')
            res_all[index[i['name']]]['count'] += i['per_s'] * timestamp 
            if i['count'] > i['storage']:i['count'] = i['storage']

        level += timestamp//3600
        res_time['seconds'] += timestamp
        res_time['minutes'] += timestamp//60
        res_time['hours'] += timestamp//3600

        res_time['wait_minutes'] += offline_sec
        res_time['wait_hours'] += offline_sec


        move = input('\nДействие  : ').split(' ')

def save_game():
    with open('save.dat', 'w') as f:
        f.write(name + '\n')
        f.write(str(money) + '\n')
        f.write(str(level)  + '\n')
        f.write(str(time.time()) + '\n')
        f.write(str(res_time['seconds'])  + '\n')
        f.write(str(res_time['minutes'])  + '\n')
        f.write(str(res_time['hours'])  + '\n')
        f.write(str(res_time['wait_minutes'])  + '\n')
        f.write(str(res_time['wait_hours'])  + '\n')
        f.write(str(buy[0])  + '\n')

        for i in res_all:
            f.write(str(i['count'])  + '\n')
            f.write(str(i['price'])  + '\n')
            f.write(str(i['price_start'])  + '\n')
            f.write(str(i['up_cost'])  + '\n')
            f.write(str(i['storage'])  + '\n')
            f.write(str(i['per_s'])  + '\n')
            f.write(str(i['level'])  + '\n')

# functions
def draw_header():
    os.system('clear')
    print('Секунды   :', pn(res_time['seconds']), gap(res_time['seconds']) + '| Профиль :', name)
    print('Минуты    :', pn(res_time['minutes']), gap(res_time['minutes']) + '| Уровень :', pn(level))
    print('Часы      :', pn(res_time['hours']), gap(res_time['hours']) + '| Деньги  :', pn(money) + '$')

def draw_buy():
    if buy[0] <= 9:
        buy[1] = 0
        if buy[0] == 2:
            if res_time['seconds'] >= 10 and res_time['minutes'] >= 1:
                buy[1] = 1
        if buy[0] == 3:
            if res_time['minutes'] >= 10 and res_all[0]['count'] >= 50:
                buy[1] = 1
        if buy[0] == 4:
            if res_time['hours'] >= 5 and res_all[1]['count'] >= 30000:
                buy[1] = 1
        if buy[0] == 5:
            if res_time['minutes'] >= 600 and res_all[2]['count'] >= 10000 and money >= 100000000:
                buy[1] = 1
        if buy[0] == 6:
            if res_time['hours'] >= 15 and  res_all[3]['count'] >= 50000 and money >= 10000000000:
                buy[1] = 1
        if buy[0] == 7:
            if res_time['hours'] >= 24:
                buy[1] = 1
        if buy[0] == 8:
            if res_time['seconds'] >= 1:
                buy[1] = 1
        if buy[0] == 9:
            if res_time['seconds'] >= 1:
                buy[1] = 1
        if buy[0] == 10:
            if res_time['seconds'] >= 1:
                buy[1] = 1
        if buy[0] == 11:
            if res_time['seconds'] >= 1:
                buy[1] = 1
        if buy[1] == 1: print('\n' + buy[buy[0]])

def draw_res():
    if res_all:
        print('')
        for i in res_all:
            print(draw_name(i['name']), draw_storage(i['count'], i['storage']), '|',  upgradable(i['up_cost'], i['level']), pn(i['price'] * i['count']) + '$')

# game loops
def progress():
    global res_time, level
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
            level += 1

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
        global money, move, name, page

        if page == 'main':
            draw_header()
            draw_res()
            draw_buy()
        
        elif page != 'start':
            res_stat()
        
        if page != 'start': move = input('\nДействие  : ').split(' ')
        else: page = 'main'
        i = 0
        try: 
            res_id = index[move[0]]
            i = res_all[res_id]
        except Exception:
            try:
                i = res_all[int(move[0]) - 1]
            except Exception: pass
        if i != 0:
            if page != i['name']:
                page = 'main'
        
        if move[0] == 'quit' or move[0] == 'exit' or move[0] == 'e':
            save_game()
            game_exit = 1
            os.system('clear')
            os._exit(1)
        
        if move[0] == 'help':
            os.system('clear')
            print(help_text)
            move = input('\nДействие : ').split(' ')
        
        if move[0] == 'open':
            if buy[1] == 1:
                if buy[0] == 2:
                    res_time['seconds'] -= 10
                    res_time['minutes'] -= 1
                    res_all.append(res_stone)

                if buy[0] == 3:
                    res_time['minutes'] -= 10
                    res_all[0]['count'] -= 50
                    res_all.append(res_wood)

                if buy[0] == 4:
                    res_time['hours'] -= 5
                    res_all[1]['count'] -= 30000
                    res_all.append(res_coal)

                if buy[0] == 5:
                    res_time['minutes'] -= 600
                    money -= 100000000
                    res_all[2]['count'] -= 10000
                    res_all.append(res_fabric)

                if buy[0] == 6:
                    res_time['hours'] -= 15
                    res_all[3]['count'] -= 50000
                    money -= 10000000000
                    res_all.append(res_copper)

                if buy[0] == 7:
                    res_time['hours'] -= 24
                    res_all.append(res_steel)

                if buy[0] == 8:
                    res_time['seconds'] -= 1
                    res_all.append(res_gold)

                if buy[0] == 9:
                    res_time['seconds'] -= 1
                    res_all.append(res_uranium)

                if buy[0] == 10:
                    res_time['seconds'] -= 1
                    res_all.append(res_klit)

                if buy[0] == 11:
                    res_time['seconds'] -= 1
                    res_all.append(res_chromium)

                buy[1] = 0
                buy[0] += 1

            else: print('\033[31m' + buy[buy[0]] + '\033[0m'); move = input().split(' ')

        if move[0] == 'sell' and len(move) > 1:
            sell(move[1])

        if move[0] == 'up' and len(move) > 1:
            i = 0
            loop = 1
            try: 
                res_id = index[move[1]]
                i = res_all[res_id]
                
            except Exception:
                try:
                    i = res_all[int(move[1]) - 1]
                except Exception: pass
            try:
                if move[2] == 'max': loop = 'max'
                else: loop = int(move[2])
            except Exception: pass
            
            if i:
                while 1:
                    if money >= i['up_cost']:
                        money -= i['up_cost']
                        i['level'] += 1
                        # увеличение цены продажи
                        i['price'] +=  i['price_start']
                        # бонус в 100 уровней
                        if i['level'] % 100 == 0:
                            i['price'] +=  i['price_start']
                            i['price_start'] *= 2
                            i['price'] *= 2
                            i['up_cost'] *= 1.4
                        if i['level'] % 50 == 0: i['storage'] *= 2
                        # увеличение стоимости улучшени]
                        i['up_cost'] *= 1.07
                        # увеличение хранилища
                        i['storage'] += i['level'] * 1.5
                        # увеличение ресурсов в секунду
                        i['per_s'] += 0.1
                        if loop != 'max': 
                            loop -=1
                            if loop <= 0: break
                    else: break
        
        if move[0] == 'name':
            name = move[1]
        
        if move[0] == 'main' or move[0] == 'm':
            page = 'main'

        if move[0] == 'save' or move[0] == 's':
            save_game()
        
        if move[0] == 'delete' and move[1] == 'save' and move[2] == name:
            os.system('rm ./save.dat')

        res_stat()

time_l = Thread(target=progress)
render_l = Thread(target=game_render)

time_l.start(); render_l.start(); time_l.join(); render_l.join()
