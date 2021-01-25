level = 1
nps = 1
up_price = 10
storage = 100

nps_start = nps

all_price = 0

# nps scaling
# 1 > 5 > 100
# up_price scaling
# 10 > 50 > 1000
# time scaling
# 0.5 > 0.6 > 0.7
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

print('level:', level, "\nup_price:", pn(up_price), 'nps:', pn(nps),'Storage:', storage, 'Scale', pn(up_price / nps), '\nSumm:', pn(all_price), '\n')

for i in range(171):
    # увеличение цены
    level += 1
    nps = nps + nps_start
    if level % 100 == 0:
        nps_start *= 2
        nps *= 2
        up_price *= 1.4
    if level % 50 == 0: storage *=2
    # увеличение прибыли
    up_price *= 1.07
    #увеличение хранилища
    storage += level * 1.5
    # счет суммы
    all_price += up_price

    print('level:', level, "\nup_price:", pn(up_price), 'nps:', pn(nps),'Storage:', pn(storage), 'Scale', pn(up_price / nps), '\nSumm:', pn(all_price), '\n')
