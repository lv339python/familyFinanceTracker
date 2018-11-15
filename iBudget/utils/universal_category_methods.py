"""
This module consists methods common for different categories
(spendings, funds, incomes)
"""
from datetime import datetime, date, time


def total_value_for_category(history, last_entry=False):
    """
    Counting total value and get last or first
    registered history entry as optional arguments
    for this category
        Args:
            history: Django ORM object with history for specific category
            last_entry: ability to get last registered entry
        Returns:
            Dictionary with history info
    """
    category_info = dict(total=0)
    min_time, min_date = time.min, date.min
    category_info['last_date'] = datetime.combine(min_date, min_time)
    for i in history:
        if last_entry:
            category_info['total'] += i.value
            if i.date > category_info['last_date']:
                category_info['last_date'] = i.date
                category_info['last_value'] = i.value
    category_info['last_date'] = datetime.date(category_info['last_date'])

    return category_info
