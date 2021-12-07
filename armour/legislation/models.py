import os
import re
import uuid
from datetime import timedelta

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.query_utils import Q
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices


class Location(models.Model):
    name = models.CharField(_('Name'), max_length=120)
    published = models.BooleanField(_('Published'), default=True)
    vat = models.ForeignKey("VATRate", null=True, on_delete=models.CASCADE, blank=True, )
    ord = models.IntegerField(_('Order'), default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Location')
        verbose_name_plural = _(u'Locations')
        ordering = ['ord']


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=120)
    published = models.BooleanField(_('Published'), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Sector')
        verbose_name_plural = _(u'Sectors')


class Topic(models.Model):
    name = models.CharField(_('Name'), max_length=120)
    published = models.BooleanField(_('Published'), default=True)
    ord = models.IntegerField(_('Order'), default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Topic')
        verbose_name_plural = _(u'Topics')
        ordering = ['ord']


class PriceSettings(models.Model):
    site = models.OneToOneField(Site, related_name="site_settings", on_delete=models.CASCADE)
    disc_choice = models.BooleanField(_('Discont on two or more choices'), default=False)
    disc_topic = models.PositiveIntegerField("Discount Topic", null=False, default=0,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    disc_location = models.PositiveIntegerField("Discount Location", null=False, default=0,
                                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    disc_next_choice = models.BooleanField(_('Discont on every next choice'), default=False)
    disc_next_topic = models.PositiveIntegerField("Discount Next Topic", null=False, default=0,
                                                  validators=[MinValueValidator(0), MaxValueValidator(100)])
    disc_next_location = models.PositiveIntegerField("Discount Next Location", null=False, default=0,
                                                     validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.site.name

    class Meta:
        verbose_name = _(u'Price Settings')
        verbose_name_plural = _(u'Price Settings')


class VATRate(models.Model):
    settings = models.ForeignKey(PriceSettings, on_delete=models.CASCADE, related_name="vat")
    name = models.CharField(_('Name'), max_length=400, unique=True)
    value = models.PositiveIntegerField(_('Value'), validators=[MinValueValidator(1), MaxValueValidator(99), ])
    stripeId = models.CharField(_('Stripe'), max_length=400, null=True, blank=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'VAT Rate')
        verbose_name_plural = _(u'VAT Rates')
        ordering = ['name']


class Currency(models.Model):
    name = models.CharField(_('Code'), max_length=4, primary_key=True)
    settings = models.ForeignKey(PriceSettings, null=True, on_delete=models.CASCADE, blank=False,
                                 related_name="currency")
    main = models.BooleanField(_('Default'), default=False, )
    published = models.BooleanField(_('Published'), default=True),

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Currency')
        verbose_name_plural = _(u'Currencys')


class DiscountCodes(models.Model):
    name = models.CharField(_('Description'), max_length=250, )
    settings = models.ForeignKey(PriceSettings, null=True, on_delete=models.CASCADE, blank=False, related_name="dcodes")
    size = models.PositiveIntegerField("Size [%]", null=False, default=1,
                                       validators=[MinValueValidator(1), MaxValueValidator(100)])
    code = models.CharField(_('Code'), max_length=10, unique=True)

    multiple = models.BooleanField(_('Multiple-use'), default=False)
    used = models.BooleanField(_('Used'), default=False, editable=False)
    active = models.BooleanField(_('Active'), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Discount Code')
        verbose_name_plural = _(u'Discount Codes')


class LegislationTopic(models.Model):
    title = models.CharField(_('Title'), max_length=300)
    description = RichTextField(_('Full description'), max_length=60000, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="leglocations")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="legtopics")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    published = models.BooleanField(_('Published'), default=True)
    version = models.PositiveIntegerField(_('Version'), default=1)

    changed = models.BooleanField(_('Changed'), default=False, editable=False)

    free = models.BooleanField(_('Show for free'), default=False, )
    order = models.PositiveIntegerField(_('Order for free'), default=1)
    orderfull = models.PositiveIntegerField(_('Order for full'), default=1)

    def get_keyp(self):
        return self.kpoints.filter(published=True).distinct().order_by('id')

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         old = LegislationTopic.objects.get(id=self.pk)  # fetch current data from db to examine version
    #         if old.version < self.version:  # changing version
    #
    #             for question in self.legquestions.all():
    #                 copy = Question.objects.get(id=question.id)
    #                 copy.pk = None
    #                 copy.legtopic = self
    #                 copy.parent = question
    #                 copy.changed = False
    #                 copy.save()
    #
    #             for point in self.kpoints.all():
    #                 copy = KeyPoint.objects.get(id=point.id)
    #                 copy.pk = None
    #                 copy.legtopic = self
    #                 copy.parent = point
    #                 copy.changed = False
    #                 copy.save()
    #
    #                 for comply in point.topcomply.all():
    #                     comply_copy = LegislationTopicComply.objects.get(id=comply.id)
    #                     comply_copy.pk = None
    #                     comply_copy.point = copy
    #                     comply_copy.save()
    #
    #     super(LegislationTopic, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'Legislation topic')
        verbose_name_plural = _(u'Legislation topics')
        ordering = ['title']


class Question(models.Model):
    title = models.TextField(_('Title'), max_length=2000)
    published = models.BooleanField(_('Published'), default=True)
    legtopic = models.ForeignKey(LegislationTopic, on_delete=models.CASCADE, related_name="legquestions", null=True, )
    changed = models.BooleanField(_('Changed'), default=False, editable=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="questionchilds", null=True, blank=True,
                               editable=False)
    desc = models.TextField(_('Description'), max_length=6000, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Question')
        verbose_name_plural = _(u'Questions')


class Requirements(models.Model):
    name = models.CharField(_('Name'), max_length=600)
    description = RichTextField(_('Full description'), max_length=60000, null=True)
    nodescription = models.TextField(_('Non Conformance description'), max_length=2000, null=True, blank=True)
    published = models.BooleanField(_('Published'), default=True)

    def __str__(self):
        return self.name

    def points_active(self):
        return self.reqpoints.filter(published=True).distinct().order_by('id')

    class Meta:
        verbose_name = _(u'Standard or Other Requirement')
        verbose_name_plural = _(u'Standard or Other Requirements')


class KeyPoint(models.Model):
    point = RichTextField(_('Key Point'), max_length=60000, )
    published = models.BooleanField(_('Published'), default=True)
    legtopic = models.ForeignKey(LegislationTopic, on_delete=models.CASCADE, related_name="kpoints", null=True, )
    req = models.ForeignKey(Requirements, on_delete=models.CASCADE, related_name="reqpoints", null=True, )
    changed = models.BooleanField(_('Changed'), default=False, editable=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="kpchilds", null=True, blank=True,
                               editable=False)

    def __str__(self):
        try:
            return re.compile('<strong>(.*?)</strong>', re.DOTALL | re.IGNORECASE).findall(self.point)[0]
        except:
            return strip_tags(self.point)

    class Meta:
        verbose_name = _(u'Key Point')
        verbose_name_plural = _(u'Key Points')
        ordering = ['id']


class LegislationTopicComply(models.Model):
    title = RichTextField(_('Title'), max_length=60000, )
    point = models.ForeignKey(KeyPoint, on_delete=models.CASCADE, related_name="topcomply", null=True, )
    created = models.DateTimeField(null=False, blank=False, auto_now_add=True, editable=False, )

    def __str__(self):
        return strip_tags(self.title)[:100]

    class Meta:
        verbose_name = _(u'Comply option')
        verbose_name_plural = _(u'Comply option')
        ordering = ['created']


class LegislationTopicOption(models.Model):
    option = models.CharField(_('Option'), max_length=600)
    comply = models.ForeignKey(LegislationTopicComply, on_delete=models.CASCADE, related_name="koptions", null=True, )

    def __str__(self):
        return self.option

    class Meta:
        verbose_name = _(u'Option')
        verbose_name_plural = _(u'Options')
        ordering = ['option']


class LocationCurrencyPrice(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False, related_name="locationprices")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=False, related_name="currencylocationprices")
    price = models.FloatField(_('Price'), validators=[MinValueValidator(1), ])

    def __str__(self):
        return str(self.price)

    class Meta:
        verbose_name = _(u'Location price')
        verbose_name_plural = _(u'Location prices')
        unique_together = ['location', 'currency']


class TopicCurrencyPrice(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False, related_name="topicprices")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=False, related_name="currencytopicprices")
    price = models.FloatField(_('Price'), validators=[MinValueValidator(1), ])

    def __str__(self):
        return str(self.price)

    class Meta:
        verbose_name = _(u'Topic price')
        verbose_name_plural = _(u'Topic prices')
        unique_together = ['topic', 'currency']


class Sector(models.Model):
    name = models.CharField(_('Name'), max_length=120)
    published = models.BooleanField(_('Published'), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Sector')
        verbose_name_plural = _(u'Sectors')


class Register(models.Model):
    system_check_deprecated_details = {
        'version': 'Removed for now'
    }
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, blank=False,
                                related_name="companylegislations")
    finished = models.BooleanField(_('Finished'), default=False)
    started = models.DateTimeField(_('Started'), null=False, blank=False, auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), null=False, blank=False, auto_now=True)
    finish_date = models.DateTimeField(_('Finish date'), null=True, blank=True, )
    name = models.CharField(_('Name'), max_length=300, null=True)
    uuid = models.UUIDField(editable=False, null=True, blank=True)

    def __str__(self):
        return self.started.strftime('%Y-%m-%d')

    def get_reviev_date(self):
        if not self.finish_date:
            return None
        else:
            return self.finish_date + timedelta(days=365)

    def get_legtopic_progress(self, location, topic):
        conf = self
        qargs = [Q(legquestions__isnull=False, legquestions__questionsresponses__response=True,
                   legquestions__questionsresponses__position__register=conf) | Q(legquestions__isnull=True)]
        qargs1 = [Q(category__in=self.company.category.all()) | Q(category__isnull=True)]

        prdcount = 0
        allcount = 0
        ltopics = []
        if self.company.free:
            src = LegislationTopic.objects.filter(*qargs, *qargs1, published=True, kpoints__isnull=False,
                                                  location__id=location, topic__id=topic, free=True).order_by(
                'order').distinct()[
                  :settings.FREE_LIMIT]
            val = src.values_list('id', flat=True)

            if len(val) > 0:
                prdcount += KeyPoint.objects.filter(legtopic__id__in=val, published=True).distinct().count()

            allcount += prdcount

        else:
            src = LegislationTopic.objects.filter(*qargs, *qargs1, published=True, kpoints__isnull=False,
                                                  location__id=location,
                                                  topic__id=topic).order_by('order').distinct()

            val = src.values_list('id', flat=True)
            if len(val) > 0:
                prdcount += KeyPoint.objects.filter(legtopic__id__in=val, published=True).distinct().count()

            val = LegislationTopic.objects.filter(*qargs, *qargs1, published=True, kpoints__isnull=False).values_list(
                'id', flat=True)
            if len(val) > 0:
                allcount += KeyPoint.objects.filter(legtopic__id__in=val, published=True).distinct().count()

        for l in src:
            ltopics.append(l)

        if self.company.free:
            if len(ltopics) < settings.FREE_LIMIT:
                rqcount = settings.FREE_LIMIT - len(ltopics)
                if rqcount > 0:
                    rq = self.company.req.filter(published=True, reqpoints__isnull=False).distinct()[:rqcount]
                    for l in rq:
                        prdcount += l.reqpoints.filter(published=True).distinct().count()
                        allcount += l.reqpoints.filter(published=True).distinct().count()

        else:
            rq = self.company.req.filter(published=True, reqpoints__isnull=False).distinct()
            for l in rq:
                prdcount += l.reqpoints.filter(published=True).distinct().count()
                allcount += l.reqpoints.filter(published=True).distinct().count()

        qanswers = [Q(topicresponse__isnull=False, topicresponse__position__location__id=location,
                      topicresponse__position__topic__id=location) | Q(
            topicresponse__req__isnull=False)]

        answers = LegislationTopicsKeyPointResponse.objects.filter(topicresponse__position__register=conf,
                                                                   *qanswers).distinct()
        prdprogress = 0
        if prdcount != 0:
            prdprogress = (answers.count() * 100) / prdcount

        answersall = LegislationTopicsKeyPointResponse.objects.filter(
            topicresponse__position__register=conf, ).distinct()

        allprogress = 0
        if allcount != 0:
            allprogress = (answersall.count() * 100) / allcount

        return {'prdprogress': round(prdprogress, 0), 'allprogress': round(allprogress, 0)}

    def get_or_create_uuid(self):
        uid = self.uuid and self.uuid or str(uuid.uuid4())
        if not self.uuid:
            self.uuid = uid
            self.save()

        return uid

    def get_ncs(self):
        return LegislationNonConformanceResponse.objects.filter(
            topicreply__position__register=self).distinct().order_by("started")

    def get_ncs_cnt(self):
        return self.get_ncs().count()

    def get_topics(self):
        ret = []
        for p in self.legislationpos.filter(topic__isnull=False):
            ret.append(p.topic.id)
        return Topic.objects.filter(id__in=ret).order_by("name")

    def get_locations(self):
        ret = []
        for p in self.legislationpos.filter(location__isnull=False):
            ret.append(p.location.id)

        return Location.objects.filter(id__in=ret).order_by("name")

    def get_leg_topics(self):
        return LegislationTopicsResponse.objects.filter(position__register=self).values('legtopic',
                                                                                           'req', ).order_by(
            "legtopic__title")

    def get_products(self):
        return self.legislationpos.filter(req__isnull=True).order_by("topic__name", "location__name")

    def get_other(self):
        return self.legislationpos.filter(req__isnull=False).order_by("req__name", )

    class Meta:
        verbose_name = _(u'Legal Register')
        verbose_name_plural = _(u'Legal Registers')
        ordering = ['-finished']


class LegislationPosition(models.Model):
    register = models.ForeignKey(Register, on_delete=models.CASCADE, blank=False, related_name="legislationpos")
    started = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, blank=False, auto_now=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True, related_name="topicpos")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True, related_name="locationpos")
    req = models.ForeignKey(Requirements, on_delete=models.CASCADE, blank=True, null=True, related_name="reqpos")
    topicpos = models.PositiveIntegerField(editable=False, default=1)

    def get_emptyp(self, ):
        posempty = []

        if self.topic:
            topics = self.get_topics()
            if self.register.company.free:
                topics = topics.filter(free=True)

            for t in topics:
                if self.postopicresponses.filter(legtopic=t).count() == 0:
                    posempty.append(t.id)

            if len(posempty) > 0:
                return LegislationTopic.objects.filter(id__in=posempty, published=True).distinct()

        elif self.req:
            for t in self.register.company.req.all():
                if self.postopicresponses.filter(req=t).count() == 0:
                    posempty.append(t.id)

            if len(posempty) > 0:
                return Requirements.objects.filter(id__in=posempty, published=True).distinct()

        return []

    def get_nonpositions(self, ):
        return self.postopicresponses.filter(status=LegislationTopicsResponse.State.non).distinct()

    def get_incpositions(self, ):
        return self.postopicresponses.filter(status=LegislationTopicsResponse.State.inc).distinct()

    def get_fullpositions(self, ):
        return self.postopicresponses.filter(status=LegislationTopicsResponse.State.full).distinct()

    def get_topics(self, ):
        return LegislationTopic.objects.filter(topic=self.topic, location=self.location).order_by("title")

    def __str__(self):
        return self.register.__str__()

    class Meta:
        verbose_name = _(u'Legislation position')
        verbose_name_plural = _(u'Legislation positions')


class LegislationSpecQuestion(models.Model):
    position = models.ForeignKey(LegislationPosition, on_delete=models.CASCADE, blank=False,
                                 related_name="specquerypos")
    started = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, blank=False, auto_now=True)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE, blank=False,
                                 related_name="questionsresponses")
    response = models.BooleanField(_('Yes/No'), default=False)

    def __str__(self):
        return self.question.title

    class Meta:
        verbose_name = _(u'Legislation specific question')
        verbose_name_plural = _(u'Legislation specific questions')


class LegislationTopicsResponse(models.Model):
    class Answers(DjangoChoices):
        yes = ChoiceItem(1, label=_('Full Compliance'))
        no = ChoiceItem(0, label=_('No Compliance'))
        partial = ChoiceItem(2, label=_('Partial Compliance'))

    class State(DjangoChoices):
        non = ChoiceItem(1, label=_('No Compliance'))
        inc = ChoiceItem(2, label=_('Incomplete'))
        full = ChoiceItem(3, label=_('Full Compliance'))

    position = models.ForeignKey(LegislationPosition, on_delete=models.CASCADE, blank=False, null=True,
                                 related_name="postopicresponses", )
    legtopic = models.ForeignKey(LegislationTopic, on_delete=models.CASCADE, related_name="ltopicreply", null=True,
                                 blank=True)
    started = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, blank=False, auto_now=True)
    requirements = models.ManyToManyField(LegislationTopicOption, blank=True)
    response = models.IntegerField(choices=Answers.choices, null=True, blank=True, )
    pos = models.IntegerField(editable=False, null=True, blank=True, )
    req = models.ForeignKey(Requirements, on_delete=models.CASCADE, blank=True, null=True, related_name="reqreply")
    note = models.TextField(null=True, blank=True, )
    ncnote = models.TextField(null=True, blank=True, )
    status = models.IntegerField(editable=False, default=0, choices=State.choices)

    def verify(self):
        ret = False
        rep = self.topicresponsekeyp.filter(response__in=[0, 1]).distinct().count()

        if self.legtopic:
            kp = self.legtopic.kpoints.filter(published=True).distinct().count()
            if kp == rep:
                ret = True

        elif self.req:
            kp = self.req.reqpoints.filter(published=True).distinct().count()
            if kp == rep:
                ret = True

        return ret

    def set_status_number(self):
        repyes = self.topicresponsekeyp.filter(response__in=[1]).distinct().count()
        repno = self.topicresponsekeyp.filter(response__in=[0]).distinct().count()
        repall = repyes + repno
        kp = 0
        if self.legtopic:
            kp = self.legtopic.kpoints.filter(published=True).distinct().count()
        elif self.req:
            kp = self.req.reqpoints.filter(published=True).distinct().count()

        if repyes >= kp:
            status = 3
        elif repall >= kp and repno > 0:
            status = 1
        else:
            status = 2

        return status

    class Meta:
        verbose_name = _(u'Legislation topic response')
        verbose_name_plural = _(u'Legislation topic responses')
        ordering = ["pos"]


class LegislationTopicsKeyPointResponse(models.Model):
    class Answers(DjangoChoices):
        yes = ChoiceItem(1, label=_('Full Compliance'))
        no = ChoiceItem(0, label=_('No Compliance'))

    topicresponse = models.ForeignKey(LegislationTopicsResponse, on_delete=models.CASCADE,
                                      related_name="topicresponsekeyp", )
    point = models.ForeignKey(KeyPoint, on_delete=models.CASCADE, related_name="kpointresponse", )
    started = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, blank=False, auto_now=True)
    note = models.TextField(null=True, blank=True, max_length=4000)
    response = models.IntegerField(choices=Answers.choices, null=True, blank=True, )
    ncnote = models.TextField(null=True, blank=True, )

    class Meta:
        verbose_name = _(u'Legislation key point response')
        verbose_name_plural = _(u'Legislation key point responses')
        unique_together = ('topicresponse', 'point',)


class SourceNC(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    default = models.BooleanField(_('For Legal register'), default=False)
    defaulto = models.BooleanField(_('For Outer NC'), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'NC Sources')
        verbose_name_plural = _(u'NC Sources')
        ordering = ['name']


class LegislationNonConformanceResponse(models.Model):
    nctype = "inner"

    class Priority(DjangoChoices):
        low = ChoiceItem("low", label=_('Low'))
        medium = ChoiceItem("medium", label=_('Medium'))
        high = ChoiceItem("high", label=_('High'))

    topicreply = models.ForeignKey(LegislationTopicsResponse, on_delete=models.CASCADE, related_name="topicnon", )
    source = models.ForeignKey(SourceNC, on_delete=models.CASCADE, null=True)
    started = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, blank=False, auto_now=True)
    identified = models.TextField("Identified by", max_length=2000, null=True)
    assigned = models.TextField("Assigned to", max_length=2000, null=True)
    containment = models.TextField("Containment actions", max_length=2000, null=True)
    completion = models.TextField("Completion date & by whom", max_length=2000, null=True)
    root = models.TextField("Root cause", max_length=2000, null=True)
    corrective = models.TextField("Actions to be taken", max_length=2000, null=True)
    cost = models.TextField("Cost of nonconformance", max_length=2000, null=True)
    reviewed = models.TextField("Reviewed and closed out by", max_length=2000, null=True)
    desc = models.TextField("Description", max_length=2000, null=True)
    ncdesc = models.TextField("NC description", max_length=2000, null=True)
    assign = models.ForeignKey("user.User", verbose_name="Assigned to", null=True, blank=True,
                               on_delete=models.SET_NULL)
    verified = models.BooleanField(_('Verified'), default=False, editable=False)
    point = models.ForeignKey(KeyPoint, on_delete=models.CASCADE, related_name="kpointncresponse", null=True,
                              blank=True)
    priority = models.CharField("Priority", choices=Priority.choices, default=Priority.low, max_length=15)
    identified_by = models.ForeignKey("user.User", verbose_name="Identified by", null=True, blank=True,
                                      on_delete=models.SET_NULL, related_name="ncidentified")
    completeddate = models.DateField("Completion date", null=True, blank=False, )
    completed_by = models.ForeignKey("user.User", verbose_name="Identified by", null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name="nccompleted")
    revieweddate = models.DateField("Review date", null=True, blank=False, )
    reviewed_by = models.ForeignKey("user.User", verbose_name="Identified by", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="ncreviewed")

    no = models.PositiveIntegerField(verbose_name="No", default=1, )

    def verify(self):
        if self.completeddate and self.completed_by:
            return True

        return False

    def save(self, *args, **kwargs):
        self.verified = self.verify()
        super(LegislationNonConformanceResponse, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'NC')
        verbose_name_plural = _(u'NC')
        ordering = ['started']


class Document(models.Model):
    title = models.CharField(_('Title'), max_length=300)
    file = models.FileField(_('File'), max_length=2000, upload_to='documents/%Y/%m/%d/')
    locations = models.ManyToManyField(Location, verbose_name="Location", blank=True, )
    topics = models.ManyToManyField(Topic, verbose_name="Topics", blank=True, )
    category = models.ManyToManyField(Category, verbose_name="Sector", blank=True)
    free = models.BooleanField(_('Show for free'), default=False, )
    published = models.BooleanField(_('Published'), default=False, )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _(u'Document')
        verbose_name_plural = _(u'Documents')
        ordering = ['title']


class LegislationDocument(models.Model):
    register = models.ForeignKey(Register, on_delete=models.CASCADE, blank=False, related_name="legdocs")
    started = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, blank=False, auto_now=True)
    title = models.CharField(_('Title'), max_length=300, null=True)
    file = models.FileField(_('File'), max_length=2000, upload_to='legislation/documents/%Y/%m/%d/')
    uuid = models.UUIDField(editable=False, null=True, blank=True)

    def __str__(self):
        return self.register.__str__()

    def get_extention(self):
        if not self.file:
            return None
        fileName, fileExtension = os.path.splitext(self.file.name)
        return fileExtension.upper().replace(".", "")

    def save(self, *args, **kwargs):
        super(LegislationDocument, self).save(*args, **kwargs)
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
            self.save()

    class Meta:
        verbose_name = _(u'Legislation position')
        verbose_name_plural = _(u'Legislation positions')


class NonConformanceOuterResponse(models.Model):
    nctype = "outer"

    class Priority(DjangoChoices):
        low = ChoiceItem("low", label=_('Low'))
        medium = ChoiceItem("medium", label=_('Medium'))
        high = ChoiceItem("high", label=_('High'))

    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name="companyouternc")
    initialrecord = models.BooleanField(default=False)
    source = models.ForeignKey(SourceNC, on_delete=models.CASCADE, null=True, related_name="outersources")
    started = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, blank=False, auto_now=True)
    identified = models.TextField("Identified by", max_length=2000, null=True)
    assigned = models.TextField("Assigned to", max_length=2000, null=True)
    containment = models.TextField("Containment actions", max_length=2000, null=True)
    completion = models.TextField("Completion date & by whom", max_length=2000, null=True)
    root = models.TextField("Root cause", max_length=2000, null=True)
    corrective = models.TextField("Corrective actions", max_length=2000, null=True)
    cost = models.TextField("Cost of nonconformance", max_length=2000, null=True)
    reviewed = models.TextField("Reviewed and closed out by", max_length=2000, null=True)
    description = models.TextField("Description", max_length=2000, null=True)
    assign = models.ForeignKey("user.User", verbose_name="Assigned to", null=True, blank=True,
                               on_delete=models.SET_NULL)
    verified = models.BooleanField(_('Verified'), default=False, editable=False)

    priority = models.CharField("Priority", choices=Priority.choices, default=Priority.low, max_length=15)
    identified_by = models.ForeignKey("user.User", verbose_name="Identified by", null=True, blank=True,
                                      on_delete=models.SET_NULL, related_name="ncouteridentified")
    completeddate = models.DateField("Completion date", null=True, blank=False, )
    completed_by = models.ForeignKey("user.User", verbose_name="Identified by", null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name="ncoutercompleted")
    revieweddate = models.DateField("Review date", null=True, blank=False, )
    reviewed_by = models.ForeignKey("user.User", verbose_name="Identified by", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="ncouterreviewed")
    no = models.PositiveIntegerField(verbose_name="No", default=1, )

    def verify(self):
        if self.completeddate and self.completed_by:
            return True

        return False

    def save(self, *args, **kwargs):
        self.verified = self.verify()
        super(NonConformanceOuterResponse, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'Outer NC')
        verbose_name_plural = _(u'Outer NC')
        ordering = ['started']


class NonConformanceOuterResponseStates(models.Model):
    class Priority(DjangoChoices):
        low = ChoiceItem("low", label=_('Low'))
        medium = ChoiceItem("medium", label=_('Medium'))
        high = ChoiceItem("high", label=_('High'))

    legislation = models.ForeignKey(Register, on_delete=models.CASCADE, blank=False,
                                    related_name="legislationouternc")
    source = models.ForeignKey(SourceNC, on_delete=models.CASCADE, null=True)
    started = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, blank=False, auto_now=True)
    identified = models.TextField("Identified by", max_length=2000, null=True)
    assigned = models.TextField("Assigned to", max_length=2000, null=True)
    containment = models.TextField("Containment actions", max_length=2000, null=True)
    completion = models.TextField("Completion date & by whom", max_length=2000, null=True)
    root = models.TextField("Root cause", max_length=2000, null=True)
    corrective = models.TextField("Corrective actions", max_length=2000, null=True)
    cost = models.TextField("Cost of nonconformance", max_length=2000, null=True)
    reviewed = models.TextField("Reviewed and closed out by", max_length=2000, null=True)
    desc = models.TextField("Description", max_length=2000, null=True)
    assign = models.ForeignKey("user.User", null=True, blank=True, on_delete=models.SET_NULL)
    verified = models.BooleanField(_('Verified'), default=False, editable=False)

    priority = models.CharField("Priority", choices=Priority.choices, default=Priority.low, max_length=15)
    identified_by = models.ForeignKey("user.User", verbose_name="Identified by", null=True, blank=True,
                                      on_delete=models.SET_NULL, related_name="ncouterstateidentified")
    completeddate = models.DateField("Completion date", null=True, blank=False, )
    completed_by = models.ForeignKey("user.User", verbose_name="Identified by", null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name="ncouterstatecompleted")
    revieweddate = models.DateField("Review date", null=True, blank=False, )
    reviewed_by = models.ForeignKey("user.User", verbose_name="Identified by", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="ncouterstatereviewed")

    class Meta:
        verbose_name = _(u'State of Outer NC')
        verbose_name_plural = _(u'State of Outer NC')


class Guidance(models.Model):
    title = models.CharField(_('Title'), max_length=300)
    file = models.FileField(_('File'), max_length=2000, upload_to='guidance/%Y/%m/%d/')
    locations = models.ManyToManyField(Location, verbose_name="Location", blank=True, )
    topics = models.ManyToManyField(Topic, verbose_name="Topics", blank=True, )
    category = models.ManyToManyField(Category, verbose_name="Sector", blank=True)
    published = models.BooleanField(_('Published'), default=False, )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _(u'Guidance')
        verbose_name_plural = _(u'Guidance')
        ordering = ['title']
