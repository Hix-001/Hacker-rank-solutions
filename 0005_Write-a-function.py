#05/07/2026
#Medium
#Write a function
# HackerRank: Given a year as an integer, determine if it is a leap year by evaluating if it is evenly divisible by 4, excluding century years unless divisible by 400.

def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
year = int(input("Enter a year: "))
print(is_leap(year))
