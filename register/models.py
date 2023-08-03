from django.db import models

class Bemor(models.Model):
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    sharif = models.CharField(max_length=100)
    tugilgan_sana = models.DateField(null=True, blank=True)
    tel = models.CharField(max_length=15)
    pasport_seriya = models.CharField(max_length=10, blank=True, null=True)
    manzil = models.CharField(max_length=150)
    balans = models.IntegerField(default=0)
    royhatdan_otgan_sana = models.DateField(auto_now_add=True, null=True, blank=True)
    joylashgan = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ism} {self.familiya}"

    class Meta:
        ordering = ['familiya', 'ism']

class Xona(models.Model):
    qavat = models.PositiveSmallIntegerField()
    raqami = models.PositiveSmallIntegerField()
    xona_sigimi = models.PositiveSmallIntegerField()
    bosh_joy_soni = models.PositiveSmallIntegerField()
    turi = models.CharField(max_length=20, choices=(('Lux', 'Lux'), ('Odatiy', 'Odatiy'), ('Pol-lux', 'Pol-lux')))
    joy_narxi = models.IntegerField()
    def __str__(self):
        return f'{self.qavat} - qavat. {self.raqami} - xona'


class XulosaShablon(models.Model):
    xulosa_name = models.TextField()
    header_text = models.TextField(null=True, blank=True)
    footer_text = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.xulosa_name

class Yollanma(models.Model):
    nom = models.CharField(max_length=300)
    narx = models.IntegerField()
    qayerga = models.CharField(max_length=50)  # Labaratoriya, UZI, EKG, Doktor
    xulosa_shablon_id = models.ForeignKey(XulosaShablon, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.nom}."


    def save(self, *args, **kwargs):
        if not self.xulosa_shablon_id:
            new_one = XulosaShablon.objects.create(
                xulosa_name = self.nom
            )
            self.xulosa_shablon_id = new_one
        super(Yollanma, self).save(*args, **kwargs)
        self.xulosa_shablon_id.xulosa_name = self.nom
        self.xulosa_shablon_id.save()

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
    tolangan_summa = models.JSONField(null=True, blank=True, default=[])
    sana = models.DateField(auto_now_add=True)
    turi = models.CharField(choices=(('Naqd', 'Naqd'), ('Plastik', 'Plastik')), blank=True, max_length=50)
    tolandi = models.BooleanField(default=False)  # to'landi, qarzdor
    yollanma_id = models.ForeignKey(Yollanma, on_delete=models.CASCADE, null=True, blank=True)  # 3
    joylashtirish_id = models.ForeignKey(Joylashtirish, on_delete=models.CASCADE, null=True, blank=True) # 2
    xulosa_holati = models.CharField(max_length=30, blank=True, null=True, choices=(
        ('Topshirilyapti', 'Topshirilyapti'),
        ('Kutyapti', 'Kutyapti'),
        ('Kiritildi', 'Kiritildi'),
    ))
    tolangan_sana = models.DateField(null=True, blank=True)
    ozgartirilgan_sana = models.DateField(null=True, blank=True)
    haqdor = models.BooleanField(default=False)

    def __str__(self):
        umumiy = 0
        for i in self.tolangan_summa:
            if i.get('summa'):
                umumiy += int(i.get('summa'))
        if self.bemor_id:
            return f"{self.bemor_id.ism}, {umumiy} so'm"
        return f"{umumiy} so'm"


class Xulosa(models.Model):
    xulosa_matni = models.TextField()
    sana = models.DateField(auto_now_add=True)
    tolov_id = models.ForeignKey(Tolov, on_delete=models.CASCADE)
    chop_etildi = models.BooleanField(default=False)

    def __str__(self):
        if self.tolov_id.bemor_id:
            return f"{self.tolov_id.bemor_id.ism}, {self.xulosa_matni[:50]}"
        return f"{self.xulosa_matni[:50]}"

class TolovQaytarish(models.Model):
    summa = models.IntegerField()
    sana = models.DateField(auto_now_add=True)
    izoh = models.CharField(max_length=300)
    tolov_id = models.ForeignKey(Tolov, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.izoh

class Chek(models.Model):
    bemor_id = models.ForeignKey(Bemor, on_delete=models.SET_NULL, null=True)
    sana = models.DateField()
    tolov_maqsadlar = models.JSONField(default=list())
    def __str__(self):
        if self.bemor_id:
            return f"{self.bemor_id.ism} ({self.sana})"
        return f"{self.sana}"


