from django.db import models


class Bemor(models.Model):
    ism = models.CharField(max_length=50)
    fam = models.CharField(max_length=50)
    tel = models.CharField(max_length=13)
    pasport_seriya = models.CharField(max_length=9)
    manzil = models.CharField(max_length=150)
    navbat = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.ism + ' ' + self.fam


class Tolov(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.SET_NULL, null=True)
    summa = models.PositiveBigIntegerField()
    sana = models.DateTimeField(auto_now=True)
    turi = models.CharField(choices=(('Naqd', 'Naqd'), ('Plastic', 'Plastic')), blank=True, max_length=50)
    tolandi = models.BooleanField()  # to'landi, qarzdor
    maqsadi = models.CharField(max_length=100)  # UZI, LOR, Revmatolog, Yotoq, Ko'rik ..., Qarovchi uchun to'lov
    izoh = models.TextField(null=True, blank=True)

    # agar yotoq uchun bo'lsa:
    kun_soni = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.bemor) + " " + str(self.summa) + " " + self.maqsadi


class Xulosa(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE)
    tur = models.CharField(max_length=50)  # UZI, LOR, Ko'rik ...
    xulosa = models.TextField()
    sana = models.DateTimeField()
    kim_tomonidan = models.CharField(max_length=100)

    def __str__(self):
        return str(self.bemor) + " - " + self.kim_tomonidan


class Xona(models.Model):
    qavat = models.PositiveSmallIntegerField(default=1)
    raqami = models.PositiveSmallIntegerField()
    joylar_soni = models.PositiveSmallIntegerField()
    turi = models.CharField(max_length=20, choices=(('Lux', 'Lux'), ('Odatiy', 'Odatiy')))

    # qo'shimcha
    # kunlik_tolov = models.BigIntegerField(default=1500000)

    def __str__(self):
        return f'{self.qavat} - qavat. {self.raqami} - xona'


class Joylashtirish(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE)
    xona = models.ForeignKey(Xona, on_delete=models.CASCADE)
    kelish_sanasi = models.DateField()
    ketish_sanasi = models.DateField(null=True, blank=True)  # ketgandan so'ng tahrirlanadi
    qarovchi = models.BooleanField()

    def __str__(self):
        return f'{self.bemor}. {self.xona}'
