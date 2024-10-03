from datetime import timedelta
from random import randint

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

weekdayDict = {
            "sunday": "Sun",
            "monday": "Mon",
            "tuesday": "Tues",
            "wednesday": "Wed",
            "thursday": "Thur",
            "friday": "Fri",
            "saturday": "Sat"
        }

def generateRandomNumber(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def getDatesBetween(start_date, end_date):
    """
        @param start_date: a datetime.date object representing the beginning date
        @param end_date: a datetime.date object representing the end date

        returns an array of datetime.date objects of the dates in between the start_date and end_date
    """

    date_list = []
    curr_date = start_date

    while curr_date <= end_date:
        date_list.append(curr_date)
        curr_date += timedelta(days=1)

    return date_list

def getNumberDaysBetween(start_date, end_date):
    """
        @param start_date: a datetime.date object representing the beginning date
        @param end_date: a datetime.date object representing the end date

        returns an integer representing the number of dates between start_date and end_date
    """

    return int((end_date - start_date).days)

def getKeyByValue(value, dict):
    return {i for i in dict if dict[i]== value}