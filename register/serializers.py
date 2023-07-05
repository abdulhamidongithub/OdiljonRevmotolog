from django.contrib.auth.models import User
from rest_framework.serializers import *

from .models import *


class BemorSerializer(ModelSerializer):
    class Meta:
        model = Bemor
        fields = '__all__'

    def to_representation(self, instance):
        data = super(BemorSerializer, self).to_representation(instance)
        hozirgi_bemor = Bemor.objects.get(id=data.get('id'))
        joylashishlar = Joylashtirish.objects.filter(bemor_id=hozirgi_bemor)
        serializer_ = JoylashtirishSerializer(joylashishlar, many=True)
        tolovlari = Tolov.objects.filter(bemor_id=hozirgi_bemor)
        serializer = TolovReadBemorUchun(tolovlari, many=True)
        data.update({'tolovlar': serializer.data, 'joylashishlar': serializer_.data})
        return data


class XulosaShablonSerializer(ModelSerializer):
    class Meta:
        model = XulosaShablon
        fields = '__all__'

class YollanmaSerializer(ModelSerializer):
    xulosa_shablon_id = XulosaShablonSerializer(read_only=True)
    class Meta:
        model = Yollanma
        fields = '__all__'

class TolovSerializer(ModelSerializer):
    class Meta:
        model = Tolov
        fields = '__all__'

class XonaSerializer(ModelSerializer):
    class Meta:
        model = Xona
        fields = '__all__'

class JoylashtirishSerializer(ModelSerializer):
    class Meta:
        model = Joylashtirish
        fields = '__all__'

class JoylashtirishReadSerializer(ModelSerializer):
    xona_id = XonaSerializer(read_only=True)
    class Meta:
        model = Joylashtirish
        fields = '__all__'

class TolovReadSerializer(ModelSerializer):
    # bemor_id = BemorSerializer(read_only=True)
    yollanma_id = YollanmaSerializer(read_only=True)
    joylashtirish_id = JoylashtirishReadSerializer(read_only=True)
    class Meta:
        model = Tolov
        fields = '__all__'

class TolovReadBemorUchun(ModelSerializer):
    yollanma_id = YollanmaSerializer(read_only=True)
    class Meta:
        model = Tolov
        fields = '__all__'

class XulosaSerializer(ModelSerializer):
    class Meta:
        model = Xulosa
        fields = '__all__'

class XulosaReadSerializer(ModelSerializer):
    tolov_id = TolovReadSerializer(read_only=True)
    class Meta:
        model = Xulosa
        fields = '__all__'


class TolovQaytarishSerializer(ModelSerializer):
    class Meta:
        model = TolovQaytarish
        fields = '__all__'


class TolovPatch(ModelSerializer):
    class Meta:
        model = Tolov
        fields =["tolangan_summa", "tolangan_sana", "tolandi"]


