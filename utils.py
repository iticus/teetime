'''
Created on May 18, 2016

@author: ionut
'''

import datetime


DAY_NUM = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}


def days_to_dates(days):
    dates = []
    for day in days:
        today = datetime.datetime.today()
        if today.weekday() == DAY_NUM[day]:
            dates.append(today+datetime.timedelta(days=14))
        else:
            while today.weekday() != DAY_NUM[day]:
                today = today + datetime.timedelta(days=1)
            today = today + datetime.timedelta(days=7)
            dates.append(today)
            
    return dates
            

def timestr_to_seconds(timestr):
    seconds = 0
    t, a = timestr.split(' ')
    if a.strip().lower() == 'pm':
        seconds += 43200
    h,m = t.split(':')
    if h == '12':
        h = '0'
    seconds += 3600 * int(h) + 60 * int(m)
    return seconds


def sort_elements(elements):
    data = []
    for element in elements:
        tms = element.find_elements_by_class_name('PodLabel_TeeTime')
        for tm in tms: 
            data.append([timestr_to_seconds(tm.get_attribute('innerHTML')), element])
            
    data.sort(key=lambda x: x[0])
    data = [x[1] for x in data]
    return data