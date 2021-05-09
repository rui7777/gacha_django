from rest_framework import viewsets
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from gacha.models import GachaAdmin
from .serializers import GachaAdminSerializer, GachaSerializer
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
import random


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super(IsAdminUserOrReadOnly, self).has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class GachaAdminViewSet(viewsets.ModelViewSet):
    """ガチャのアイテムモデルのCRUD用APIクラス"""

    queryset = GachaAdmin.objects.all()
    serializer_class = GachaAdminSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class GachaViewSet(views.APIView):
    """ガチャのCRUD用APIクラス"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = GachaSerializer

    def post(self, request):
        queryset = GachaAdmin.objects.all()
        res = self.result(request, queryset)
        final = GachaAdmin.objects.none()
        for i, gacha_id in enumerate(res):
            final = final.union(GachaAdmin.objects.filter(id=queryset[gacha_id].id), all=True)
        data = {
            'result': GachaSerializer(final, many=True).data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def result(self, request, queryset):
        weight_normal = {1: 0.94849, 2: 0.0504, 3: 0.00111}
        weight_ten = {1: 0.90278, 2: 0.09281, 3: 0.00441}
        weight_last = {2: 0.94849, 3: 0.05151}
        weight_ssr_only = {3: 1.00}
        choice_normal = "通常ガチャ"
        choice_sr = "11連ガチャ(SR以上確定)"
        choice_ssr = "11連ガチャ(SSR確定)"

        if request.data['choice'] == choice_normal:
            return self.random_items(queryset, weight_normal, 1)
        else:
            res1 = self.random_items(queryset, weight_ten, 10)
            if request.data['choice'] == choice_sr:
                lottery_last = {key: weight_last[queryset[key].weight] for key in range(len(queryset)) if
                                queryset[key].rarity == "SR" or queryset[key].rarity == "SSR"}
                res2 = random.choices(tuple(lottery_last), weights=lottery_last.values(), k=1)
                return res1 + res2
            elif request.data['choice'] == choice_ssr:
                lottery_last = {key: weight_ssr_only[queryset[key].weight] for key in range(len(queryset)) if
                                queryset[key].rarity == "SSR"}
                res2 = random.choices(tuple(lottery_last), weights=lottery_last.values(), k=1)
                return res1 + res2

    def random_items(self, queryset, weight: dict, times: int) -> list:
        lottery = {key: weight[queryset[key].weight] for key in range(len(queryset))}
        return random.choices(tuple(lottery), weights=lottery.values(), k=times)
