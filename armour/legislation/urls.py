from django.conf.urls import url

from .views import SpecificQuestions, SetSpecQuestionView, LegislationTopicsView, LegislationTopicsContentView, \
    SetLegistaltionTopicView, LegislationNonConformanceView, SetNonConformanceView, FinishView, LegislationListView, \
    StartNewView, LegislationDocView, LegislationReportView, OuterNonConformanceView, SetOuterNonConformanceView, \
    LegislationDeleteView, LegislationNCReportView, PlanSpecQuestionConfirmationView, SpecQuestionConfirmationView, \
    GuidanceListView, LegUpdateView, LegislationNCOuterReportView, SetDiscountView

urlpatterns = [
    url(r'^my/list/$', LegislationListView.as_view(), {}, 'leg-list'),
    url(r'^specific-questions/$', SpecificQuestions.as_view(), {}, 'spec-questions'),
    url(r'^specific-questions/set/$', SetSpecQuestionView.as_view(), {}, 'spec-question-set'),
    url(r'^legislation-topics/$', LegislationTopicsView.as_view(), {}, 'legislation-topics'),
    url(r'^legislation-topics/content/$', LegislationTopicsContentView.as_view(), {}, 'legislation-topics-content'),
    url(r'^legislation-topics/set/$', SetLegistaltionTopicView.as_view(), {}, 'legislation-topics-set'),
    url(r'^non-conformance/$', LegislationNonConformanceView.as_view(), {}, 'non-conformance'),
    url(r'^non-conformance/set/(?P<pk>\d+)/$', SetNonConformanceView.as_view(), {}, 'non-conformance-set'),
    url(r'^finish/$', FinishView.as_view(), {}, 'finish'),
    url(r'^start/$', StartNewView.as_view(), {}, 'start-legislation'),
    url(r'^document/download/(?P<pk>[0-9A-Fa-f-]+)/$', LegislationDocView.as_view(), {}, 'get-leg-doc'),
    url(r'^document/report/pdf/(?P<pk>[0-9A-Fa-f-]+)/$', LegislationReportView.as_view(), {}, 'get-report-pdf'),
    url(r'^non-conformance/compact/$', OuterNonConformanceView.as_view(), {}, 'additional-non-conformance'),
    url(r'^non-conformance/compact/set/(?P<pk>\d+)/$', SetOuterNonConformanceView.as_view(), {},
        'additional-non-conformance-set'),
    url(r'^legislation/delete/(?P<pk>\d+)/$', LegislationDeleteView.as_view(), {}, 'legislation-delete'),
    url(r'^document/report/nc/pdf/(?P<pk>[0-9A-Fa-f-]+)/(?P<mode>[\w\-]+)/$', LegislationNCReportView.as_view(), {},
        'get-report-nc-pdf'),
    url(r'^document/report/outer/nc/pdf/$', LegislationNCOuterReportView.as_view(), {},
        'get-report-nc-outer-pdf'),
    url(r'^specific-questions/confirmation/$', SpecQuestionConfirmationView.as_view(), {},
        'spec-questions-confirmation'),
    url(r'^select/your/plan/$', PlanSpecQuestionConfirmationView.as_view(), {}, 'select-your-plan'),
    url(r'^guidance/list/$', GuidanceListView.as_view(), {}, 'guidance-list'),
    url(r'^version/update/$', LegUpdateView.as_view(), {}, 'legislation-version-update'),
    url(r'^discount/set/$', SetDiscountView.as_view(), {}, 'discount-set'),
]
