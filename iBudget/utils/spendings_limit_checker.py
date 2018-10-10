"""the helper functions which checks incoming spendings, finds out if they are shared and compares
them with existing limits in that group.
If the limit is close/exceeded - it warns a user.
"""

from spending.models import SpendingLimitationGroup
from spending_history.models import SpendingHistory


def comp_gr_spends_w_limit(group_id):
    """params:
    group_id - the id of the group for which the spending is added
    """
    find_limit = \
    SpendingLimitationGroup.objects.filter(spending_category_id__is_shared=True,
                                           spending_category_id__sharedspendingcategories__group_id=
                                           group_id).distinct('value')
    if not find_limit:
        return 'There are no limits for this group'
    list_of_values = {}
    for i in find_limit:
        limit_amount = i.value
        list_of_values.setdefault('limit_amount', limit_amount)
        start_date = i.start_date
        list_of_values.setdefault('start_date', start_date)
        end_date = i.end_date
        list_of_values.setdefault('end_date', end_date)

    spendings = \
    SpendingHistory.objects.filter(spending_categories_id__is_shared=True,
                                   spending_categories_id__sharedspendingcategories__group_id=
                                   group_id, date__range=(list_of_values['start_date'],
                                                          list_of_values['end_date']))
    spent_sum = 0
    for i in spendings:
        spent_sum = spent_sum + i.value
        print(spent_sum)
    spent_sum = int(spent_sum)
    print(spent_sum)


    if spent_sum > list_of_values['limit_amount']:
        return 'Warning! The limit is exceeded! Do not spend more on this category'
    if spent_sum - list_of_values['limit_amount'] <= 100:
        return 'Attention! You approach the limit for this category! Cut your spendings!'


    return None
