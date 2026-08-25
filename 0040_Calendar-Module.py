#07/07/2026
#Easy
#Calendar Module
# HackerRank: Determine the day of the week for a given date using the standard calendar module.

import calendar
if __name__ == '__main__':
    month, day, year = map(int, input().split())
    print(calendar.day_name[calendar.weekday(year, month, day)].upper())
