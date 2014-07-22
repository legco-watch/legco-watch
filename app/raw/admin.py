from django.contrib import admin
from raw.models import ScrapeJob, RawCouncilAgenda, RawMember, RawScheduleMember, RawCommittee, RawCommitteeMembership


admin.site.register(ScrapeJob)
admin.site.register(RawCouncilAgenda)
admin.site.register(RawMember)
admin.site.register(RawScheduleMember)
admin.site.register(RawCommittee)
admin.site.register(RawCommitteeMembership)