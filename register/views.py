from django.db import transaction
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
import datetime
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination

from .serializers import *
from .models import *

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer

class BemorModelViewSet(ModelViewSet):
    queryset = Bemor.objects.all()
    serializer_class = BemorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = Bemor.objects.all()
        qidiruv = self.request.query_params.get('qidiruv')
        t_date = self.request.query_params.get('tolov_date')
        tolandi = self.request.query_params.get('tolov_tolandi')
        y_id = self.request.query_params.get('yollanma_id')
        t_from_date = self.request.query_params.get('tolov_from_date')
        t_to_date = self.request.query_params.get('tolov_to_date')
        j_id = self.request.query_params.get('joylashtirish_id')
        qayerga = self.request.query_params.get('qayerga')
        sana = self.request.query_params.get('sana')
        joylashgan = self.request.query_params.get('joylashgan')
        tolov_sana = self.request.query_params.get('tolov_sana')
        ozgartirilgan_sana = self.request.query_params.get('ozgartirilgan_sana')
        xulosa_holati=self.request.query_params.get('xulosa_holati')
        if qidiruv:
            queryset = queryset.filter(ism__icontains=qidiruv)|queryset.filter(
                familiya__icontains=qidiruv)|queryset.filter(sharif__icontains=qidiruv)|queryset.filter(
                tel__icontains=qidiruv)
        if joylashgan and tolov_sana is None and sana is None:
            queryset = queryset.filter(joylashgan=True)
        elif sana and joylashgan and tolov_sana:
            tolovlar = Tolov.objects.filter(tolangan_sana=tolov_sana).values("bemor_id").distinct()
            queryset = queryset.filter(joylashgan=True) | queryset.filter(royhatdan_otgan_sana=sana)
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        if tolandi is not None:
            tolovlar = Tolov.objects.filter(tolandi=False).values("bemor_id").distinct()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        if j_id and tolandi is not None and t_date:
            queryset = Bemor.objects.none()
            tolovlar = Tolov.objects.filter(tolandi=False, joylashtirish_id__isnull=False).values("bemor_id").distinct() | Tolov.objects.filter(
                sana=t_date, joylashtirish_id__isnull=False).values("bemor_id").distinct() | Tolov.objects.filter(
                tolangan_sana=t_date, joylashtirish_id__isnull=False).values("bemor_id").distinct()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        elif y_id and tolandi is not None and t_date:
            tolovlar = Tolov.objects.filter(tolandi=False, yollanma_id__isnull=False).values("bemor_id").distinct() | Tolov.objects.filter(
                sana=t_date, yollanma_id__isnull=False).values("bemor_id").distinct() | Tolov.objects.filter(
                tolangan_sana=t_date, yollanma_id__isnull=False).values("bemor_id").distinct()
            queryset = Bemor.objects.none()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        elif t_date and y_id:
            tolovlar = Tolov.objects.filter(sana=t_date, joylashtirish_id__isnull=True
                                ).values("bemor_id").distinct()|Tolov.objects.filter(
                tolangan_sana=t_date, joylashtirish_id__isnull=True).values("bemor_id").distinct()
            queryset = Bemor.objects.none()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        elif t_date and j_id:
            tolovlar = Tolov.objects.filter(sana=t_date, yollanma_id__isnull=True).values("bemor_id").distinct() | Tolov.objects.filter(
                tolangan_sana=t_date, yollanma_id__isnull=True).values("bemor_id").distinct()
            queryset = Bemor.objects.none()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        elif t_date and qayerga:
            tolovlar = Tolov.objects.filter(sana=t_date, yollanma_id__qayerga=qayerga).values("bemor_id").distinct() | Tolov.objects.filter(
                tolangan_sana=t_date, yollanma_id__qayerga=qayerga).values("bemor_id").distinct()
            queryset = Bemor.objects.none()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        elif qayerga and xulosa_holati and ozgartirilgan_sana:
            tolovlar = Tolov.objects.filter(yollanma_id__qayerga=qayerga, ozgartirilgan_sana=ozgartirilgan_sana, xulosa_holati=xulosa_holati).values("bemor_id").distinct() | Tolov.objects.filter(
                xulosa_holati=xulosa_holati, ozgartirilgan_sana=ozgartirilgan_sana, yollanma_id__qayerga=qayerga).values("bemor_id").distinct()
            queryset = Bemor.objects.none()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        elif qayerga and xulosa_holati:
            tolovlar = Tolov.objects.filter(yollanma_id__qayerga=qayerga, xulosa_holati=xulosa_holati).values("bemor_id").distinct() | Tolov.objects.filter(
                xulosa_holati=xulosa_holati, yollanma_id__qayerga=qayerga).values("bemor_id").distinct()
            queryset = Bemor.objects.none()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        elif t_from_date and t_to_date and y_id:
            tolovlar = Tolov.objects.filter(sana__range=(t_from_date, t_to_date), joylashtirish_id__isnull=True).values("bemor_id").distinct() | Tolov.objects.filter(
                tolangan_sana__range=(t_from_date, t_to_date), joylashtirish_id__isnull=True).values("bemor_id").distinct()
            queryset = Bemor.objects.none()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        elif t_from_date and t_to_date and j_id:
            tolovlar = Tolov.objects.filter(sana__range=(t_from_date, t_to_date), yollanma_id__isnull=True).values("bemor_id").distinct() | Tolov.objects.filter(
                tolangan_sana__range=(t_from_date, t_to_date), yollanma_id__isnull=True).values("bemor_id").distinct()
            queryset = Bemor.objects.none()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        elif t_from_date and t_to_date and qayerga:
            tolovlar = Tolov.objects.filter(sana__range=(t_from_date, t_to_date),
                                            yollanma_id__qayerga=qayerga).values("bemor_id").distinct() | Tolov.objects.filter(
                tolangan_sana__range=(t_from_date, t_to_date), yollanma_id__qayerga=qayerga).values("bemor_id").distinct()
            queryset = Bemor.objects.none()
            for tolov in tolovlar:
                queryset = queryset | Bemor.objects.filter(id=tolov.get('bemor_id'))
        return queryset

    @action(detail=True)
    def tolovlar(self, request, pk):
        tolovlar = Tolov.objects.filter(joylashtirish_id__isnull=False, joylashtirish_id__ketish_sanasi__isnull=True)
        for tolov in tolovlar:
            joy = Joylashtirish.objects.get(id=tolov.joylashtirish_id.id)
            boshi = datetime.datetime.strptime(str(joy.kelish_sanasi), "%Y-%m-%d")
            oxiri = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
            joy.yotgan_kun_soni = abs((boshi - oxiri).days) + 1
            if joy.qarovchi:
                s = int(joy.yotgan_kun_soni) * int(joy.xona_id.joy_narxi) * 2
            else:
                s = int(joy.yotgan_kun_soni) * int(joy.xona_id.joy_narxi)
            joy.save()
            tolov.summa = s
            tolov.save()
        bemor = Bemor.objects.get(id=pk)
        payments = Tolov.objects.filter(bemor_id=bemor)
        query = self.request.query_params.get('tolandi')
        date = self.request.query_params.get('sana')
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
        t_date = self.request.query_params.get('tolangan_sana')
        bemor = self.request.query_params.get('bemor_id')
        tolandi = self.request.query_params.get('tolandi')
        queryset = Tolov.objects.all()
        if bemor and (tolandi is not None or t_date or date):
            queryset = queryset.filter(bemor_id__id=int(bemor))
            if date:
               queryset = queryset.filter(sana = date)
            elif t_date:
                tolovs = Tolov.objects.filter(id=None)
                for obj in queryset:
                    for item in obj.tolangan_summa:
                        if item.get('sana') == t_date:
                            tolovs = tolovs | Tolov.objects.filter(id=obj.id)
                            break
                queryset = tolovs
            else:
                if tolandi == 'false':
                    queryset = queryset.filter(tolandi=False)
                else:
                    queryset = queryset.filter(tolandi=True)
        elif search_word:
            queryset = queryset.filter(yollanma_id__qayerga__contains=search_word)
        elif xulosa_status:
            queryset = queryset.filter(xulosa_holati=xulosa_status)
        elif date:
            queryset = queryset.filter(sana=date)
        serializer = TolovReadSerializer(queryset, many=True)
        tolovlar = Tolov.objects.filter(joylashtirish_id__isnull=False, joylashtirish_id__ketish_sanasi__isnull=True)
        for tolov in tolovlar:
            joy = Joylashtirish.objects.get(id=tolov.joylashtirish_id.id)
            boshi = datetime.datetime.strptime(str(joy.kelish_sanasi), "%Y-%m-%d")
            oxiri = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
            joy.yotgan_kun_soni = abs((boshi - oxiri).days) + 1
            if joy.qarovchi:
                s = int(joy.yotgan_kun_soni) * int(joy.xona_id.joy_narxi) * 2
            else:
                s = int(joy.yotgan_kun_soni) * int(joy.xona_id.joy_narxi)
            joy.save()
            tolov.summa = s
            tolov.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TolovReadSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        tolov = request.data
        serializer = TolovSerializer(data=tolov)
        if serializer.is_valid():
            with transaction.atomic():
                t = 0
                tolangan_amount = serializer.validated_data.get("tolangan_summa")
                for i in tolangan_amount:
                    t += int(i.get('summa'))
                if t == serializer.validated_data.get("summa"):
                    serializer.save(xulosa_holati="Topshirilyapti", tolandi=True, haqdor=False)
                elif t > serializer.validated_data.get("summa"):
                    serializer.save(xulosa_holati="Topshirilyapti", tolandi=False, haqdor=True)
                elif t < serializer.validated_data.get("summa"):
                    serializer.save(xulosa_holati="Topshirilyapti", tolandi=False, haqdor=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        tolov = request.data
        t = self.get_object()
        serializer = TolovPatch(t, data=tolov)
        if serializer.is_valid():
            t_summa = 0
            tolangan_amount = serializer.validated_data.get("tolangan_summa")
            for i in tolangan_amount:
                t_summa += int(i.get('summa'))
            if (t.joylashtirish_id is not None and t.joylashtirish_id.ketish_sanasi is not None and t.summa == t_summa) or (t.yollanma_id is not None and t.summa == t_summa):
                t.tolandi = True
            elif t.joylashtirish_id is not None and t.joylashtirish_id.ketish_sanasi is not None and t.summa < t_summa:
                t.tolandi = False
                t.haqdor = True
            else:
                t.tolandi = False
            t.tolangan_summa = serializer.validated_data.get('tolangan_summa')
            t.tolangan_sana = serializer.validated_data.get('tolangan_sana')
            t.xulosa_holati = serializer.validated_data.get('xulosa_holati')
            t.tolov_qaytarildi = serializer.validated_data.get("tolov_qaytarildi")
            t.izoh = serializer.validated_data.get("izoh")
            t.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class XulosaModelViewSet(ModelViewSet):
    queryset = Xulosa.objects.all()
    serializer_class = XulosaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        bemori = self.request.query_params.get("bemor_id")
        queryset = self.queryset
        if bemori:
            tolovlar = Tolov.objects.filter(bemor_id__in=Bemor.objects.filter(id=int(bemori)))
            queryset = queryset.filter(tolov_id__in=tolovlar)
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
            with transaction.atomic():
                tolov = Tolov.objects.get(id=xulosa.get('tolov_id'))
                tolov.xulosa_holati = 'Kiritildi'
                tolov.ozgartirilgan_sana = datetime.date.today()
                tolov.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class XonaModelViewSet(ModelViewSet):
    queryset = Xona.objects.all()
    serializer_class = XonaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class JoylashtirishModelViewSet(ModelViewSet):
    queryset = Joylashtirish.objects.all()
    serializer_class = JoylashtirishSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        ketish_sana = self.request.query_params.get("ketish_sanasi")
        queryset = self.queryset
        if ketish_sana is not None:
            queryset = queryset.filter(ketish_sanasi__isnull=True)
        serializer = JoylashtirishReadSerializer(queryset, many=True)
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
            with transaction.atomic():
                serializer.save()
                joy = Joylashtirish.objects.get(id=serializer.data.get('id'))
                patient = Bemor.objects.get(id=joy.bemor_id.id)
                boshi = datetime.datetime.strptime(str(joy.kelish_sanasi), "%Y-%m-%d")
                oxiri = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
                joy.yotgan_kun_soni = abs((boshi-oxiri).days) + 1
                if joy.qarovchi:
                    s = int(joy.yotgan_kun_soni) * int(joy.xona_id.joy_narxi) * 2
                else:
                    s = int(joy.yotgan_kun_soni) * int(joy.xona_id.joy_narxi)
                joy.save()
                Tolov.objects.create(
                    bemor_id = patient,
                    joylashtirish_id = joy,
                    summa = s,
                    tolangan_summa = []
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
        # current_time = datetime.datetime.now()
        # current_hour = current_time.hour
        # current_minutes = current_time.minute
        joylashtirish = self.get_object()
        data = request.data
        serializer = JoylashtirishSerializer(joylashtirish, data=data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                patient = Bemor.objects.get(id=joylashtirish.bemor_id.id)
                patient.joylashgan = False
                patient.save()
                tolov = Tolov.objects.get(joylashtirish_id=joylashtirish)
                xona = Xona.objects.get(id=joylashtirish.xona_id.id)
                # boshi = datetime.datetime.strptime(str(joylashtirish.kelish_sanasi), "%Y-%m-%d")
                # oxiri = datetime.datetime.strptime(str(joylashtirish.ketish_sanasi), "%Y-%m-%d")
                # if (current_hour >= 13) or (current_hour == 12 and current_minutes > 30):
                #     joylashtirish.yotgan_kun_soni = abs((boshi - oxiri).days) + 1
                # else:
                #     joylashtirish.yotgan_kun_soni = abs((boshi - oxiri).days)
                # joylashtirish.save()
                if joylashtirish.qarovchi:
                    if joylashtirish.ketish_sanasi:
                        xona.bosh_joy_soni += 2
                    s = int(joylashtirish.yotgan_kun_soni) * int(joylashtirish.xona_id.joy_narxi) * 2
                else:
                    if joylashtirish.ketish_sanasi:
                        xona.bosh_joy_soni += 1
                    s = int(joylashtirish.yotgan_kun_soni) * int(joylashtirish.xona_id.joy_narxi)
                tolov.summa = s
                tolanganlar = 0
                for i in tolov.tolangan_summa:
                    tolanganlar += i.get('summa')
                if tolov.summa < tolanganlar:
                    tolov.haqdor = True
                    tolov.tolandi = False
                elif tolov.summa == tolanganlar:
                    tolov.tolandi = True
                    tolov.haqdor = False
                tolov.save()
                xona.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class XulosaShablonModelViewSet(ModelViewSet):
    queryset = XulosaShablon.objects.all()
    serializer_class = XulosaShablonSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class YollanmaModelViewSet(ModelViewSet):
    queryset = Yollanma.objects.all()
    serializer_class = YollanmaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class BoshXonalarModelViewSet(ModelViewSet):
    queryset = Xona.objects.filter(bosh_joy_soni__gt=0)
    serializer_class = XonaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qarovchisi = self.request.query_params.get('qarovchi')
        turi = self.request.query_params.get('tur')
        natija = Xona.objects.filter(bosh_joy_soni__gt=0)
        if qarovchisi and qarovchisi == 'True':
            natija = natija.filter(bosh_joy_soni__gt=1)
        if turi:
            natija = natija.filter(turi=turi)
        return natija

class TolovQaytarishViewSet(ModelViewSet):
    queryset = TolovQaytarish.objects.all()
    serializer_class = TolovQaytarishSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        d = self.request.data
        serializer = TolovQaytarishSerializer(data=d)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                tolov = Tolov.objects.get(id=d.get('tolov_id'))
                tolov.tolangan_summa.append({"sana": str(datetime.date.today()), "summa": -(serializer.validated_data.get('summa'))})
                t = 0
                for i in tolov.tolangan_summa:
                    t += int(i.get("summa"))
                if t == tolov.summa:
                    tolov.haqdor = False
                    tolov.tolandi = True
                elif t > tolov.summa:
                    tolov.haqdor = True
                    tolov.tolandi = False
                else:
                    tolov.haqdor = False
                    tolov.tolandi = False
                tolov.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChekModelViewSet(ModelViewSet):
    queryset = Chek.objects.all()
    serializer_class = ChekSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Chek.objects.all()
        bemor = self.request.query_params.get("bemor_id")
        oxirgisi = self.request.query_params.get("oxirgisi")
        if bemor:
            queryset = queryset.filter(bemor_id__id=int(bemor))
        elif oxirgisi:
            queryset = queryset.filter(id=queryset.last().id)
        return queryset

    def create(self, request, *args, **kwargs):
        check_to_be_created = request.data
        serializer = ChekSerializer(data=check_to_be_created)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                tolovlar = check_to_be_created.get('tolov_maqsadlar')
                for i in tolovlar:
                    tolov = Tolov.objects.get(id=i.get('tolov_id'))
                    if tolov.tolandi != True:
                        tolov.tolangan_summa.append({"summa": int(i.get('summa')), "sana": check_to_be_created.get('sana')})
                        tolov.tolangan_sana = check_to_be_created.get('sana')
                        if tolov.yollanma_id:
                            tolov.tolandi = True
                        else:
                            t = 0
                            for i in tolov.tolangan_summa:
                                if i.get('summa'):
                                    t += i.get("summa")
                            if t == tolov.summa and tolov.joylashtirish_id.ketish_sanasi is not None:
                                tolov.tolandi = True
                            elif t < tolov.summa:
                                tolov.tolandi = False
                            elif t > tolov.summa and tolov.joylashtirish_id.ketish_sanasi is not None:
                                tolov.haqdor = True
                                tolov.tolandi = False
                            elif t > tolov.summa:
                                tolov.tolandi = False
                    tolov.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TolovlarAPIView(APIView):
    serializer_class = TolovAdminSerializer
    def get(self, request):
        queryset = Tolov.objects.all()
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        by_date = self.request.query_params.get('by_date')
        search_word = self.request.query_params.get("qayerga")
        joylashtirish = self.request.query_params.get('joylashtirish_id')
        yollanma = self.request.query_params.get('yollanma_id')
        qaytarildi = self.request.query_params.get('tolov_qaytarildi')
        tolandi = self.request.query_params.get('tolandi')
        search = self.request.query_params.get('search')
        pagination_class = PageNumberPagination
        pagination_class.page_size = 30
        paginator = PageNumberPagination()
        if search:
            queryset = queryset.filter(bemor_id__ism__icontains=search) | queryset.filter(
                bemor_id__familiya__icontains=search) | queryset.filter(bemor_id__sharif__icontains=search) | queryset.filter(
                bemor_id__tel__icontains=search)
            if yollanma:
                queryset = queryset.filter(yollanma_id__isnull=False)
            elif joylashtirish:
                queryset = queryset.filter(joylashtirish_id__isnull=False)
            elif search_word:
                queryset = queryset.filter(yollanma_id__qayerga=search_word)
        if from_date and to_date and search_word:
            queryset = queryset.filter(sana__range=(from_date, to_date), yollanma_id__qayerga=search_word,
                            tolangan_sana__isnull=True) | queryset.filter(
                tolangan_sana__range=(from_date, to_date), yollanma_id__qayerga=search_word)
        elif search_word and by_date:
            queryset = queryset.filter(sana=by_date, yollanma_id__qayerga=search_word,
                                       tolangan_sana__isnull=True) | queryset.filter(
                tolangan_sana=by_date, yollanma_id__qayerga=search_word)
        elif from_date and to_date and joylashtirish:
            queryset = queryset.filter(sana__range=(from_date, to_date), joylashtirish_id__isnull=False,
                            tolangan_sana__isnull=True) | queryset.filter(
                tolangan_sana__range=(from_date, to_date), joylashtirish_id__isnull=False)
            all_objects = Tolov.objects.filter(joylashtirish_id__isnull=False, tolandi=False)
            tolovs = Tolov.objects.filter(id=None)
            for obj in all_objects:
                for item in obj.tolangan_summa:
                    if item.get('sana') == by_date:
                        tolovs = tolovs | Tolov.objects.filter(id=obj.id)
                        break
            queryset = queryset | tolovs
        elif joylashtirish and by_date:
            queryset = queryset.filter(sana=by_date, joylashtirish_id__isnull=False,
                                       tolangan_sana__isnull=True) | queryset.filter(
                tolangan_sana=by_date, joylashtirish_id__isnull=False)
            all_objects = Tolov.objects.filter(joylashtirish_id__isnull=False, tolandi=False)
            tolovs = Tolov.objects.filter(id=None)
            for obj in all_objects:
                for item in obj.tolangan_summa:
                    if item.get('sana') == by_date:
                        tolovs = tolovs | Tolov.objects.filter(id=obj.id)
                        break
            queryset = queryset | tolovs
        elif from_date and to_date and yollanma:
            queryset = queryset.filter(sana__range=(from_date, to_date), yollanma_id__isnull=False,
                            tolangan_sana__isnull=True) | queryset.filter(
                tolangan_sana__range=(from_date, to_date), yollanma_id__isnull=False)
        elif yollanma and by_date:
            queryset = queryset.filter(sana=by_date, yollanma_id__isnull=False,
                                       tolangan_sana__isnull=True) | queryset.filter(
                tolangan_sana=by_date, yollanma_id__isnull=False)
        elif yollanma and qaytarildi:
            queryset = queryset.filter(tolov_qaytarildi=True, yollanma_id__isnull=False)
        elif joylashtirish and qaytarildi:
            queryset = queryset.filter(tolov_qaytarildi=True, joylashtirish_id__isnull=False)
        if tolandi is not None:
            if tolandi == 'false':
                queryset = queryset.filter(tolandi=False)
            else:
                queryset = queryset.filter(tolandi=True)
            if joylashtirish:
                queryset = queryset.filter(joylashtirish_id__isnull=False)
            elif yollanma:
                queryset = queryset.filter(yollanma_id__isnull=False)
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        umumiy_tolanganlar = 0
        qarzdorlik = 0
        for tolov in queryset:
            t = 0
            for i in tolov.tolangan_summa:
                if i.get('summa') is not None:
                    t += i.get('summa')
            if t <= tolov.summa:
                qarzdorlik = qarzdorlik + tolov.summa - t
            umumiy_tolanganlar += t
        serializer = TolovAdminSerializer(paginated_queryset, many=True)
        import math
        total_pages = math.ceil(len(queryset) / 30)
        return Response({'natija_tolovlar': serializer.data,
                         'umumiy_summa': umumiy_tolanganlar,
                         "qarzdorlik": qarzdorlik,
                         "sahifalar_soni": total_pages}, status=status.HTTP_200_OK)

class TolovDeleteAPIView(APIView):
    serializer_class = TolovAdminSerializer
    def delete(self, request, pk):
        Tolov.objects.filter(id=pk).delete()
        return Response({"succes": "true", "message":"To'lov o'chirildi"}, status=status.HTTP_200_OK)

class UserAPIView(APIView):
    serializer_class = UserReadSerializer
    def get(self, request):
        users = User.objects.all()
        serializer = UserReadSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserPostView(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                username = serializer.validated_data.get("username"),
                password = serializer.validated_data.get("password"),
                first_name = serializer.validated_data.get("first_name"),
                last_name = serializer.validated_data.get("last_name"),
                email = serializer.validated_data.get("role"),
                is_staff = True,
                is_active = True
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPutAPIView(APIView):
    serializer_class = UserSerializer
    def put(self, request, pk):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(username=serializer.validated_data.get("username"))
            if len(user) == 0:
                return Response({"success": "False", "xabar": "User topilmadi"})
            user[0].set_password(serializer.validated_data.get("password"))
            user[0].role = serializer.validated_data.get('role')
            user[0].first_name = serializer.validated_data.get('first_name')
            user[0].last_name = serializer.validated_data.get('last_name')
            user[0].save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HammaXonalarView(APIView):
    serializer_class = XonaSerializer
    def get(self, request):
        xonalar = Xona.objects.all()
        serializer = XonaJoylashuvlariSerializer(xonalar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


