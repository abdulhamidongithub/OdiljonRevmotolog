from rest_framework.serializers import *

from .models import *

class BemorSerializer(ModelSerializer):
    class Meta:
        model = Bemor
        fields = '__all__'

class YollanmaSerializer(ModelSerializer):
    class Meta:
        model = Yollanma
        fields = '__all__'

class TolovSerializer(ModelSerializer):
    class Meta:
        model = Tolov
        fields = '__all__'

class TolovReadSerializer(ModelSerializer):
    bemor_id = BemorSerializer(read_only=True)
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

class XonaSerializer(ModelSerializer):
    class Meta:
        model = Xona
        fields = '__all__'

class JoylashtirishSerializer(ModelSerializer):
    class Meta:
        model = Joylashtirish
        fields = '__all__'

class XulosaShablonSerializer(ModelSerializer):
    class Meta:
        model = XulosaShablon
        fields = '__all__'



