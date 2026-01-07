# book/forms.py

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Ҳамаи майдонҳоеро, ки корбар бояд пур кунад, номбар кунед
        fields = [
            'name', 
            'class_number', 
            'year', 
            'price', 
            'quantity_total',
            'quantity_available', 
            # 'institution' -ро дар ин ҷо намегузорем, 
            # зеро онро ба таври худкор аз корбар мегирем.
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Илова кардани классҳои Bootstrap ба ҳамаи майдонҳо
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Тарҷумаи номҳои майдонҳо (агар лозим бошад)
        self.fields['name'].label = "Номи китоб"
        self.fields['class_number'].label = "Синф"
        self.fields['year'].label = "Соли воридшавӣ"
        self.fields['price'].label = "Нархи китоб"
        self.fields['quantity_total'].label = "Шумораи умумӣ"
        self.fields['quantity_available'].label = "Шумораи дастрас (боқимонда)"