from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User, Group

from .models import *

# @admin.register(Bemor)
# class BemorAdmin(admin.ModelAdmin):
#     list_display = ["ism", "familiya", "sharif", "royhatdan_otgan_sana"]
#     search_fields = ["ism", "familiya", "sharif", "royhatdan_otgan_sana"]
#     list_filter = ["joylashgan"]
#     date_hierarchy = "royhatdan_otgan_sana"
#
#     def has_add_permission(self, request):
#         # Disable adding new objects.
#         return False

# class QayergaListFilter(SimpleListFilter):
#
#     title = "Qayerga"
#     parameter_name = "yollanma_id__qayerga"
#
#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples that define the filter options.
#         """
#         return [
#             ("Labaratoriya", "Labaratoriya"),
#             ("UZI", "UZI"),
#             ("Doktor", "Doktor"),
#             ("Joylashtirish", "Joylashtirish"),
#         ]
#
#
#     def queryset(self, request, queryset):
#         """
#         Returns a filtered queryset based on the selected filter option.
#         """
#         if self.value == "Labaratoriya":
#             return queryset.filter(yollanma_id__qayerga="Labaratoriya")
#         elif self.value == "UZI":
#             return queryset.filter(yollanma_id__qayerga="UZI")
#         elif self.value == "Doktor":
#             return queryset.filter(yollanma_id__qayerga="Doktor")
#         elif self.value == "Joylashtirish":
#             return queryset.filter(joylashtirish_id__isnull=False)
#         else:
#             return queryset

# @admin.register(Tolov)
# class TolovAdmin(admin.ModelAdmin):
#     # list_display = ["bemor_id", "tolangan_summa", "tolangan_sana"]
#     search_fields = ["tolangan_sana", "bemor_id", "yollanma_id"]
#     date_hierarchy = "tolangan_sana"
#     list_filter = ["yollanma_id__qayerga", "tolandi"]
#
#     def has_add_permission(self, request):
#         # Disable adding new objects.
#         return False

admin.site.register(Bemor)
admin.site.register(Tolov)
admin.site.register(Joylashtirish)
admin.site.register(Xulosa)
admin.site.register(XulosaShablon)
admin.site.register(Yollanma)
admin.site.register(Xona)
admin.site.register(Chek)

# admin.site.unregister(User)
# admin.site.unregister(Group)
