from django import template
from portal.models import TestHour, Test

register = template.Library()


@register.filter(name='uppercase')
def uppercase_filter(value):
    return value.upper()


@register.filter(name='time')
def get_time_filter(test_id):
    test = Test.objects.get(id=test_id)
    time = TestHour.objects.get(test=test)

    hours = str(time.time.hour)
    minutes = str(time.time.minute)
    seconds = str(time.time.second)

    if(len(hours) == 0):
        hours = "00"
    if(len(minutes) == 0):
        minutes = "00"
    if(len(seconds) == 0):
        seconds = "00"

    if(len(hours) == 1):
        hours = '0'+hours
    if(len(minutes) == 1):
        minutes = '0'+minutes
    if(len(seconds) == 1):
        seconds = '0'+seconds
    
    string_time = f"{hours}:{minutes}:{seconds}"

    return string_time
