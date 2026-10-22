from django import forms

from plugins.pdf_viewer import logic


class ManagerForm(forms.Form):
    method = forms.ChoiceField(
        choices=logic.METHOD_CHOICES,
        label='PDF viewer method',
        help_text='How PDFs are embedded on article pages that have no HTML '
                  'galley. During the proof of concept, add '
                  '?pdf_viewer=object, embed or adobe to an article URL to '
                  'try another method.',
    )
    adobe_client_id = forms.CharField(
        required=False,
        label='Adobe PDF Embed client ID',
        help_text='Required for the Adobe method. Each client ID is '
                  'registered for a single domain.',
    )

    def __init__(self, *args, **kwargs):
        self.journal = kwargs.pop('journal')
        super().__init__(*args, **kwargs)
        self.fields['method'].initial = logic.get_setting(
            self.journal, 'pdf_viewer_method', logic.METHOD_NONE,
        )
        self.fields['adobe_client_id'].initial = logic.get_setting(
            self.journal, 'pdf_viewer_adobe_client_id',
        )

    def clean(self):
        cleaned_data = super().clean()
        if (
            cleaned_data.get('method') == logic.METHOD_ADOBE
            and not cleaned_data.get('adobe_client_id')
        ):
            self.add_error(
                'adobe_client_id',
                'A client ID is required for the Adobe method.',
            )
        return cleaned_data

    def save(self):
        logic.save_setting(
            self.journal,
            'pdf_viewer_method',
            self.cleaned_data['method'],
        )
        logic.save_setting(
            self.journal,
            'pdf_viewer_adobe_client_id',
            self.cleaned_data['adobe_client_id'].strip(),
        )
