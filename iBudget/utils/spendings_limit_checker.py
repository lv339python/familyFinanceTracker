"""the helper functions which checks incoming spendings, finds out if they are shared and compares
them with existing limits in that group.
If the limit is close/exceeded - it warns a user.
"""

from django.db.models import Q
from spending.models import SpendingLimitationGroup, SpendingLimitationIndividual
from spending_history.models import SpendingHistory


def comp_gr_spends_w_limit(group_id, category):
    """params:
    group_id - the id of the group for which the spending is added;
    category - the id of the category for which we check the group limits
    """
    found_limit = \
    SpendingLimitationGroup.objects.filter(spending_category_id__is_shared=True,
                                           spending_category_id__sharedspendingcategories__group_id=
                                           group_id)
    if not found_limit:
        return 'There are no limits for this group'
    list_of_limits = []
    for i in enumerate(found_limit):
        limit_amount = i[1].value
        list_of_limits.append({'limit_amount': limit_amount})
        start_date = i[1].start_date
        list_of_limits[i[0]].setdefault('start_date', start_date)
        end_date = i[1].end_date
        list_of_limits[i[0]].setdefault('end_date', end_date)

    for item in enumerate(list_of_limits):
        spendings = \
        SpendingHistory.objects.filter(spending_categories_id__is_shared=True,
                                       spending_categories_id__sharedspendingcategories__group_id=
                                       group_id, id=category, date__range=
                                       (list_of_limits[item[0]]['start_date'],
                                        list_of_limits[item[0]]['end_date']))
        if spendings:
            spent_sum = 0
            for i in spendings:
                spent_sum = spent_sum + i.value
            spent_sum = int(spent_sum)
            ten_percent_of_limit = list_of_limits[item[0]]['limit_amount']/10
            if spent_sum > list_of_limits[item[0]]['limit_amount']:
                return 'Warning! The group limit for this spendings is exceeded! Do not spend' \
                       ' more on this category!!!'
            if spent_sum - list_of_limits[item[0]]['limit_amount'] <= ten_percent_of_limit:
                return 'Attention! You approached the limit for this spending very closely! Cut' \
                       ' your spendings!!!'

    return 'Group limits are fine for now!'

def compare_ind_spend_limit(user, current_date, spending, current_value):
    """Creating data for spending limitation tracking.
        Args:
            user (UserProfile): user.
            current_date (date): date for limitation tracking
            spending (SpendingCategories): spending category for tracking
        Returns:
            ... about current spending limitation on this category.
    """
    find_limit = \
    SpendingLimitationIndividual.objects.filter(
        Q(start_date__lte=current_date) &
        Q(finish_date__gte=current_date)).filter(user=user, spending_category=spending)
    if not find_limit:
        return 'There are no individual limits on including this date period.'

    response = ''
    for item in find_limit:
        total = sum(SpendingHistory.objects.filter(
            owner=user,
            spending_categories=spending,
            date__range=[item.start_date, item.finish_date]).values_list('value', flat=True))
        if total >= item.value:
            response += f"Warning! Your spending limit {item.value} " \
                        f"for the period from {item.start_date} to " \
                        f"{item.finish_date} is exceeded. " \
                        f"You have already spent {total}! \n"
        elif current_value >= item.value - total:
            response += f"Warning! You've set spending limit {item.value} " \
                        f"for the period from {item.start_date} to {item.finish_date} " \
                        f"on this category. " \
                        f"Registering value {current_value} exceeds specified limit. \n"
        else:
            response += f"You've set spending limit {item.value} " \
                        f"for the period from {item.start_date} to {item.finish_date} " \
                        f"on this category. " \
                        f"Now your spending are {round((current_value +total)/item.value*100, 2)}" \
                        f"percentages of the specified limit. \n"
    return response
