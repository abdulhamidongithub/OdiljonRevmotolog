from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
import datetime

from .serializers import *
from .models import *

class BemorModelViewSet(ModelViewSet):
    queryset = Bemor.objects.all()
    serializer_class = BemorSerializer

    @action(detail=True)
    def tolovlar(self, request, pk):
        bemor = Bemor.objects.get(id=pk)
        payments = Tolov.objects.filter(bemor_id=bemor)
        query = self.request.query_params.get('tolandi')
        date = self.request.query_params.get('sana')
        print(query, type(query))
        if query is not None:
            if query == 'True':
                payments = Tolov.objects.filter(bemor_id__id=pk, tolandi=True)
            elif query == 'False':
                payments = Tolov.objects.filter(bemor_id__id=pk, tolandi=False)
        if date:
            payments = payments.filter(sana=date)
        serializer = TolovReadSerializer(payments, many=True)
        return Response(serializer.data)

class TolovModelViewSet(ModelViewSet):
    queryset = Tolov.objects.all()
    serializer_class = TolovSerializer

    def get_queryset(self):
        search_word = self.request.query_params.get('qayerga')
        xulosa_status = self.request.query_params.get('xulosa_holati')
        date = self.request.query_params.get('sana')
        queryset = Tolov.objects.all()
        if search_word:
            queryset = queryset.filter(yollanma_id__qayerga__contains=search_word)
        if xulosa_status:
            queryset = queryset.filter(xulosa_holati=xulosa_status)
        if date:
            queryset = queryset.filter(sana=date)
        return queryset

    def list(self, request, *args, **kwargs):
        search_word = self.request.query_params.get('qayerga')
        xulosa_status = self.request.query_params.get('xulosa_holati')
        date = self.request.query_params.get('sana')
        queryset = Tolov.objects.all()
        if search_word:
            queryset = queryset.filter(yollanma_id__qayerga__contains=search_word)
        if xulosa_status:
            queryset = queryset.filter(xulosa_holati=xulosa_status)
        if date:
            queryset = queryset.filter(sana=date)
        serializer = TolovReadSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TolovReadSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        tolov = request.data
        serializer = TolovSerializer(data=tolov)
        if serializer.is_valid():
            serializer.save(xulosa_holati="Topshirilyapti")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class XulosaModelViewSet(ModelViewSet):
    queryset = Xulosa.objects.all()
    serializer_class = XulosaSerializer

    def list(self, request, *args, **kwargs):
        queryset = Xulosa.objects.all()
        serializer = XulosaReadSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = XulosaReadSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        xulosa = request.data
        serializer = XulosaSerializer(data=xulosa)
        if serializer.is_valid():
            serializer.save()
            tolov = Tolov.objects.get(id=xulosa.get('tolov_id'))
            tolov.xulosa_holati = 'Kiritildi'
            tolov.ozgartirilgan_sana = datetime.date.today()
            tolov.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class XonaModelViewSet(ModelViewSet):
    queryset = Xona.objects.all()
    serializer_class = XonaSerializer

class JoylashtirishModelViewSet(ModelViewSet):
    queryset = Joylashtirish.objects.all()
    serializer_class = JoylashtirishSerializer

    def list(self, request, *args, **kwargs):
        serializer = JoylashtirishReadSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        serializer = JoylashtirishReadSerializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        joylashish = request.data
        qarovchi_bor = joylashish.get('qarovchi')
        xona = Xona.objects.get(id=joylashish.get('xona_id'))
        if (qarovchi_bor and xona.bosh_joy_soni < 2) or (qarovchi_bor == False and xona.bosh_joy_soni < 1):
            return Response({"xabar": "Yetarli bo'sh joy mavjud emas"})
        serializer = JoylashtirishSerializer(data=joylashish)
        if serializer.is_valid():
            serializer.save()
            joy = Joylashtirish.objects.get(id=serializer.data.get('id'))
            patient = Bemor.objects.get(id=joy.bemor_id.id)
            if joy.yotgan_kun_soni:
                s = int(joy.yotgan_kun_soni) * int(joy.xona_id.joy_narxi)
            else:
                s = 0
            Tolov.objects.create(
                bemor_id = patient,
                joylashtirish_id = joy,
                summa = s
            )
            patient.joylashgan = True
            patient.save()
            if qarovchi_bor:
                xona.bosh_joy_soni -= 2
            else:
                xona.bosh_joy_soni -= 1
            xona.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        joylashtirish = self.get_object()
        data = request.data
        serializer = JoylashtirishSerializer(joylashtirish, data=data)
        if serializer.is_valid():
            serializer.save()
            patient = Bemor.objects.get(id=joylashtirish.bemor_id.id)
            patient.joylashgan = False
            patient.save()
            xona = Xona.objects.get(id=joylashtirish.xona_id.id)
            if joylashtirish.qarovchi:
                xona.bosh_joy_soni += 2
            else:
                xona.bosh_joy_soni += 1
            xona.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class XulosaShablonModelViewSet(ModelViewSet):
    queryset = XulosaShablon.objects.all()
    serializer_class = XulosaShablonSerializer

class YollanmaModelViewSet(ModelViewSet):
    queryset = Yollanma.objects.all()
    serializer_class = YollanmaSerializer

class BoshXonalarModelViewSet(ModelViewSet):
    queryset = Xona.objects.filter(bosh_joy_soni__gt=0)
    serializer_class = XonaSerializer

    def get_queryset(self):
        qarovchisi = self.request.query_params.get('qarovchi')
        turi = self.request.query_params.get('tur')
        natija = Xona.objects.filter(bosh_joy_soni__gt=0)
        if qarovchisi and qarovchisi == 'True':
            natija = natija.filter(bosh_joy_soni__gt=1)
        if turi:
            natija = natija.filter(turi=turi)
        return natija

