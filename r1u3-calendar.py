#zadani https://fiks.fit.cvut.cz/files/tasks/season5/round1/calendar.pdf
debug = False
def p(msg):
    if debug:
        print(msg)

#vrati pocet dni v prestupnem mesici
def count_days_leap_month(year):
    if(year%LEAP_MONTH['year_divided_by']==0):
        if(year%LEAP_MONTH['year_not_divided_by']==0):
            return LEAP_MONTH['days_in_normal']
        else:
            return LEAP_MONTH['days_in_leap_month']
    return DAYS_IN_MONTHS[LEAP_MONTH['leap_month']-1]

#spocita datum tohoto vudcovskeho roku
def count_current_v_year_days(rest_days, year):
    days_leap_month = count_days_leap_month(year)
    month = 1
    for i in range(0, len(DAYS_IN_MONTHS)):

        p("zatim je rest days: " + str(rest_days))
        if(i!=LEAP_MONTH['leap_month'] - 1):
            if(rest_days>DAYS_IN_MONTHS[i]):
                rest_days -= DAYS_IN_MONTHS[i]
                month+=1
            else:
            #(rest_days <= DAYS_IN_MONTHS[i]):
                return rest_days, month
        else:

            if(rest_days>days_leap_month):
                rest_days-= days_leap_month
                month+=1
            else:
            #(rest_days <= days_leap_month):
                return rest_days, month
    return rest_days, month

#odecte od zbyvajicich dni prestupne roky, je-li prestupnych vic, snizi rok o jedna a zvysi pocet zbyvajicich o pocet dni v roce, pak odecte
def recount_v_year(sug_year, rest_days, leap_days):
    while(leap_days>rest_days):
        rest_days += YEAR_DAYS
        if (sug_year%LEAP_MONTH['year_divided_by'] == 0):
            if(sug_year%LEAP_MONTH['year_not_divided_by'] == 0):
                rest_days += LEAP_MONTH['days_in_normal']-DAYS_IN_MONTHS[LEAP_MONTH['leap_month']-1]
            else:
                rest_days += LEAP_MONTH['days_in_leap_month']-DAYS_IN_MONTHS[LEAP_MONTH['leap_month']-1]
        sug_year-=1
    rest_days = rest_days-leap_days
    return sug_year, rest_days

#pocet vudcovsky prestupnych dni od zacatku kalendare do `year`
def count_v_leap_days(target_year_inclusive):
    leap_days_acc = 0
    for it in range(1, int(target_year_inclusive) + 1):
        if (it % LEAP_MONTH['year_divided_by'] == 0 and not(it % LEAP_MONTH['year_not_divided_by'] == 0)):
            leap_days_acc += 1
    return leap_days_acc

#spocita kolik ubehlo celych vudcovskych roku a kolik dni
def count_v_year(days):
    rest_days = days%YEAR_DAYS
    sug_year = (days - rest_days)/YEAR_DAYS
    leap_days = count_v_leap_days(sug_year)
    if(leap_days<=rest_days):
        year = sug_year
        rest_days -= leap_days
    else:
        year, rest_days = recount_v_year(sug_year, rest_days, leap_days)
    return year, rest_days

#spocita cislo dne v tydnu
def count_v_week_day(days):
    day = (days)%DAYS_IN_WEEK
    if (day == 0):
        day = DAYS_IN_WEEK
    return day

#prevadi na vudcuv kalendar
def convert(num_days):
    week_day = count_v_week_day(num_days)
    year, rest_days = count_v_year(num_days)
    p("rest dayu je " + str(rest_days))
    if(rest_days == 0):
        return week_day, DAYS_IN_MONTHS[len(DAYS_IN_MONTHS)-1], len(DAYS_IN_MONTHS), year
    else:
        year +=1
        day, month = count_current_v_year_days(rest_days, year)
    return week_day, day, month, int(year)

#spocita pocet dni od pocatku vudcova roku do zacatku nasledujiciho roku
def count_first_year():
    not_counted_days = count_current_year_days(START_DAY, START_MONTH)
    if(is_leap(START_YEAR) and START_MONTH < 2):
        days = 366 - not_counted_days
        p("start is leap")
    else:
        days = 365 - not_counted_days
    return days

#zkontroloju, zda je 'year' prestupny
def is_leap(year):
    if (year % 100 == 0):
        if (year % 400 == 0):
            return True
        return False
    if(year%4 == 0):
        return True
    return False

#najde prvni rok delitelny 4
def find_first_potential_leap_year(year):
    for i in range (year, year-4, -1):
        if (i%4 == 0):
            return i

#spocita pocet prestupnych dni od zadaneho roku do zacatku vudcova
def count_leap_days(day, month, year):
    leap_days = 0
    if (is_leap(year) and month > 2):
        leap_days += 1

    first_leap = find_first_potential_leap_year(year-1)
    i = first_leap
    while(i > START_YEAR + 1):
        if(is_leap(i)):
            leap_days += 1
        i -= 4

    return leap_days

#spocita pocet dni v celych rocich od zacatku vudcova kalendare
def count_years(year):
    year_days = (year - START_YEAR - 1)*365
    return year_days

#spocita pocet dni v zadanem roce
def count_current_year_days(day, month):
    num_days = day
    if(month==1):
        num_days += 0
    elif(month==2):
        num_days += 31
    elif(month==3):
        num_days += 59
    elif(month==4):
        num_days += 90
    elif(month==5):
        num_days += 120
    elif(month==6):
        num_days += 151
    elif(month==7):
        num_days += 181
    elif(month==8):
        num_days += 212
    elif(month==9):
        num_days += 243
    elif(month==10):
        num_days += 273
    elif(month==11):
        num_days += 304
    elif(month==12):
        num_days += 334
    return num_days

#spocita dny, ktere ubehly od pocatku vudcova kalendare
def count_days(day, month, year):
    days = 0
    if(year > START_YEAR):
        days += count_current_year_days(day, month)
        days += count_first_year()
        days += count_leap_days(day, month, year)
        days += count_years(year)
    if(year == START_YEAR):
        days += count_current_year_days(day, month)-count_current_year_days(START_DAY, START_MONTH)
    return days
#spocita pocet dni ve vudcove roku
def count_v_year_days():
    days = 0
    for i in range(0, len(DAYS_IN_MONTHS)):
        days += DAYS_IN_MONTHS[i]
    return days

START_YEAR = 1984
START_MONTH = 8
START_DAY = 20
NUM_MONTHS = 15
DAYS_IN_MONTHS = [25,21,21,24,24,25,25,21,25,24,21,24,21,24,25]

#[month, days if leap, rule, rule exception, days if exception]
LEAP_MONTH = {'leap_month': 3,
             'days_in_leap_month': 22,
             'year_divided_by': 3,
             'year_not_divided_by': 100,
             'days_in_normal': 21}
DAYS_IN_WEEK = 9
YEAR_DAYS = count_v_year_days()
p(YEAR_DAYS)

num_inputs = int(input())
for i in range (0, num_inputs):
  nday, nmonth, nyear = map(int, input().split())
  num_days = count_days(nday, nmonth, nyear)
  p(num_days)
  week_day, day, month, year = convert(num_days+1)
  print(str(week_day) + " " + str(day) + " " + str(month) + " " + str(year))
