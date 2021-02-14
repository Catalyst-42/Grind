import time, os

move = ['']
name = 'Catalyst'
page = 'start'
timestamp = time.time()
game_exit = 0
money = 0
level = 0
i = 0
dev_mode = 0
colors_open = 0

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

\033[36mmain\033[0m
\033[36mm\033[0m
венуться на главную станицу

\033[36mexit\033[0m
\033[36me\033[0m
выйти из игры, сохранив ее

\033[36msave\033[0m
сохранить игру

\033[36m[name]\033[0m
\033[36m[id]\033[0m
показать данные ресурса, его id,
число ресурсов, цену одного ресурса,
цену улучшения и его бонусы, для 
выхода используйте команду main

\033[36msell [name]\033[0m
\033[36msell [id]\033[0m
\033[36msa\033[0m
продать весь указанный ресурс, 
допустим ключь all или просто 
сокращение sa в поле id для 
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

\033[36mstats\033[0m
Показывает статистику игрока, для 
выхода используйте команду main

\033[36mname [name]\033[0m
изменить имя профиля, допустим ввод
любых символов кроме пробела, рекомендуется 
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
Версия: release 3.0 Stats Update'''

res_time = {'seconds': 0,
            'minutes': 0,
            'hours': 0,
            'wait_seconds': 0,
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

res_klit = {'name': 'Кремнелит',
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

colors = [
    {'name': 'Белый',
    'up_cost': 10000,
    'per_s': 100000,
    'level': 0},

    {'name': 'Серый',
    'up_cost': 10000,
    'per_s': 200000,
    'level': 0},

    {'name': 'Красный',
    'up_cost': 10000,
    'per_s': 300000,
    'level': 0},

    {'name': 'Желтый',
    'up_cost': 10000,
    'per_s': 400000,
    'level': 0},

    {'name': 'Зеленый',
    'up_cost': 10000,
    'per_s': 500000,
    'level': 0},

    {'name': 'Бирюзовый',
    'up_cost': 10000,
    'per_s': 600000,
    'level': 0},
    
    {'name': 'Синий',
    'up_cost': 10000,
    'per_s': 700000,
    'level': 0},
    
    {'name': 'Фиолетовый',
    'up_cost': 10000,
    'per_s': 800000,
    'level': 0}
]

index = {'Камень': 0,
         'Дерево': 1,
         'Уголь': 2,
         'Ткань': 3,
         'Медь': 4,
         'Железо': 5,
         'Золото': 6,
         'Уран': 7,
         'Кремнелит': 8,
         'Хром': 9,
         'Белый': 10,
         'Серый': 11,
         'Красный': 12,
         'Желтый': 13,
         'Зеленый': 14,
         'Бирюзовый': 15,
         'Синий': 16,
         'Фиолетовый': 17}

buy = [2, 0, 'Камень    : 1 минута;\n            10 секунд', 
             'Дерево    : 10 минут;\n            50 камней', 
             'Уголь     : 5 часов;\n            30,000 дерева', 
             'Ткань     : 100,000,000$;\n            10,000 угля;\n            600 минут', 
             'Медь      : 10,000,000,000$;\n            15 часов;\n            50,000 ткани', 
             'Железо    : 24 часа;\n            100,000,000,000$', 
             'Золото    : 300,000 секунд;\n            500,000,000,000$', 
             'Уран      : 1 секунда;\n            1,000,000,000,000$',
             'Кремнелит : 200 часов;\n            10,000,000,000,000$',
             'Хром      : 1,000,000 секунд;\n            150,000 Золота;\n            150,000 Урана;\n            150,000 Кремнелита',
             'Красители : 150,000 Хрома']

res_all = []
stats = [time.time(), time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()), '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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

def gap(name, length=17, pointed=1):
    if pointed: return (' ' * (length - len(pn(name))))
    else: return name + (' ' * (length - len(name)))

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

    return out + '] ' + str(percents) + '%' + ' ' * (3 - len(str(percents)))

def upgradable(up_cost, level, color='none'):
    level = str(level)
    if color == 'none':
        if money >= up_cost: return '\033[32ml: ' + str(level) + '\033[0m' + ' '*(5-len(level)) + '|'
        else: return '\033[31ml: ' + str(level) + '\033[0m' + ' '*(5-len(level)) + '|'
    else:
        if res_all[color]['count'] >= up_cost: return '\033[32ml: ' + str(level) + '\033[0m' + ' '*(5-len(level)) + '|'
        else: return '\033[31ml: ' + str(level) + '\033[0m' + ' '*(5-len(level)) + '|'

def sell(move):
    global money
    res_id = -1
    if move == 'all':
        for i in res_all:
            money += i['count'] * i['price']
            stats[6] += i['count'] * i['price']
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
            stats[6] += res_all[res_id]['count'] * res_all[res_id]['price']
            res_all[res_id]['count'] = 0

def res_stat():
    draw_header()
    global move, page, previous
    i = 0
    if move[0].isalpha(): move[0] = move[0].capitalize()
    
    # извините, я не знаю, как это оптимизировать...
    try: 
        res_id = index[move[0]]
        i = res_all[res_id]
        print('\n' + str(res_id+1) + '.', move[0] + ' \n')
    except Exception:
        try:
            i = res_all[int(move[0]) - 1]
            print('\n' + move[0] + '.', i['name'] + ' \n')
        except Exception: 
            try:
                i = colors[int(move[0]) - 11]
                print('\n' + move[0] + '.', i['name'] + ' краситель\n')
            except Exception: 
                try:
                    i = colors[index[move[0]] - 10]
                    print('\n' + str(index[move[0]] + 1) + '.', i['name'] + ' краситель\n')
                except Exception: 
                    move[0] = page
                    try: 
                        res_id = index[move[0]]
                        i = res_all[res_id]
                        print('\n' + str(res_id+1) + '.', move[0] + ' \n')
                    except Exception:
                        try:
                            i = colors[index[move[0]] - 10]
                            print('\n' + str(index[move[0]] + 1) + '.', i['name'] + ' краситель\n')
                        except Exception: pass

    if i:
        if index[i['name']] < 10:
            print('Колличество :', pn(i['count']),\
                '\nХранилище   :', pn(round(i['storage'])),\
                '\nСтоимость 1 :', pn(i['price']) + '$',\
                '\nВ секунду   :', round(i['per_s'], 2),\
                '\nУровень     :', pn(i['level']),\
                '\n\nУлучшение\n')

            if money >= i['up_cost']: print('\033[32m', end='')
            else: print('\033[31m', end='')
            
            if (i['level'] + 1) % 50 == 0: print('Хранилище   :', '+' + pn(i['storage']))
            else: print('Хранилище   :', '+' + pn(i['level'] * 1.5))
            
            if (i['level'] + 1) % 100 == 0: print('Стоимость 1 :', '+' + pn(i['price'] + i['price_start']*2) + '$')
            else: print('Стоимость 1 :', '+' + pn(i['price_start']) + '$' )
            
            print('В секунду   :', '+0.1',\
                '\n\nЦена улучшения :', pn(i['up_cost']) + '$',\
                '\nДеньги         :', pn(money) + '$',\
                '\033[0m')
            
            page = i['name']

        elif colors_open: 
            print('$ В секунду :', pn(i['per_s'] * i['level']) + '$', '\nУровень     :', pn(i['level']))

            if res_all[index[i['name']] - 10]['count'] >= i['up_cost']: print('\033[32m', end='')
            else: print('\033[31m', end='')
            text = ['Камня', 'Дерева', 'Угля', 'Ткани', 'Меди', 'Железа', 'Золота', 'Урана']
            print('\nУлучшение\n', '\n$ В секунду : +' + pn(i['per_s']) + '$' )
            print('\nЦена улучшения :', pn(i['up_cost']) + ' ' + text[index[i['name']] - 10])
            print(gap(res_all[index[i['name']] - 10]['name'], 15, 0) + ':', pn(res_all[index[i['name']] - 10]['count']), '\033[0m')

            page = i['name']

    else: 
        move = ['']
        if page != 'stats': page = 'main'

# save and load stats
if os.path.exists('./stats.dat'):
    with open('stats.dat', 'r') as f:
        save = f.read().splitlines()
        stats = [float(save[0]), save[1], save[2], float(save[3]), float(save[4]), float(save[5]), float(save[6]),
        float(save[7]), float(save[8]), float(save[9]), float(save[10]), float(save[11]), int(save[12]), int(save[13])]

def save_stats():
    timestamp = time.time() - stats[0]
    out = [0, 0, 0, 0]
    stats[2] = ''

    stats[3] = timestamp // 1
    stats[4] = timestamp // 60
    stats[5] = timestamp // 3600
    stats[10] = stats[6] / timestamp

    while timestamp - 24*60*60 >= 0:
        out[0] += 1
        timestamp -= 24*60*60

    while timestamp - 60*60 >= 0:
        out[1] += 1
        timestamp -= 60*60
    
    while timestamp - 60 >= 0:
        out[2] += 1
        timestamp -= 60

    while timestamp - 1 >= 0:
        out[3] += 1
        timestamp -= 1
    
    if out[0] > 0: stats[2] += str(out[0]) + ' д '
    if out[1] > 0: stats[2] += str(out[1]) + ' ч '
    if out[2] > 0: stats[2] += str(out[2]) + ' м '
    if out[3] > 0: stats[2] += str(out[3]) + ' с '

    stats[12] = 0 
    if res_all:
        stats[8] = res_all[0]['storage'] / res_all[0]['per_s']
        for i in res_all:
            if i['storage'] / i['per_s'] <= stats[8]: stats[8] = i['storage'] / i['per_s']
            if i['level'] >= stats[13]: stats[13] = i['level']
            stats[12] += i['level']

    stats[11] = 0
    if colors_open:
        for i in colors:
            stats[11] += i['per_s'] * i['level']
            stats[12] += i['level']

    if money >= stats[9]: stats[9] = money
    
    with open('stats.dat', 'w') as f:
        for i in range(len(stats)):
            f.write(str(stats[i]) + '\n')

    timestamp = time.time()

def draw_stats():
    os.system('clear')
    timestamp = stats[7]
    out = [0, 0, 0, 0]
    while timestamp - 24*60*60 >= 0:
        out[0] += 1
        timestamp -= 24*60*60

    while timestamp - 60*60 >= 0:
        out[1] += 1
        timestamp -= 60*60
    
    while timestamp - 60 >= 0:
        out[2] += 1
        timestamp -= 60

    while timestamp - 1 >= 0:
        out[3] += 1
        timestamp -= 1
    
    max_offline = ''

    if out[0] > 0: max_offline += str(out[0]) + ' д '
    if out[1] > 0: max_offline += str(out[1]) + ' ч '
    if out[2] > 0: max_offline += str(out[2]) + ' м '
    if out[3] > 0: max_offline += str(out[3]) + ' с '

    timestamp = stats[8]
    out = [0, 0, 0, 0]
    best_offline = ''
    while timestamp - 24*60*60 >= 0:
        out[0] += 1
        timestamp -= 24*60*6

    while timestamp - 60*60 >= 0:
        out[1] += 1
        timestamp -= 60*60
    
    while timestamp - 60 >= 0:
        out[2] += 1
        timestamp -= 60

    while timestamp - 1 >= 0:
        out[3] += 1
        timestamp -= 1
    
    if out[0] > 0: best_offline += str(out[0]) + ' д '
    if out[1] > 0: best_offline += str(out[1]) + ' ч '
    if out[2] > 0: best_offline += str(out[2]) + ' м '
    if out[3] > 0: best_offline += str(out[3]) + ' с '

    print('Статистика игрока', name,
        '\n\nНачало игры :', stats[1],
        '\nВремя игры  :', stats[2],
        '\n\nСекунд получено :', pn(stats[3]), 
        '\nМинут получено  :', pn(stats[4]),
        '\nЧасов получено  :', pn(stats[5]),
        '\nДенег получено  :', pn(stats[6]) + '$',
        '\n\nМаксимальное время в афк :', max_offline,
        '\nПрибыльное время в афк   :', best_offline,
        '\n\nДеньги                       :', pn(money) + '$',
        '\nМаксимум денег в кошельке    :', pn(stats[9]) + '$',
        '\nДенег в секунду за все время :', pn(stats[10]) + '$ / c',
        '\nДенег в секунду за красители :', pn(stats[11]) + '$ / c',
        '\n\nУровней куплено      :', pn(stats[12]),
        '\nМаксимальный уровень :', stats[13])

# save and load
def save_res_update(res, offset):
    offset = offset * 7
    res['count'] = float(save[11 + offset])
    res['price'] = int(save[12 + offset])
    res['price_start'] = int(save[13 + offset])
    res['up_cost'] = float(save[14 + offset])
    res['storage'] = float(save[15 + offset])
    res['per_s'] = float(save[16 + offset])
    res['level'] = int(save[17 + offset])

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

        res_time['wait_minutes'] = float(save[7])
        res_time['wait_hours'] = float(save[8])
        save[8] = int(save[9])
        colors_open = int(save[10])

        # res loop
        buy[0] = save[8]

        if buy[0] - 2 > 10: b = range(10)
        else: b = range(buy[0] - 2)

        for i in b:
            j = [res_stone, res_wood, res_coal, res_fabric, res_copper, res_steel, res_gold, res_uranium, res_klit, res_chromium]
            save_res_update(j[i], i)
            res_all.append(j[i])

        if colors_open:
            for i in range(len(colors)):
                colors[i]['up_cost'] = int(save[81 + i*2])
                colors[i]['level'] = int(save[82 + i*2])

        # offline encounter
        os.system('clear')
        timestamp = time.time() - timestamp
        if stats[7] <= timestamp: stats[7] = timestamp
        timestamp = round(timestamp)
        print('С возвращением, ' + name + '\nВас не было в игре:\n')
        offline_sec = timestamp
        offline_min = 0
        offline_hrs = 0
        offline_days = 0

        while offline_days - 3600*24 >= 1:
            offline_days += 1
            offline_sec -= 3600*24

        while offline_sec - 3600 >= 1:
            offline_hrs += 1
            offline_sec -= 3600

        while offline_sec - 60 >= 1:
            offline_min += 1
            offline_sec -= 60

        if offline_days > 0: print(offline_days, 'д ', end='')
        if offline_hrs > 0: print(offline_hrs, 'ч ', end='')
        if offline_min > 0: print(offline_min, 'м ', end='')
        if offline_sec > 0: print(offline_sec, 'с ', end='')

        print('\n\nВы получили:\n')
        
        median = money
        if colors_open:
            for i in colors:
                money += i['per_s'] * i['level'] * timestamp
        
            print(draw_name('Деньги'), pn(money - median) + '$\n')
        
        print(draw_name('Секунды'), pn(timestamp))

        if timestamp//60>=1000: print(draw_name('Минуты'), pn(timestamp//60)) 
        else: print(draw_name('Минуты'), timestamp//60)

        if timestamp//3600>=1000: print(draw_name('Часы'), pn(timestamp//3600))
        else: print(draw_name('Часы'), timestamp//3600)

        print(draw_name('Уровни'), pn(timestamp//3600), end='\n\n')
        

        for i in res_all:
            if i['per_s'] * timestamp + i['count'] < i['storage']: print(draw_name(i['name']), pn(i['per_s'] * timestamp))
            else: print('\033[31m'+draw_name(i['name']), pn(i['storage'] - i['count']) + '\033[0m')
            res_all[index[i['name']]]['count'] += i['per_s'] * timestamp 
            if i['count'] > i['storage']: i['count'] = i['storage']

        res_time['seconds'] += timestamp
        res_time['minutes'] += timestamp//60
        res_time['hours'] += timestamp//3600
        level += timestamp//3600

        res_time['wait_minutes'] += offline_sec
        res_time['wait_hours'] += offline_sec

        move = input('\nДействие  : ').split(' ')
        timestamp = time.time()

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
        f.write(str(colors_open) + '\n')

        for i in res_all:
            f.write(str(i['count'])  + '\n')
            f.write(str(i['price'])  + '\n')
            f.write(str(i['price_start'])  + '\n')
            f.write(str(i['up_cost'])  + '\n')
            f.write(str(i['storage'])  + '\n')
            f.write(str(i['per_s'])  + '\n')
            f.write(str(i['level'])  + '\n')

        for i in colors:
            f.write(str(i['up_cost']) + '\n')
            f.write(str(i['level']) + '\n')

# functions
def draw_header():
    os.system('clear')
    print('Секунды   :', pn(res_time['seconds']), gap(res_time['seconds']) + '| Профиль :', name)
    print('Минуты    :', pn(res_time['minutes']), gap(res_time['minutes']) + '| Уровень :', pn(level))
    print('Часы      :', pn(res_time['hours']), gap(res_time['hours']) + '| Деньги  :', pn(money) + '$')

def draw_buy():
    if buy[0] <= 12:
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
            if res_time['hours'] >= 24 and money >= 100000000000:
                buy[1] = 1
        if buy[0] == 8:
            if res_time['seconds'] >= 300000 and money >= 500000000000:
                buy[1] = 1
        if buy[0] == 9:
            if res_time['seconds'] >= 1 and money >= 1000000000000:
                buy[1] = 1
        if buy[0] == 10:
            if res_time['hours'] >= 200 and money >= 10000000000000:
                buy[1] = 1
        if buy[0] == 11:
            if res_time['seconds'] >= 1000000 and \
            res_all[6]['count'] >= 150000 and \
            res_all[7]['count'] >= 150000 and \
            res_all[8]['count'] >= 150000:
                buy[1] = 1

        if buy[0] == 12:
            if res_all[9]['count'] >= 150000:
                buy[1] = 1

        if buy[1] == 1: print('\n' + buy[buy[0]])

def draw_res():
    if res_all:
        print('\nРесурсы\n')
        for i in res_all:
            print(draw_name(i['name']), draw_storage(i['count'], i['storage']), '|',\
            upgradable(i['up_cost'], i['level']), pn(i['price'] * i['count']) + '$')

    if colors_open:
        print('\nКрасители\n')

        text = ['█ Белый краситель             \033[0m|',
        '\033[2m█ Серый краситель             \033[0m|',
        '\033[31m█ Красный краситель           \033[0m|',
        '\033[33m█ Желтый краситель            \033[0m|',
        '\033[32m█ Зеленый краситель           \033[0m|',
        '\033[36m█ Бирюзовый краситель         \033[0m|',
        '\033[34m█ Синий краситель             \033[0m|',
        '\033[35m█ Фиолетовый краситель        \033[0m|']
        for i in range(len(colors)):
            print(text[i], upgradable(colors[i]['up_cost'], colors[i]['level'], i), pn(colors[i]['per_s'] * colors[i]['level']) + '$ / с')

# game loops
def progress():
    global res_time, level, timestamp, colors, colors_open, money
    timestamp = time.time() - timestamp

    res_time['wait_seconds'] += timestamp
    res_time['wait_minutes'] += timestamp
    res_time['wait_hours'] += timestamp 

    if res_time['wait_seconds'] >= 1:
        res_time['seconds'] += int(res_time['wait_seconds'])
        res_time['wait_seconds'] -= int(res_time['wait_seconds'])

    while res_time['wait_minutes'] >= 60:
        res_time['minutes'] += int(res_time['wait_minutes'] / 60)
        res_time['wait_minutes'] -= int(res_time['wait_minutes'])

    while res_time['wait_hours'] >= 3600:
        level += int(res_time['wait_hours'] / 3600)
        res_time['hours'] += int(res_time['wait_hours'] / 3600)
        res_time['wait_hours'] -= int(res_time['wait_hours'])

    if res_all:
        for i in res_all:
            i['count'] += i['per_s'] * timestamp
            if i['count'] > i['storage']:
                i['count'] = i['storage']

            i['count'] = round(i['count'], 1)

    if colors_open:
        for i in colors:
            money += i['per_s'] * i['level'] * timestamp
            stats[6] += i['per_s'] * i['level'] * timestamp

    if money >= stats[9]: stats[9] = money
    timestamp = time.time()

def game_render():
    while 1:
        global money, move, name, page, dev_mode, colors_open, colors

        if page == 'main':
            draw_header()
            draw_res()
            draw_buy()
        
        elif page == 'stats':
            save_stats()
            draw_stats()
        
        elif page != 'start':
            res_stat()

        if dev_mode: print('\nws:', res_time['wait_seconds'],
            '\nwm:', res_time['wait_minutes'],
            '\nwh:', res_time['wait_hours'],
            '\nut:', time.time(),
            '\npg:', page,
            '\nco:', colors_open,
            '\nb0:', buy[0])

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
            if page != i['name'] and page != 'stats':
                page = 'main'

        progress()
        
        if move[0] == 'help':
            os.system('clear')
            print(help_text)
            move = input('\nДействие : ').split(' ')

        if move[0] == 'stats':
            save_stats()
            draw_stats()
            page = 'stats'
            # move = input('\nДействие : ').split(' ')
        
        if move[0] == 'quit' or move[0] == 'exit' or move[0] == 'e':
            save_game()
            game_exit = 1
            os.system('clear')
            os._exit(1)
        
        if move[0] == 'open' and buy[0] <= 12:
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
                    money -= 100000000000
                    res_all.append(res_steel)

                if buy[0] == 8:
                    res_time['seconds'] -= 300000
                    money -= 500000000000
                    res_all.append(res_gold)

                if buy[0] == 9:
                    res_time['seconds'] -= 1
                    money -= 1000000000000
                    res_all.append(res_uranium)

                if buy[0] == 10:
                    res_time['hours'] -= 200
                    money -= 10000000000000
                    res_all.append(res_klit)

                if buy[0] == 11:
                    res_time['seconds'] -= 1000000
                    res_all[6]['count'] -= 150000
                    res_all[7]['count'] -= 150000
                    res_all[8]['count'] -= 150000
                    res_all.append(res_chromium)

                if buy[0] == 12:
                    res_all[9]['count'] -= 150000
                    colors_open = 1

                buy[1] = 0
                buy[0] += 1

            else: print('\033[31m' + buy[buy[0]] + '\033[0m'); move = input().split(' ')

        if (move[0] == 'sell' and len(move) > 1) or move[0] == 'sa':
            if move[0] == 'sa': move = ['sell', 'all']
            elif move[1] != 'all' and move[1].isalpha(): move[1] = move[1].capitalize()
            sell(move[1])

        if move[0] == 'up' and len(move) > 1:
            if move[1].isalpha(): move[1] =  move[1].capitalize()
            i = 0
            loop = 1
            colored = 0 
            
            try: 
                res_id = index[move[1]]
                i = res_all[res_id]
            except Exception:
                try:
                    i = res_all[int(move[1]) - 1]
                except Exception:
                    try:
                        i = colors[int(move[1]) - 11]
                        colored = 1
                    except Exception: 
                        try:
                            i = colors[index[move[1]] - 10]
                            colored = 1
                        except Exception: pass

            try:
                if move[2] == 'max': loop = 'max'
                else: loop = int(move[2])
            except Exception: pass
            
            if i:
                while 1:
                    if not colored and money >= i['up_cost']:
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
                        # увеличение стоимости улучшения
                        i['up_cost'] *= 1.07
                        # увеличение хранилища
                        i['storage'] += i['level'] * 1.5
                        # увеличение ресурсов в секунду
                        i['per_s'] += 0.1

                        if loop != 'max': 
                            loop -=1
                            if loop <= 0: break

                    elif colored and colors_open and res_all[index[i['name']] - 10]['count'] >= i['up_cost']:
                        res_all[index[i['name']] - 10]['count'] -= i['up_cost']
                        colors[index[i['name']] - 10]['up_cost'] += 10000
                        colors[index[i['name']] - 10]['level'] += 1

                        if loop != 'max': 
                            loop -=1
                            if loop <= 0: break

                    else: break
        
        if move[0] == 'name':
            name = move[1]
        
        if move[0] == 'save' or move[0] == 's':
            save_game()
    
        if len(move) >= 3:
            if move[0] == 'delete' and move[1] == 'save' and move[2] == name:
                os.system('rm ./save.dat')
        
        if len(move) >= 2:
            if move[0] == 'developer' and move[1] == 'mode':
                if dev_mode == 0: dev_mode = 1
                else: dev_mode = 0

        if move[0] == 'main' or move[0] == 'm':
            page = 'main'

        else: res_stat()

game_render()
