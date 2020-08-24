from django import forms




CATEGORIES = [
    ('home', 'Home'),
    ('fashion', 'Fashion'),
    ('books', 'Books'),
    ('business', 'Business'),
    ('crafts', 'Crafts'),
    ('pet supplies', 'Pet Supplies'),
    ('other', 'Other')


]


class ListingForm(forms.Form):
    title = forms.CharField(label='Title')
    description = forms.CharField(widget=forms.Textarea(), label='Desctiption')
    starting_bid = forms.FloatField(label='Starting Bid')
    image_url = forms.URLField(label='Image URL', required=False)
    category = forms.MultipleChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices=CATEGORIES,
    )