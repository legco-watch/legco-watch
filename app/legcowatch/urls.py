from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView
import raw.views
import common.views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', common.views.LandingView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^raw/agendas/?$', raw.views.RawCouncilAgendaListView.as_view(), name='raw_agenda_list'),
    url(r'^raw/agendas/(?P<pk>[0-9]+)/?$', raw.views.RawCouncilAgendaDetailView.as_view(), name='raw_agenda'),
    url(r'^raw/agendas/(?P<slug>[a-zA-Z0-9\-_]+)/?$', raw.views.RawCouncilAgendaDetailView.as_view(), name='raw_agenda_uid'),
    url(r'^raw/agendas/(?P<pk>[0-9]+)/source/?$', raw.views.RawCouncilAgendaSourceView.as_view(), name='raw_agenda_source'),
    url(r'^raw/agendas/(?P<slug>[a-zA-Z0-9\-_]+)/source/?$', raw.views.RawCouncilAgendaSourceView.as_view(), name='raw_agenda_source_uid'),
    url(r'^raw/members/?$', raw.views.RawMemberListView.as_view(), name='raw_member_list'),
    url(r'^raw/members/(?P<pk>[0-9]+)/?$', raw.views.RawMemberDetailView.as_view(), name='raw_member'),
    url(r'^raw/committees/?$', raw.views.RawCommitteeListView.as_view(), name='raw_committee_list'),
    url(r'^raw/committees/(?P<pk>[0-9]+)/?$', raw.views.RawCommitteeDetailView.as_view(), name='raw_committee'),
    url(r'^error_report/?$', common.views.ErrorReportFormView.as_view(), name='error_report'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
