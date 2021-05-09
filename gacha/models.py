import uuid
from django.db import models


class GachaAdmin(models.Model):
    """ガチャのアイテムモデル(admin用)"""

    class Meta:
        db_table = 'gacha'

    RARITY_SSR = "SSR"
    RARITY_SR = "SR"
    RARITY_R = "R"
    RARITY_SET = (
        (RARITY_SSR, "SSR"),
        (RARITY_SR, "SR"),
        (RARITY_R, "R"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='名前', max_length=20)
    weight = models.IntegerField(verbose_name='重み', null=False, blank=False)
    rarity = models.CharField(verbose_name='レア度', choices=RARITY_SET, default=RARITY_R, max_length=8)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
