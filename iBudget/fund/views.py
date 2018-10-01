from django.views.decorators.http import require_http_methods
from .models import FundCategories
from django.http import JsonResponse


@require_http_methods(["GET"])
def show_fund_ind(request):
    """Handling request for creating of fund_id list.
        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    if user:
        user_card = []
        for entry in FundCategories.objects.filter(owner=user):
            user_card.append({'id': entry.id, 'name': entry.name})
            print(user_card)

        return JsonResponse(user_card, status=200, safe=False)
    return JsonResponse({}, status=400)
