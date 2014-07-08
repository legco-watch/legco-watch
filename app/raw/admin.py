from django.contrib import admin
from raw.models import ScrapeJob, RawCouncilAgenda, RawMember


admin.site.register(ScrapeJob)
admin.site.register(RawCouncilAgenda)
admin.site.register(RawMember)