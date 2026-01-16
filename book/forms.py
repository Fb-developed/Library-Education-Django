# book/forms.py

from django import forms
from .models import Book, BookPriceFactor

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


class BookPriceFactorForm(forms.ModelForm):
    class Meta:
        model = BookPriceFactor
        fields = [
            'label',
            'factor',
            'price_from',
            'price_to',
            'year_from',
            'year_to',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['label'].label = "Номгу"
        self.fields['factor'].label = "Фоиз аз нархи китоб"
        self.fields['price_from'].label = "Нарх аз"
        self.fields['price_to'].label = "Нарх то"
        self.fields['year_from'].label = "Соли нашр аз"
        self.fields['year_to'].label = "Соли нашр то"
        self.fields['description'].label = "Шарҳу эзоҳ"

    def clean(self):
        cleaned_data = super().clean()
        price_from = cleaned_data.get('price_from')
        price_to = cleaned_data.get('price_to')
        year_from = cleaned_data.get('year_from')
        year_to = cleaned_data.get('year_to')

        if price_from is not None and price_to is not None and price_from > price_to:
            self.add_error('price_to', 'Нарх то бояд аз нарх аз калон бошад.')

        if year_from is not None and year_to is not None and year_from > year_to:
            self.add_error('year_to', 'Соли нашр то бояд аз соли нашр аз калон бошад.')

        return cleaned_data
