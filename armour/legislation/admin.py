from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from tabbed_admin import TabbedModelAdmin

from .forms import LegislationTopicForm, KeyPointForm, QuestionForm, VATRateForm, DocumentForm, \
    GuidanceForm
from .models import Requirements, LocationCurrencyPrice, TopicCurrencyPrice, \
    Location, Topic, Currency, PriceSettings, DiscountCodes, Question, KeyPoint, LegislationTopicOption, \
    LegislationTopic, LegislationTopicComply, SourceNC, Document, Category, Guidance, VATRate


class LocationCurrencyPriceAdmin(NestedStackedInline, admin.StackedInline):
    model = LocationCurrencyPrice
    extra = 0


class TopicCurrencyPriceAdmin(NestedStackedInline, admin.StackedInline):
    model = TopicCurrencyPrice
    extra = 0


@admin.register(Location)
class LocationAdmin(TabbedModelAdmin, NestedModelAdmin):
    list_display = ('name', 'ord', 'published', 'vat')
    search_fields = ['name', ]

    tab_general = (
        (None, {
            'fields': ((), ('name', 'ord', 'published', 'vat')
                       )
        }),
    )

    tab_currency = (LocationCurrencyPriceAdmin,)
    tabs = [
        ('General', tab_general),
        ('Prices', tab_currency),
    ]


@admin.register(Topic)
class TopicAdmin(TabbedModelAdmin, NestedModelAdmin):
    list_display = ('name', 'ord', 'published',)
    search_fields = ['name', ]

    tab_general = (
        (None, {
            'fields': ((), ('name', 'ord', 'published',)
                       )
        }),
    )

    tab_currency = (TopicCurrencyPriceAdmin,)
    tabs = [
        ('General', tab_general),
        ('Prices', tab_currency),
    ]


class CurrencyAdmin(admin.TabularInline):
    model = Currency
    extra = 1


class DiscountCodesAdmin(admin.TabularInline):
    model = DiscountCodes
    extra = 1
    fields = ()
    readonly_fields = ('used',)


class VATAdmin(admin.TabularInline):
    model = VATRate
    extra = 1
    fields = ()
    form = VATRateForm


@admin.register(PriceSettings)
class PriceSettingsAdmin(TabbedModelAdmin, NestedModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(PriceSettingsAdmin, self).get_actions(request)
        # del actions['delete_selected']
        return actions

    list_display = ('site',)

    tab_general = (
        (None, {
            'fields': ((), ('disc_choice', 'disc_topic', 'disc_location',),
                       ('disc_next_choice', 'disc_next_topic', 'disc_next_location',)
                       )
        }),
    )

    tab_currency = (CurrencyAdmin,)
    tab_discount = (DiscountCodesAdmin,)
    tab_vat = (VATAdmin,)

    tabs = [
        ('Price Metrics', tab_general),
        ('Currency', tab_currency),
        ('Discount Codes', tab_discount),
        ('VAT Taxes', tab_vat),
    ]


class TopicOptions(NestedStackedInline, admin.StackedInline):
    model = LegislationTopicOption
    extra = 1


class ComplyOptions(NestedStackedInline, admin.StackedInline):
    model = LegislationTopicComply
    extra = 1
    readonly_fields = ['created', ]
    # inlines = [TopicOptions]


class KeP(NestedStackedInline, admin.StackedInline):
    model = KeyPoint
    extra = 1
    inlines = [ComplyOptions]
    exclude = ('req',)
    form = KeyPointForm


class QuestionOptions(NestedStackedInline, admin.StackedInline):
    model = Question
    extra = 1
    form = QuestionForm


@admin.register(LegislationTopic)
class LegislationTopicAdmin(TabbedModelAdmin, NestedModelAdmin):
    form = LegislationTopicForm
    list_display = ('title', 'location', 'topic', 'category', 'published', 'free')
    list_filter = ('version', 'location', 'topic', 'category',)
    inlines = [
        KeP
    ]
    tab_question = (
        (None, {
            'fields': (
            'title', 'description', 'location', 'topic', 'category', 'published', 'free', 'order', 'orderfull',
            'version'),
        }),
    )
    tab_kp = (KeP,)
    tab_quest = (QuestionOptions,)

    tabs = [
        ('General', tab_question),
        ('Specific questions', tab_quest),
        ('Key Points', tab_kp),
    ]

    def copy(modeladmin, request, queryset):
        print(queryset)

        for l in queryset:
            obj = LegislationTopic.objects.get(id=l.id)
            obj.pk = None
            obj.title = "[COPY] " + l.title
            obj.save()

            for q in l.legquestions.all():
                objq = Question.objects.get(id=q.id)
                objq.pk = None
                objq.legtopic = obj
                objq.save()

            for q in l.kpoints.all():
                objq = KeyPoint.objects.get(id=q.id)
                objq.pk = None
                objq.legtopic = obj
                objq.save()

                for c in q.topcomply.all():
                    objc = LegislationTopicComply.objects.get(id=c.id)
                    objc.pk = None
                    objc.point = objq
                    objc.save()

    copy.short_description = "Copy"
    actions = [copy]


# @admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'published',)
    search_fields = ['name', ]


class KePReq(NestedStackedInline, admin.StackedInline):
    model = KeyPoint
    extra = 1
    inlines = [ComplyOptions]
    exclude = ('legtopic',)
    form = KeyPointForm


@admin.register(Requirements)
class RequirementsAdmin(TabbedModelAdmin, NestedModelAdmin):
    list_display = ('name', 'published',)
    search_fields = ['name', ]

    inlines = [
        KePReq
    ]
    tab_req = (
        (None, {
            'fields': ('name', 'description', 'published',),
        }),
    )
    tab_kp = (KePReq,)

    tabs = [
        ('Genaral', tab_req),
        ('Key Points', tab_kp),
    ]


@admin.register(SourceNC)
class SourceNCAdmin(admin.ModelAdmin):
    list_display = ('name', 'default', 'defaulto')
    search_fields = ['name', ]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'free')
    search_fields = ['title', ]
    form = DocumentForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'published')
    search_fields = ['name', ]


@admin.register(Guidance)
class GuidanceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title', ]
    form = GuidanceForm
