from django import forms
#from django.forms import ModelForm, fields
#from django.forms.models import _Labels
from .models import BookInstance
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime


class RenewBookForm(forms.Form):
  renewal_date = forms.DateField(help_text='Enter a day between now and 4 weeks (default 3).')

  def clean_renewal_date(self):
    data = self.cleaned_data['renewal_date']

    # check if data is not in past
    if data < datetime.date.today():
      raise ValidationError(_('Invalid date - renewal in past'))
    
    #Check date is in range librarian allowed to change (+4 weeks).
    if data > datetime.date.today() + datetime.timedelta(weeks=4):
      raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

    # Remember to always return the cleaned data.
    return data


""" class RenewBookModelForm(ModelForm):
  class Meta:
    model = BookInstance
    fields = ['due_back',]
    _Labels = { 'due_back': _('renewal_date'), }
    help_text = { 
      'due_back': _('Enter a date between now and 4 weeks (default 3).'),
    }
  
  def clean_due_back(self):
       data = self.cleaned_data['due_back']

       #Check date is not in past.
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

       #Check date is in range librarian allowed to change (+4 weeks)
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       # Remember to always return the cleaned data.
       return data """