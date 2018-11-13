"""
This module consists functions for providing history boot files
"""
from datetime import datetime


def total_value_for_category(history, last_entry=False, first_entry=False):
    category_info = dict(total=0)
    for i in history:
        category_info['total'] += i.value
        if last_entry:
            category_info['last_date'] = datetime(1, 1, 1)
            if i.date > category_info['last_date']:
                category_info['last_date'] = i.date
                category_info['last_value'] = i.value
        category_info['last_date'] = datetime.date(category_info['last_date'])
        if first_entry:
            category_info['first_date'] = datetime.today()
            if i.date < category_info['first_date']:
                category_info['first_date'] = i.date
                category_info['first_value'] = i.value
            category_info['first_date'] = datetime.date(category_info['first_date'])
    return category_info
