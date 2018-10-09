from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import FundCategories, UserProfile

@require_http_methods(["GET"])
def show_spending_ind(request):
    """Handling request for creating of spending categories list.

        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    #user = request.user
    user = UserProfile.get_by_id(5)
    if user:
        user_funds = []
        for entry in FundCategories.filter_by_user_id(user, False):
            user_funds.append({'id': entry.id, 'name': entry.name})
        return JsonResponse(user_funds, status=200, safe=False)
    return JsonResponse({}, status=400)
