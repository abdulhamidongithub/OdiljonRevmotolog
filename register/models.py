from django.db import models

class Bemor(models.Model):
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    sharif = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    pasport_seriya = models.CharField(max_length=10, blank=True, null=True)
    manzil = models.CharField(max_length=150)
    balans = models.IntegerField(default=0)
    royhatdan_otgan_sana = models.DateField(auto_now_add=True, null=True, blank=True)
    joylashgan = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ism} {self.familiya}"

class Xona(models.Model):
    qavat = models.PositiveSmallIntegerField()
    raqami = models.PositiveSmallIntegerField()
    xona_sigimi = models.PositiveSmallIntegerField()
    bosh_joy_soni = models.PositiveSmallIntegerField()
    turi = models.CharField(max_length=20, choices=(('Lux', 'Lux'), ('Odatiy', 'Odatiy'), ('Pol-lux', 'Pol-lux')))
    joy_narxi = models.IntegerField()
    def __str__(self):
        return f'{self.qavat} - qavat. {self.raqami} - xona'

class Yollanma(models.Model):
    nom = models.CharField(max_length=300)
    narx = models.IntegerField()
    qayerga = models.CharField(max_length=50)  # Labaratoriya, UZI, EKG, Doktor
    def __str__(self):
        return self.nom

class Joylashtirish(models.Model):
    bemor_id = models.ForeignKey(Bemor, on_delete=models.CASCADE)
    xona_id = models.ForeignKey(Xona, on_delete=models.CASCADE)
    kelish_sanasi = models.DateField()
    ketish_sanasi = models.DateField(null=True, blank=True)  # ketgandan so'ng tahrirlanadi
    qarovchi = models.BooleanField(default=False)
    yotgan_kun_soni = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    def __str__(self):
        return f'{self.bemor_id.ism}. {self.xona_id.qavat}, {self.xona_id.raqami}'

class Tolov(models.Model):
    bemor_id = models.ForeignKey(Bemor, on_delete=models.SET_NULL, null=True)
    summa = models.PositiveBigIntegerField()
    sana = models.DateField(auto_now_add=True)
    turi = models.CharField(choices=(('Naqd', 'Naqd'), ('Plastik', 'Plastik')), blank=True, max_length=50)
    tolandi = models.BooleanField(default=False)  # to'landi, qarzdor
    yollanma_id = models.ForeignKey(Yollanma, on_delete=models.CASCADE, null=True)  # 3
    joylashtirish_id = models.ForeignKey(Joylashtirish, on_delete=models.CASCADE, null=True, blank=True) # 2
    xulosa_holati = models.CharField(max_length=30, blank=True, null=True, choices=(
        ('Topshirilyapti', 'Topshirilyapti'),
        ('Kutyapti', 'Kutyapti'),
        ('Kiritildi', 'Kiritildi'),
    ), default="Topshirilyapti")
    ozgartirilgan_sana = models.DateField(null=True, blank=True, auto_now=True)
    # kun_soni = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.bemor_id.ism}, {self.summa}"


class Xulosa(models.Model):
    xulosa_matni = models.TextField()
    sana = models.DateField(auto_now_add=True)
    tolov_id = models.ForeignKey(Tolov, on_delete=models.CASCADE)    # 3
    chop_etildi = models.BooleanField(default=False)
    # kim_tomonidan = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.tolov_id.bemor_id.ism}, {self.xulosa_matni[:50]}"


class XulosaShablon(models.Model):
    xulosa_name = models.TextField()
    text_xulosa = models.TextField()
    def __str__(self):
        return self.xulosa_name



