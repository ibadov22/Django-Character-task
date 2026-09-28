from django import forms

from .models import CharacterRecord


class CharacterForm(forms.ModelForm):
    class Meta:
        model = CharacterRecord
        fields = ['name', 'character_type', 'health', 'attack_power', 'special']

        labels = {
            'name': 'Ad',
            'character_type': 'Tip',
            'health': 'Health',
            'attack_power': 'Attack Power',
            'special': 'Xüsusi dəyər',
        }

        help_texts = {
            'special': 'Warrior - defense, Mage - mana, Archer - arrows',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "Personajın adını daxil edin",
            }),
            'character_type': forms.Select(attrs={
                'class': 'form-select mb-3',
            }),
            'health': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
            }),
            'attack_power': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
            }),
            'special': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise forms.ValidationError("Ad ən azı 2 simvol olmalıdır")
        return name


class AttackForm(forms.Form):
    attacker = forms.ModelChoiceField(
        label='Attacker',
        queryset=CharacterRecord.objects.filter(health__gt=0),
        empty_label='Hücum edəni seçin',
        widget=forms.Select(attrs={'class': 'form-select mb-3'}),
    )
    target = forms.ModelChoiceField(
        label='Target',
        queryset=CharacterRecord.objects.filter(health__gt=0),
        empty_label='Hədəfi seçin',
        widget=forms.Select(attrs={'class': 'form-select mb-3'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        attacker = cleaned_data.get('attacker')
        target = cleaned_data.get('target')
        if attacker and target and attacker == target:
            raise forms.ValidationError("Personaj özünə hücum edə bilməz")
        return cleaned_data
