from models import Employee,Establishment,Theatre
from django import forms

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['name','theatre','Role',]

    def __init__(self, *args, **kwargs):
        self.usr = kwargs.pop('estb_usr',None)
        print self.usr
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['theatre'].queryset = Theatre.objects.filter(establishment__user=self.usr)