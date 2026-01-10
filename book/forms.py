# book/forms.py

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Ҳамаи майдонҳоеро, ки корбар бояд пур кунад, номбар кунед
        # Барои илова, quantity_available дар __init__ хориҷ карда мешавад
        fields = [
            'name', 
            'class_number', 
            'year', 
            'price', 
            'quantity_total',
            'quantity_available',  # Барои update истифода мешавад, барои илова хориҷ карда мешавад
            # 'institution' -ро дар ин ҷо намегузорем, 
            # зеро онро ба таври худкор аз корбар мегирем.
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Илова кардани классҳои Bootstrap ба ҳамаи майдонҳо
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Тарҷумаи номҳои майдонҳо
        self.fields['name'].label = "Номи китоб"
        self.fields['class_number'].label = "Синф"
        self.fields['year'].label = "Соли воридшавӣ"
        self.fields['price'].label = "Нархи китоб"
        self.fields['quantity_total'].label = "Шумораи умумӣ"
        
        # Барои илова, quantity_available-ро хориҷ кардан
        # Агар instance вуҷуд надошта бошад ё instance.pk None бошад, ин илова аст
        if not self.instance or not self.instance.pk:
            # Барои илова, quantity_available-ро аз форма хориҷ мекунем, зеро онро дар view таъин мекунем
            if 'quantity_available' in self.fields:
                del self.fields['quantity_available']
        else:
            # Барои update, майдони quantity_available-ро нигоҳ дошта, label-ро таъин мекунем
            if 'quantity_available' in self.fields:
                self.fields['quantity_available'].label = "Шумораи дастрас (боқимонда)"