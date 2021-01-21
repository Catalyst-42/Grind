import time
import os
from threading import Thread

seconds = 0
minutes = 0
hours = 0

sleep_time = 1
game_exit = 0

def get_time():
    global seconds, minutes, hours
    wait_minutes = 0
    wait_hours = 0

    while 1:
        time.sleep(sleep_time)
        wait_minutes += 1
        wait_hours += 1

        seconds += 1
        if wait_minutes == 60:
            minutes += 1
            wait_minutes = 0

        if wait_hours == 3600:
            hours += 1
            wait_hours = 0

        if game_exit == 1:
            os._exit(1)

def game_render():
    while 1:
        os.system('clear')
        print('Секунды:', seconds)
        print('Минуты:', minutes)
        print('Часы:', hours)

        move = input('Действие: ')

        if move == 'quit' or move == 'exit':
            game_exit = 1
            os._exit(1)

time_l = Thread(target=get_time)
render_l = Thread(target=game_render)

time_l.start()
render_l.start()

time_l.join()
render_l.join()
