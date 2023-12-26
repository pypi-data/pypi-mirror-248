from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy as _p

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from minidebconf.models import Diet, Registration, RegistrationType, ShirtSize
from minidebconf.models import ScheduleBlock


def register_form_factory():
    form_fields = ['full_name']
    notes = False
    if settings.MINIDEBCONF_REGISTER_PHONE is not None:
        form_fields.append('phone_number')
    if RegistrationType.objects.exists():
        form_fields.append('registration_type')
    form_fields.append('full_name')
    form_fields.append('involvement')
    form_fields.append('gender')
    form_fields.append('country')
    form_fields.append('city_state')
    if ScheduleBlock.objects.count() > 0:
        form_fields.append('days')
    if settings.MINIDEBCONF_REGISTER_ARRANGED_ACCOMMODATION:
        form_fields.append('arranged_accommodation')
        notes = True
    if settings.MINIDEBCONF_REGISTER_ARRANGED_FOOD:
        form_fields.append('arranged_food')
        notes = True
    if Diet.objects.exists():
        form_fields.append('diet')
    if settings.MINIDEBCONF_REGISTER_TRAVEL_REIMBURSEMENT:
        form_fields.append("travel_reimbursement")
        form_fields.append("travel_cost")
        notes = True
    if notes:
        form_fields.append("notes")
    if ShirtSize.objects.exists():
        form_fields.append('shirt_size')


    class RegisterForm(forms.ModelForm):
        full_name = forms.CharField(max_length=256, label=_('Full name'))
        class Meta:
            model = Registration
            fields = form_fields
            widgets = {
                'days': forms.CheckboxSelectMultiple(),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["full_name"].initial = self.instance.full_name
            if 'phone_number' in self.fields:
                self.fields["phone_number"].required = settings.MINIDEBCONF_REGISTER_PHONE
            if settings.MINIDEBCONF_REGISTER_DEFAULT_COUNTRY:
                self.initial['country'] = settings.MINIDEBCONF_REGISTER_DEFAULT_COUNTRY
            if 'arranged_accommodation' in self.fields:
                self.fields['arranged_accommodation'].label = _('I would like to stay at the conference-arranged accommodation')
            if 'arranged_food' in self.fields:
                self.fields['arranged_food'].label = _('I would like to have the conference-arranged meals')
            if 'travel_reimbursement' in self.fields:
                self.fields["travel_reimbursement"].label = _('I would like to request reimbursement of my travel costs')
            if 'travel_cost' in self.fields:
                self.fields['travel_cost'].label = _('Estimated travel cost (upper bound, in %(currency)s)') % { 'currency': settings.DEBCONF_BURSARY_CURRENCY_SYMBOL }

            self.helper = FormHelper()

            if self.instance.id:
                submit = _p("conference", "Update registration")
            else:
                submit = _p("conference", "Register")
            self.helper.add_input(Submit("submit", submit))


        def save(self):
            super().save()
            name = self.cleaned_data['full_name'].split()
            user = self.instance.user
            user.first_name = name[0]
            user.last_name = " ".join(name[1:])
            user.save()
    return RegisterForm
