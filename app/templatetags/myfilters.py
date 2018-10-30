from django import template
register = template.Library()
from django.utils import timezone
from . import jalali


def persian_month(data):
	month = {
		'1': 'فروردین', '2': 'اردیبهشت', '3': 'خرداد',
		'4': 'تیر', '5': 'مرداد', '6': 'شهریور',
		'7': 'مهر', '8': 'آبان', '9': 'آذر',
		'10': 'دی', '11': 'بهمن', '12': 'اسفند',
	}
	for key, value in month.items():
		data = data.replace(key, value)
	return data

def persian_numbers(data):
	numbers = {
		'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
		'5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹',
	}
	for key, value in numbers.items():
		data = data.replace(key, value)
	return data

@register.filter(name = 'persian')
def datetime_persian(self):
	mydatetime 	= self
	mydatetime 	= timezone.localtime(mydatetime)

	mydate 		= mydatetime.strftime('%Y-%m-%d')
	myjtime		= mydatetime.strftime('%H-%M').split('-')
	myjdate 	= jalali.Gregorian(mydate).persian_string().split('-')
	myjdatetime	= myjdate + myjtime

	myjdatetime[1] = persian_month(myjdatetime[1])
	myjdatetime    = [persian_numbers(i) for i in myjdatetime]

	return "{} {} {} ساعت {}:{}".format(
		myjdatetime[2],
		myjdatetime[1],
		myjdatetime[0],
		myjdatetime[3],
		myjdatetime[4],
	)


