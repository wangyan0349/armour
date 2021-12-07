# -*- coding: utf-8 -*-
import stripe
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import LegislationTopic, KeyPoint, Question, VATRate, Document, Guidance, Location, Topic, Category


class DocumentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['locations'].widget = FilteredSelectMultiple('Location', is_stacked=False, )
        self.fields['locations'].queryset = Location.objects.all()

        self.fields['topics'].widget = FilteredSelectMultiple('Topic', is_stacked=False, )
        self.fields['topics'].queryset = Topic.objects.all()

        self.fields['category'].widget = FilteredSelectMultiple('Category', is_stacked=False, )
        self.fields['category'].queryset = Category.objects.all().order_by("name")

    class Meta:
        model = Document
        fields = '__all__'


class GuidanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GuidanceForm, self).__init__(*args, **kwargs)
        self.fields['locations'].widget = FilteredSelectMultiple('Location', is_stacked=False, )
        self.fields['locations'].queryset = Location.objects.all()

        self.fields['topics'].widget = FilteredSelectMultiple('Topic', is_stacked=False, )
        self.fields['topics'].queryset = Topic.objects.all()

        self.fields['category'].widget = FilteredSelectMultiple('Category', is_stacked=False, )
        self.fields['category'].queryset = Category.objects.all().order_by("name")

    class Meta:
        model = Guidance
        fields = '__all__'


class LegislationTopicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LegislationTopicForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        obj = super(LegislationTopicForm, self).save(commit=False)

        if commit:
            obj.changed = True
            obj.save()

        return obj

    class Meta:
        model = LegislationTopic
        fields = '__all__'


class KeyPointForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(KeyPointForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        obj = super(KeyPointForm, self).save(commit=False)

        if commit:
            obj.changed = True
            obj.save()

        return obj

    class Meta:
        model = KeyPoint
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        obj = super(QuestionForm, self).save(commit=False)

        if commit:
            obj.changed = True
            obj.save()

        return obj

    class Meta:
        model = Question
        fields = '__all__'


class VATRateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VATRateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        obj = super(VATRateForm, self).save(commit=False)

        if commit:

            stripe.api_key = settings.STRIPE_SECRET_KEY

            if not obj.stripeId:
                st = stripe.TaxRate.create(
                    display_name=obj.name,
                    percentage=obj.value,
                    inclusive=False,
                    active=True,
                )
                obj.stripeId = st.get('id')

            else:
                stripe.TaxRate.modify(
                    obj.stripeId,
                    display_name=obj.name,
                    active=False,
                )

                st = stripe.TaxRate.create(
                    display_name=obj.name,
                    percentage=obj.value,
                    inclusive=False,
                    active=True,
                )
                obj.stripeId = st.get('id')

            obj.save()

        return obj

    class Meta:
        model = VATRate
        fields = '__all__'
