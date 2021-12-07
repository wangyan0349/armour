import json
import mimetypes
import os
import uuid
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView, View, RedirectView, TemplateView, DeleteView
from wkhtmltopdf.views import PDFTemplateView

from .models import Register, Question, LegislationPosition, LegislationSpecQuestion, LegislationTopic, \
    LegislationTopicsResponse, LegislationNonConformanceResponse, SourceNC, LegislationDocument, \
    Document, NonConformanceOuterResponse, NonConformanceOuterResponseStates, \
    LegislationTopicsKeyPointResponse, KeyPoint, Guidance, DiscountCodes
from ..company.models import PaymentsPositions
from ..general.mixins import PaymentValidMixin, AjaxableResponseMixin, VerifyAllSpecQuestions, VerifyLegTopis, \
    VerifyAllSpecQuestionsAJAX, VerifyLegTopisAJAX, PaymentValidMixinAJAX, OrganizationIsActive, \
    PlanCheckFree


class SpecificQuestions(LoginRequiredMixin, OrganizationIsActive, DetailView):
    template_name = 'legislation/specific-questions.html'

    def get_context_data(self, **kwargs):
        context = super(SpecificQuestions, self).get_context_data(**kwargs)
        conf = self.request.user.company.get_open_register()
        src = self.request.user.company.gen_all_published_products()

        if len(src.get('questions_id', [])) > 0:
            LegislationSpecQuestion.objects.filter(position__register=conf, ).exclude(
                question__id__in=src.get('questions_id', [])).delete()

        context['data'] = src
        context['selected'] = LegislationSpecQuestion.objects.filter(position__register=conf, )
        return context

    def get_object(self, **kwargs):
        conf = self.request.user.company.get_open_register()

        if not conf:
            conf = Register.objects.create(company=self.request.user.company)
            return conf
        else:
            return conf


class SetSpecQuestionView(LoginRequiredMixin, OrganizationIsActive, AjaxableResponseMixin, View):
    def post(self, request, *args, **kwargs):
        conf = self.request.user.company.get_open_register()

        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        question = data.get('question')
        reply = data.get('reply', '0')
        answer = False
        if int(reply) == 1:
            answer = True

        quest = Question.objects.get(id=question)

        poz, created = LegislationPosition.objects.get_or_create(register=conf, topic=quest.legtopic.topic,
                                                                 location=quest.legtopic.location)

        sc, created = LegislationSpecQuestion.objects.get_or_create(position=poz, question=quest)
        sc.response = answer
        sc.save()

        return JsonResponse({"status": "OK"})


class LegislationTopicsView(LoginRequiredMixin, PaymentValidMixin, VerifyAllSpecQuestions, DetailView):
    template_name = 'legislation/legislation-topics.html'

    def get_context_data(self, **kwargs):
        context = super(LegislationTopicsView, self).get_context_data(**kwargs)
        context['data'] = self.request.user.company.gen_products(check_free=True)
        return context

    def get_object(self, **kwargs):
        return self.request.user.company.get_open_register()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LegislationTopicsContentView(LoginRequiredMixin, PaymentValidMixinAJAX, AjaxableResponseMixin,
                                   VerifyAllSpecQuestionsAJAX, View):
    template_name = "legislation/legislation-topics-content.html"

    def get(self, request, *args, **kwargs):
        conf = self.request.user.company.get_open_register()
        qargs = [Q(legquestions__isnull=False, legquestions__questionsresponses__response=True,
                   legquestions__questionsresponses__position__register=conf) | Q(legquestions__isnull=True)]
        qargs1 = [Q(category__in=self.request.user.company.category.all()) | Q(category__isnull=True)]

        ltopics = []
        firstnotfilled = None
        mess = self.request.session.get('validerror', False)

        if self.request.user.company.free:
            src = LegislationTopic.objects.filter(*qargs, *qargs1, published=True, kpoints__isnull=False,
                                                  location__id=request.GET.get('location'),
                                                  topic__id=request.GET.get('topic'), free=True).order_by(
                'order').distinct()[
                  :settings.FREE_LIMIT]


        else:
            src = LegislationTopic.objects.filter(*qargs, *qargs1, published=True, kpoints__isnull=False,
                                                  location__id=request.GET.get('location'),
                                                  topic__id=request.GET.get('topic')).order_by('orderfull').distinct()
        for l in src:
            ltopics.append(l)
            if mess and not firstnotfilled:
                if l.ltopicreply.filter(position__register=conf).count() == 0:
                    firstnotfilled = len(ltopics)

                for r in l.ltopicreply.filter(position__register=conf):

                    if not r.verify():
                        firstnotfilled = len(ltopics)
                        break;

        if self.request.user.company.free:
            if len(ltopics) < settings.FREE_LIMIT:
                rqcount = settings.FREE_LIMIT - len(ltopics)
                if rqcount > 0:
                    rq = self.request.user.company.req.filter(published=True,
                                                              reqpoints__isnull=False).distinct().order_by(
                        'name')[:rqcount]
                    for l in rq:
                        ltopics.append(l)

                        if mess and not firstnotfilled:
                            if l.postopicresponses.filter(position__register=conf).count() == 0:
                                firstnotfilled = len(ltopics) + 1

                            for r in l.reqreply.filter(position__register=conf):
                                if not r.verify():
                                    firstnotfilled = len(ltopics) + 1
                                    break;


        else:
            rq = self.request.user.company.req.filter(published=True, reqpoints__isnull=False).distinct().order_by(
                'name')
            for l in rq:
                ltopics.append(l)
                if mess and not firstnotfilled:
                    if l.postopicresponses.filter(position__register=conf).count() == 0:
                        firstnotfilled = len(ltopics)

                    for r in l.reqreply.filter(position__register=conf):
                        if not r.verify():
                            firstnotfilled = len(ltopics)
                            break;

        qanswers = [Q(topicresponse__isnull=False, topicresponse__position__location__id=request.GET.get('location'),
                      topicresponse__position__topic__id=request.GET.get('topic')) | Q(
            topicresponse__req__isnull=False)]

        answers = LegislationTopicsKeyPointResponse.objects.filter(topicresponse__position__register=conf, *qanswers)

        progress = conf.get_legtopic_progress(request.GET.get('location'), request.GET.get('topic'))

        posqanswers = [
            Q(req__isnull=True, location__id=request.GET.get('location'), topic__id=request.GET.get('topic')) | Q(
                req__isnull=False)]

        position = None
        if not mess:
            lastposition = conf.legislationpos.filter(*posqanswers).order_by("-topicpos").first()
            if lastposition:
                position = lastposition.topicpos

        elif firstnotfilled:
            position = firstnotfilled

        if mess:
            del self.request.session['validerror']

        d = {'content': render_to_string(self.template_name,
                                         {'ltopics': ltopics, 'answers': answers, "position": position,
                                          }, request=request),
             'prdprogress': progress.get('prdprogress'),
             'allprogress': progress.get('allprogress'),
             'counter': len(ltopics)}
        return JsonResponse(d)


class SetLegistaltionTopicView(LoginRequiredMixin, PaymentValidMixinAJAX, AjaxableResponseMixin,
                               VerifyAllSpecQuestionsAJAX,
                               View):
    def post(self, request, *args, **kwargs):
        today = datetime.now()

        paids = PaymentsPositions.objects.filter(payment__validate__gte=today, payment__date__lte=today,
                                                 payment__company=self.request.user.company)

        if paids.count() == 0:
            return JsonResponse({'error': "You can't do this operation"}, status=400)
        else:

            conf = self.request.user.company.get_open_register()

            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
            reply = data.get('reply', '')
            ncdesc = data.get('ncdesc', '')
            keypoint = data.get('keypoint', None)
            keypointnote = data.get('keypointnote', '')
            kp = KeyPoint.objects.get(id=keypoint)
            position = data.get('position', '')

            if kp.legtopic:

                poz, created = LegislationPosition.objects.get_or_create(legislation=conf, topic=kp.legtopic.topic,
                                                                         location=kp.legtopic.location)

                sc, created = LegislationTopicsResponse.objects.get_or_create(position=poz, legtopic=kp.legtopic)
            elif kp.req:
                poz, created = LegislationPosition.objects.get_or_create(legislation=conf, req=kp.req)

                sc, created = LegislationTopicsResponse.objects.get_or_create(position=poz, req=kp.req)

            else:
                return JsonResponse({'error': "You can't do this operation"}, status=400)

            pos = 0
            if reply == '' or reply == 0:
                pos = 0
            else:
                pos = int(reply)

            kppoz, created = LegislationTopicsKeyPointResponse.objects.get_or_create(topicresponse=sc, point=kp)

            kppoz.note = keypointnote
            kppoz.response = pos
            kppoz.ncnote = ncdesc
            kppoz.save()
            progress = conf.get_legtopic_progress(data.get('location'), data.get('topic'))

            if position:
                poz.topicpos = position
                poz.save()

                posqanswers = [Q(req__isnull=True, location__id=data.get('location'), topic__id=data.get('topic')) | Q(
                    req__isnull=False)]

                conf.legislationpos.filter(*posqanswers).exclude(id=poz.id).update(topicpos=1)

            sc.status = sc.set_status_number()
            sc.save()

            return JsonResponse({"status": "OK", 'prdprogress': progress.get('prdprogress'),
                                 'allprogress': progress.get('allprogress')})


class LegislationNonConformanceView(LoginRequiredMixin, PaymentValidMixin, VerifyAllSpecQuestions, VerifyLegTopis,
                                    DetailView):
    template_name = 'legislation/legislation-nonconformance.html'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        exists = []
        topics = LegislationTopicsKeyPointResponse.objects.filter(topicresponse__position__register=obj,
                                                                  response__in=[0]).distinct()

        if topics.count() == 0:
            LegislationNonConformanceResponse.objects.filter(topicreply__position__register=obj).delete()
            return super(LegislationNonConformanceView, self).get(request, *args, **kwargs)
        else:

            for answer in topics:
                sc, created = LegislationNonConformanceResponse.objects.get_or_create(topicreply=answer.topicresponse,
                                                                                      point=answer.point)
                if not sc.ncdesc:
                    sc.ncdesc = answer.ncnote
                    sc.save()

                exists.append(sc.id)

            LegislationNonConformanceResponse.objects.filter(topicreply__position__register=obj).exclude(
                id__in=exists).delete()

            return super(LegislationNonConformanceView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LegislationNonConformanceView, self).get_context_data(**kwargs)
        obj = self.get_object()
        nonconformance = []
        inner = LegislationNonConformanceResponse.objects.filter(
            topicreply__position__register=obj).distinct().order_by("started")

        # outer = self.request.user.company.companyouternc.all().distinct().order_by("started")
        outer = []
        for o in inner:
            nonconformance.append(o)

        for o in outer:
            nonconformance.append(o)

        context['nonconformance'] = nonconformance

        context['sourceslegal'] = SourceNC.objects.filter(default=True).order_by("name")
        context['sources'] = SourceNC.objects.filter(defaulto=True).order_by("name")

        return context

    def get_object(self):
        return self.request.user.company.get_open_register()


class SetNonConformanceView(LoginRequiredMixin, PaymentValidMixinAJAX, AjaxableResponseMixin,
                            VerifyAllSpecQuestionsAJAX,
                            VerifyLegTopisAJAX, View):
    def post(self, request, pk, *args, **kwargs):
        conf = self.request.user.company.get_open_register()
        try:
            obj = LegislationNonConformanceResponse.objects.get(topicreply__position__register=conf, id=pk)
        except:
            return JsonResponse({"status": "ERROR"}, status=400)

        sc = None
        if request.POST.get('source', None):
            sc = SourceNC.objects.get(id=request.POST.get('source'))

        obj.source = sc
        identified = request.POST.get('identified', '')
        if identified:
            obj.identified_by = self.request.user.company.companyusers.get(id=identified)

        priority = request.POST.get('priority', '')
        if priority:
            obj.priority = priority

        assign = request.POST.get('assign', '')
        if assign:
            assinguser = self.request.user.company.companyusers.get(id=assign)
            if not obj.assign or (obj.assign and obj.assign != assinguser):
                current_site = Site.objects.get_current()
                protocol = settings.IS_HTTPS and "https://" or "http://"
                baseurl = protocol + current_site.domain

                ctx = {'user': assinguser, 'baseurl': baseurl, 'nc': obj}
                content = render_to_string("email/new-nc.html", ctx, request=self.request)

                mail = EmailMessage(subject="New NC has been assigned to you", body=content,
                                    from_email=settings.DEFAULT_FROM_EMAIL, to=[assinguser.email])
                mail.content_subtype = 'html'
                mail.send()

            obj.assign = assinguser

        obj.root = request.POST.get('root', '')
        obj.corrective = request.POST.get('corrective', '')
        revieweddate = request.POST.get('reviewed', '')
        if revieweddate:
            revieweddate = datetime.strptime(revieweddate, "%d.%m.%Y").strftime("%Y-%m-%d")
            obj.revieweddate = revieweddate

        completeddate = request.POST.get('completeddate', '')
        if completeddate:
            completeddate = datetime.strptime(completeddate, "%d.%m.%Y").strftime("%Y-%m-%d")
            obj.completeddate = completeddate

        completed_by = request.POST.get('completed_by', '')
        if completed_by:
            obj.completed_by = self.request.user.company.companyusers.get(id=completed_by)

        reviewed_by = request.POST.get('reviewed_by', '')
        if reviewed_by:
            obj.reviewed_by = self.request.user.company.companyusers.get(id=reviewed_by)

        description = request.POST.get('description', '')
        if description:
            obj.ncdesc = description

        obj.save()
        content = ''
        createnew = request.POST.get('add-new', "0")

        if createnew == '1':
            no = self.request.user.company.companyouternc.all().distinct().count() + LegislationNonConformanceResponse.objects.filter(
                topicreply__position__register=conf).distinct().count() + 1
            newobj = NonConformanceOuterResponse.objects.create(company=self.request.user.company, initialrecord=True,
                                                                no=no)
            start = 0

            nonconformance = []
            inner = []

            if conf:
                inner = LegislationNonConformanceResponse.objects.filter(
                    topicreply__position__register=conf).distinct().order_by("started")

            outer = self.request.user.company.companyouternc.all().distinct().order_by("started")

            for o in inner:
                nonconformance.append(o)

            for o in outer:
                nonconformance.append(o)

            content = render_to_string("legislation/outer-nc-content.html",
                                       {'nonconformance': nonconformance, 'start': start,
                                        'company': self.request.user.company,
                                        'inittab': len(nonconformance),
                                        'sourceslegal': SourceNC.objects.filter(default=True).order_by("name"),
                                        'sources': SourceNC.objects.filter(defaulto=True).order_by("name"), },
                                       request=request)

        return JsonResponse(
            {"status": "OK", 'verify': obj.verify() and 1 or 0, 'id': obj.id, 'nctype': 'inner', 'content': content})


class FinishView(LoginRequiredMixin, PaymentValidMixin, RedirectView):
    pattern_name = 'leg-list'

    def get_redirect_url(self, *args, **kwargs):
        lopen = self.request.user.company.get_open_register()
        if lopen:
            today = datetime.now()
            lopen.finished = True
            lopen.finish_date = today
            lopen.save()

            for d in Document.objects.all():
                try:
                    cp = ContentFile(d.file.read())
                except:
                    continue;

                cp.name = d.file.name

                dc = LegislationDocument(legislation=lopen, title=d.title, file=cp)
                dc.save()

            for nco in NonConformanceOuterResponse.objects.filter(company=self.request.user.company,
                                                                  initialrecord=False).order_by('id'):
                nc = NonConformanceOuterResponseStates(legislation=lopen, source=nco.source,
                                                       started=nco.started, updated=nco.updated,
                                                       identified=nco.identified,
                                                       assigned=nco.assigned, containment=nco.containment,
                                                       completion=nco.completion,
                                                       root=nco.root, corrective=nco.corrective, cost=nco.cost,
                                                       reviewed=nco.reviewed, desc=nco.description,
                                                       assign=nco.assign, verified=nco.verified, priority=nco.priority,
                                                       identified_by=nco.identified_by,
                                                       completeddate=nco.completeddate, completed_by=nco.completed_by,
                                                       revieweddate=nco.revieweddate,
                                                       reviewed_by=nco.reviewed_by)
                nc.save()

        return super(FinishView, self).get_redirect_url(*args, **kwargs)


class LegislationListView(LoginRequiredMixin, PaymentValidMixin, DetailView):
    template_name = 'legislation/legislation-list.html'

    def get_context_data(self, **kwargs):
        context = super(LegislationListView, self).get_context_data(**kwargs)
        context['open'] = self.request.user.company.get_open_register()
        context['docs'] = Document.objects.all()

        newspecq = []
        # FIXME This view seems to show when legislation has changed, fix once versioning working
        # if newversion:
        #     products = self.request.user.company.gen_version_published_products(newversion).get('questions', [])
        #     ids = []
        #     for p in products:
        #         quest = p.get('get_questions', [])
        #         if quest:
        #             ids += quest.values_list("id", flat=True)
        #
        #     if len(ids):
        #         qargs = [Q(changed=True) | Q(legtopic__changed=True) | Q(legtopic__kpoints__changed=True)]
        #         newspecq = Question.objects.filter(id__in=ids, legtopic__version=newversion,
        #                                            *qargs).distinct().order_by('title')

        context['newspecq'] = newspecq

        return context

    def get_object(self, **kwargs):
        return self.request.user.company


class StartNewView(FinishView):
    pattern_name = 'organization-update'


class LegislationDocView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        doc = get_object_or_404(LegislationDocument, uuid=pk, legislation__company=self.request.user.company)
        fullpath = doc.file.path

        if os.path.exists(fullpath):
            with open(fullpath, 'rb') as fh:
                mimetype, encoding = mimetypes.guess_type(fullpath)
                response = HttpResponse(fh.read(), content_type=mimetype)
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(fullpath)
                return response

        raise Http404


class LegislationReportView(LoginRequiredMixin, PDFTemplateView):
    template_name = 'pdf/report.html'
    filename = 'my_pdf.pdf'
    show_content_in_browser = True
    object = None
    cmd_options = {
        'orientation': 'landscape',
    }

    def get(self, request, pk, *args, **kwargs):
        self.object = get_object_or_404(Register, uuid=pk, company=self.request.user.company)
        return super(LegislationReportView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LegislationReportView, self).get_context_data(**kwargs)
        context['staticroot'] = settings.STATIC_ROOT
        context['object'] = self.object
        product = self.request.GET.get('product', '')
        positions = self.object.get_products()
        if product:
            positions = positions.filter(id=product)

        other = self.object.get_other()

        ncs = self.object.get_ncs()
        if product:
            ncs = ncs.filter(topicreply__position__id=product)

        context['positions'] = positions
        context['others'] = other
        context['ncs'] = ncs

        return context


class OuterNonConformanceView(LoginRequiredMixin, PaymentValidMixin, TemplateView):
    template_name = 'legislation/outer-nonconformance.html'

    def get(self, request, *args, **kwargs):
        topics = self.request.user.company.companyouternc.all().count()
        if topics == 0:
            t = NonConformanceOuterResponse.objects.create(company=self.request.user.company, initialrecord=True)
        return super(OuterNonConformanceView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OuterNonConformanceView, self).get_context_data(**kwargs)
        obj = self.get_object()

        exists = []
        topics = LegislationTopicsKeyPointResponse.objects.filter(topicresponse__position__register=obj,
                                                                  response__in=[0]).distinct()
        for answer in topics:
            sc, created = LegislationNonConformanceResponse.objects.get_or_create(topicreply=answer.topicresponse,
                                                                                  point=answer.point)
            if not sc.ncdesc:
                sc.ncdesc = answer.ncnote
                sc.save()

            exists.append(sc.id)

        LegislationNonConformanceResponse.objects.filter(topicreply__position__register=obj).exclude(
            id__in=exists).delete()

        start = 0
        topics = 0
        context['nonconformance'] = []
        inner = []
        no = 1
        if obj:
            for nc in LegislationNonConformanceResponse.objects.filter(topicreply__position__register=obj).order_by(
                    "started"):
                nc.no = no
                nc.save()
                no += 1

            inner = LegislationNonConformanceResponse.objects.filter(topicreply__position__register=obj).order_by(
                "started")

        context['start'] = start
        for nc in self.request.user.company.companyouternc.all().order_by("started"):
            nc.no = no
            nc.save()
            no += 1

        outer = self.request.user.company.companyouternc.all().order_by("started")
        context['nonconformance'] = []
        for o in inner:
            context['nonconformance'].append(o)

        for o in outer:
            context['nonconformance'].append(o)

        context['inittab'] = int(1)
        context['company'] = self.request.user.company

        context['sources'] = SourceNC.objects.filter(defaulto=True).order_by("name")
        context['sourceslegal'] = SourceNC.objects.filter(default=True).order_by("name")
        context['nc_open'] = self.request.GET.get('nc-open', None)

        return context

    def get_object(self):
        return self.request.user.company.get_open_register()


class SetOuterNonConformanceView(LoginRequiredMixin, PaymentValidMixinAJAX, AjaxableResponseMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            obj = NonConformanceOuterResponse.objects.get(company=self.request.user.company, id=pk)
        except:
            return JsonResponse({"status": "ERROR"}, status=400)

        sc = None
        if request.POST.get('source', None):
            sc = SourceNC.objects.get(id=request.POST.get('source'))

        obj.source = sc
        identified = request.POST.get('identified', '')
        if identified:
            obj.identified_by = self.request.user.company.companyusers.get(id=identified)

        priority = request.POST.get('priority', '')
        if priority:
            obj.priority = priority

        assign = request.POST.get('assign', '')
        if assign:
            assinguser = self.request.user.company.companyusers.get(id=assign)
            if not obj.assign or (obj.assign and obj.assign != assinguser):
                current_site = Site.objects.get_current()
                protocol = settings.IS_HTTPS and "https://" or "http://"
                baseurl = protocol + current_site.domain

                ctx = {'user': assinguser, 'baseurl': baseurl, 'nc': obj}
                content = render_to_string("email/new-nc.html", ctx, request=self.request)

                mail = EmailMessage(subject="New", body=content,
                                    from_email=settings.DEFAULT_FROM_EMAIL, to=[assinguser.email])
                mail.content_subtype = 'html'
                mail.send()

            obj.assign = assinguser

        obj.root = request.POST.get('root', '')
        obj.corrective = request.POST.get('corrective', '')
        obj.description = request.POST.get('description', '')

        revieweddate = request.POST.get('revieweddate', '')
        if revieweddate:
            revieweddate = datetime.strptime(revieweddate, "%d.%m.%Y").strftime("%Y-%m-%d")
            obj.revieweddate = revieweddate

        completeddate = request.POST.get('completeddate', '')

        if completeddate:
            completeddate = datetime.strptime(completeddate, "%d.%m.%Y").strftime("%Y-%m-%d")
            obj.completeddate = completeddate

        completed_by = request.POST.get('completed_by', '')
        if completed_by:
            obj.completed_by = self.request.user.company.companyusers.get(id=completed_by)

        reviewed_by = request.POST.get('reviewed_by', '')
        if reviewed_by:
            obj.reviewed_by = self.request.user.company.companyusers.get(id=reviewed_by)

        if sc or request.POST.get('reviewed_by', '') or request.POST.get('completed_by', '') or request.POST.get(
                'revieweddate', '') or request.POST.get('completeddate', '') or request.POST.get('identified',
                                                                                                 '') or request.POST.get(
            'assigned', '') or request.POST.get(
            'containment', '') or request.POST.get('completion', '') or request.POST.get('root',
                                                                                         '') or request.POST.get(
            'corrective', '') or request.POST.get('priority', '') or request.POST.get('reviewed',
                                                                                      '') or request.POST.get(
            'description', ''):
            obj.initialrecord = False

        obj.save()

        createnew = request.POST.get('add-new', "0")
        content = ''
        if createnew == '1':
            leg = self.request.user.company.get_open_register()
            no = self.request.user.company.companyouternc.all().distinct().count() + LegislationNonConformanceResponse.objects.filter(
                topicreply__position__register=leg).distinct().count() + 1

            newobj = NonConformanceOuterResponse.objects.create(company=self.request.user.company, initialrecord=True,
                                                                no=no)
            start = 0

            nonconformance = []
            inner = []
            if leg:
                inner = LegislationNonConformanceResponse.objects.filter(
                    topicreply__position__register=leg).distinct().order_by("started")

            outer = self.request.user.company.companyouternc.all().distinct().order_by("started")

            for o in inner:
                nonconformance.append(o)

            for o in outer:
                nonconformance.append(o)

            content = render_to_string("legislation/outer-nc-content.html",
                                       {'nonconformance': nonconformance, 'start': start,
                                        'company': self.request.user.company,
                                        'inittab': len(nonconformance),
                                        'sources': SourceNC.objects.filter(defaulto=True).order_by("name"),
                                        'sourceslegal': SourceNC.objects.filter(default=True).order_by("name")},
                                       request=request)

        return JsonResponse(
            {"status": "OK", 'verify': obj.verify() and 1 or 0, 'id': obj.id, 'content': content, 'nctype': 'outer'})


class LegislationDeleteView(LoginRequiredMixin, AjaxableResponseMixin, DeleteView):
    template_name = "legislation/legislation-delete.html"
    model = Register
    object = None

    def get_object(self):
        return Register.objects.get(pk=self.kwargs.get('pk'), company=self.request.user.company)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        ctx = self.get_context_data(*args, **kwargs)
        d = {'content': render_to_string(self.template_name, ctx, request=request)}
        return JsonResponse(d)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {'pk': self.kwargs.get('pk'), }
        self.object.delete()
        return JsonResponse(data)

    def get_success_url(self):
        pass


class LegislationNCReportView(LoginRequiredMixin, PDFTemplateView):
    template_name = 'pdf/report_nc.html'
    filename = 'my_pdf.pdf'
    show_content_in_browser = True
    object = None
    cmd_options = {
        'orientation': 'landscape',
    }

    def get(self, request, pk, *args, **kwargs):
        self.object = get_object_or_404(Register, uuid=pk, company=self.request.user.company)
        return super(LegislationNCReportView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LegislationNCReportView, self).get_context_data(**kwargs)
        context['staticroot'] = settings.STATIC_ROOT
        context['object'] = self.object
        context['closed'] = []
        context['opened'] = []
        context['company'] = self.request.user.company
        mode = kwargs.get('mode', 'All')
        product = self.request.GET.get('product', None)
        source = self.request.GET.get('source', None)

        if source:
            ncsource = SourceNC.objects.filter(id=source).first()
            if ncsource:
                mode = ncsource.name

        elif mode == 'outer' and not source:
            mode = "All"

        context['mode'] = mode
        opened = []
        closed = []

        if mode == "inner" and product:
            src = LegislationNonConformanceResponse.objects.filter(topicreply__position__register=self.object,
                                                                   topicreply__position__id=product)
            opened = src.filter(verified=False).values_list('source__name', 'ncdesc', 'updated', 'root',
                                                            'corrective', 'no').distinct().order_by("started")
            closed = src.filter(verified=True).values_list('source__name', 'ncdesc', 'updated', 'root',
                                                           'corrective', 'no').distinct().order_by("started")

        elif mode == "inner" and not product:
            src = LegislationNonConformanceResponse.objects.filter(topicreply__position__register=self.object)
            opened = src.filter(verified=False).values_list('source__name', 'ncdesc', 'updated', 'root',
                                                            'corrective', 'no').distinct().order_by("started")
            closed = src.filter(verified=True).values_list('source__name', 'ncdesc', 'updated', 'root',
                                                           'corrective', 'no').distinct().order_by("started")

        elif mode == "outer" and product:
            src = NonConformanceOuterResponse.objects.filter(topicreply__position__id=product)
            opened = src.filter(verified=False, ).values_list('source__name', 'description', 'updated', 'root',
                                                              'corrective', 'no').distinct().order_by("started")
            closed = src.filter(verified=True, ).values_list('source__name', 'description', 'updated', 'root',
                                                             'corrective', 'no').distinct().order_by("started")

        elif mode == "outer" and not product:
            src = NonConformanceOuterResponse.objects.all()
            opened = src.filter(verified=False).values_list('source__name', 'description', 'updated', 'root',
                                                            'corrective', ).distinct().order_by("started")
            closed = src.filter(verified=True).values_list('source__name', 'description', 'updated', 'root',
                                                           'corrective', 'no').distinct().order_by("started")

        for o in opened:
            context['opened'].append(o)

        for o in closed:
            context['closed'].append(o)

        context['cnt'] = len(context['closed']) + len(context['opened'])
        return context


class LegislationNCOuterReportView(LoginRequiredMixin, PDFTemplateView):
    template_name = 'pdf/report_nc.html'
    filename = 'my_pdf.pdf'
    show_content_in_browser = True
    object = None
    cmd_options = {
        'orientation': 'landscape',
    }

    def get_context_data(self, **kwargs):
        context = super(LegislationNCOuterReportView, self).get_context_data(**kwargs)
        context['staticroot'] = settings.STATIC_ROOT
        context['closed'] = []
        context['opened'] = []
        context['company'] = self.request.user.company
        source = self.request.GET.get('source', None)
        mode = "All"
        if source:
            ncsource = SourceNC.objects.filter(id=source).first()
            if ncsource:
                mode = ncsource.name

        context['mode'] = mode
        opened = []
        closed = []

        if source:
            src = NonConformanceOuterResponse.objects.filter(source__id=source, company=self.request.user.company)
            opened = src.filter(verified=False, ).values_list('source__name', 'description', 'updated', 'root',
                                                              'corrective', 'no').distinct().order_by("started")
            closed = src.filter(verified=True, ).values_list('source__name', 'description', 'updated', 'root',
                                                             'corrective', 'no').distinct().order_by("started")

        else:
            src = NonConformanceOuterResponse.objects.filter(company=self.request.user.company)
            opened = src.filter(verified=False).values_list('source__name', 'description', 'updated', 'root',
                                                            'corrective', 'no').distinct().order_by("started")
            closed = src.filter(verified=True).values_list('source__name', 'description', 'updated', 'root',
                                                           'corrective', 'no').distinct().order_by("started")

        for o in opened:
            context['opened'].append(o)

        for o in closed:
            context['closed'].append(o)

        context['cnt'] = len(context['closed']) + len(context['opened'])
        return context


class SpecQuestionConfirmationView(LoginRequiredMixin, OrganizationIsActive, VerifyAllSpecQuestions, TemplateView):
    template_name = 'legislation/spec-question-confirmation.html'

    def get_context_data(self, **kwargs):
        context = super(SpecQuestionConfirmationView, self).get_context_data(**kwargs)

        data = self.request.user.company.gen_all_published_products().get('legtopics', [])
        count = 0

        if len(data) > 0:
            conf = self.request.user.company.get_open_register()
            qargs = [Q(legquestions__isnull=False, legquestions__questionsresponses__response=True,
                       legquestions__questionsresponses__position__register=conf) | Q(legquestions__isnull=True)]
            qargs1 = [Q(category__in=self.request.user.company.category.all()) | Q(category__isnull=True)]

            src = LegislationTopic.objects.filter(*qargs, *qargs1, published=True, kpoints__isnull=False).distinct()

            count = src.count() + self.request.user.company.req.all().count()

            if self.request.user.company.active and not self.request.user.company.specqgenerated:
                self.request.user.company.specqgenerated = True
                self.request.user.company.save()

        context['count'] = count
        return context


class PlanSpecQuestionConfirmationView(LoginRequiredMixin, OrganizationIsActive, VerifyAllSpecQuestions, PlanCheckFree,
                                       TemplateView):
    template_name = 'legislation/spec-question-plan.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.company.active and not self.request.user.company.specqgenerated:
            self.request.user.company.specqgenerated = True
            self.request.user.company.save()

        return super(PlanSpecQuestionConfirmationView, self).get(request, *args, **kwargs)


class GuidanceListView(LoginRequiredMixin, DetailView):
    template_name = 'legislation/guidance-list.html'

    def get_context_data(self, **kwargs):
        context = super(GuidanceListView, self).get_context_data(**kwargs)
        company = self.request.user.company
        qargs = [Q(locations__isnull=True, topics__isnull=True, category__isnull=True) | Q(
            locations__in=company.locations.all()) | Q(topics__in=company.topics.all()) | Q(
            category__in=company.category.all())]
        context['docs'] = Guidance.objects.filter(published=True, *qargs).distinct()

        return context

    def get_object(self):
        return self.request.user.company


class LegUpdateView(LoginRequiredMixin, PaymentValidMixin, View):
    def post(self, request, *args, **kwargs):
        origin = self.request.user.company.get_open_register()
        newversion = False  # FIXME after versioning
        if not newversion:
            messages.add_message(self.request, messages.ERROR, "Newer version doesn't exist", )
            return HttpResponseRedirect(reverse_lazy("leg-list"))

        new = False
        if not origin:
            origin = self.request.user.company.get_last_register()
            new = True

        if origin:
            conf = Register.objects.get(id=origin.id)
            if new:
                conf.pk = None
                conf.save()
                conf.finished = False
                conf.finish_date = None
                conf.uuid = str(uuid.uuid4())

            conf.version = newversion
            conf.save()

            for originpos in origin.legislationpos.all():
                pos = origin.legislationpos.get(id=originpos.id)
                if new:
                    pos.pk = None
                    pos.save()
                    pos.register = conf

                pos.save()

                for originsq in originpos.specquerypos.all():
                    sq = originpos.specquerypos.get(id=originsq.id)
                    if new:
                        sq.pk = None
                        sq.save()
                        sq.position = pos

                    sqfirst = Question.objects.filter(legtopic__version=newversion,
                                                      parent=originsq.question).first()
                    if sqfirst:
                        sq.question = sqfirst

                    sq.save()

                for origintp in originpos.postopicresponses.all():
                    sq = originpos.postopicresponses.get(id=origintp.id)
                    if new:
                        sq.pk = None
                        sq.save()
                        sq.position = pos

                    if origintp.legtopic:
                        sqfirst = LegislationTopic.objects.filter(version=newversion,
                                                                  parent=origintp.legtopic).first()
                        if sqfirst:
                            sq.legtopic = sqfirst

                    sq.save()

                    for topicresponsekeyp in origintp.topicresponsekeyp.all():
                        kp = origintp.topicresponsekeyp.get(id=topicresponsekeyp.id)

                        kpfirst = KeyPoint.objects.filter(legtopic__version=newversion,
                                                          parent=topicresponsekeyp.point).first()
                        if new:
                            kp.pk = None
                            kp.topicresponse = sq
                            kp.save()

                        if kpfirst:
                            kp.point = kpfirst

                        kp.save()

                    if new:
                        for topicresponsenc in origintp.topicnon.all():
                            kp = origintp.topicnon.get(id=topicresponsenc.id)
                            kp.pk = None
                            kp.save()
                            kp.topicreply = sq
                            kp.save()

            self.request.user.company.version = newversion
            self.request.user.company.save()

            messages.add_message(self.request, messages.SUCCESS,
                                 'The update has been completed to %s version' % newversion.version, )

        else:
            messages.add_message(self.request, messages.ERROR, 'No legislative process', )

        return HttpResponseRedirect(reverse_lazy("leg-list"))


class SetDiscountView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        nx = request.POST.get('next', 'cc-update')

        if request.session.has_key('dcode'):
            del request.session['dcode']
            messages.add_message(self.request, messages.SUCCESS, 'The discount has been removed')
            return HttpResponseRedirect(reverse_lazy(nx))
        else:

            code = request.POST.get('discount-code', None)
            if not code:
                messages.add_message(self.request, messages.ERROR, "Discount code is empty", )
                return HttpResponseRedirect(reverse_lazy(nx))

            qargs = [Q(multiple=False, used=False) | Q(multiple=True)]

            try:
                dcode = DiscountCodes.objects.get(active=True, code=code, *qargs)
            except:
                messages.add_message(self.request, messages.ERROR, "Discount code does't exist or is inactive", )
                return HttpResponseRedirect(reverse_lazy(nx))

            request.session['dcode'] = dcode.id

            messages.add_message(self.request, messages.SUCCESS, 'The discount has been calculated')

            return HttpResponseRedirect(reverse_lazy(nx))
