from rest_framework import serializers
from gacha.models import GachaAdmin


class GachaAdminSerializer(serializers.ModelSerializer):
    """ガチャのアイテムを登録するためのシリアライザ(admin用)"""

    class Meta:
        model = GachaAdmin
        fields = ['name', 'weight', 'rarity']


class GachaSerializer(serializers.Serializer):
    """ガチャ結果を返すためのシリアライザ"""

    CHOICE_NORMAL = "通常ガチャ"
    CHOICE_SR = "11連ガチャ(SR以上確定)"
    CHOICE_SSR = "11連ガチャ(SSR確定)"

    name = serializers.CharField(read_only=True)
    rarity = serializers.CharField(read_only=True)
    choice = serializers.ChoiceField(choices=[CHOICE_NORMAL, CHOICE_SR, CHOICE_SSR], write_only=True)
