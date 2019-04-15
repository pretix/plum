import os

from django import forms


class UploadedFileWidget(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class FakeFile:
        def __init__(self, file):
            self.file = file

        def __str__(self):
            return os.path.basename(self.file.name)

        @property
        def url(self):
            return self.file.url

    def format_value(self, value):
        if self.is_initial(value):
            return self.FakeFile(value)
