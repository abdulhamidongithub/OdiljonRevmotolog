from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import *

@admin.register(Bemor)
class BemorAdmin(admin.ModelAdmin):
    list_display = ["ism", "familiya", "sharif", "royhatdan_otgan_sana"]
    search_fields = ["ism", "familiya", "sharif", "royhatdan_otgan_sana"]
    list_filter = ["royhatdan_otgan_sana", "joylashgan"]
    date_hierarchy = "royhatdan_otgan_sana"

@admin.register(Tolov)
class TolovAdmin(admin.ModelAdmin):
    list_display = ["bemor_id", "tolangan_summa", "tolangan_sana"]
    search_fields = ["tolangan_sana", "bemor_id", "yollanma_id"]
    list_filter = ["yollanma_id", "tolandi", "tolangan_sana"]
    date_hierarchy = "tolangan_sana"

admin.site.register(Yollanma)

admin.site.unregister(User)
admin.site.unregister(Group)
