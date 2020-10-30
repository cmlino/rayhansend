from datetime import date
import calendar

def calc_easter(year):
    '''
    calculates the date of easter for the specified year

    code adapted from
    https://code.activestate.com/recipes/576517-calculate-easter-western-given-a-year/
    '''
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    return date(year, month, day)


def get_irregular_date(weekday: str, num: int, month: int, year: int) -> date:
    '''
    generates date object for an irregular date (eg. the 4th Sunday of April)

    :param weekday: the day of the week (eg. "Sunday")
    :param num: the week number (eg. 4)
    :param month: the month number (eg. 4)
    :param year: the year (eg. 2020)
    :return: a datetime.date object representing the specified irregular date
    '''
    days = {
        'Sunday': 0,
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6
    }
    day_index = days[weekday]

    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    month = cal.monthdatescalendar(year, month)
    irregular_date = month[num - 1][day_index]

    # calendar pads the start of month with days from the previous month
    # ensure we return a date from the proper month
    if irregular_date.month != month:
        irregular_date = month[num][day_index]

    return irregular_date