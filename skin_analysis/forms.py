# forms.py
from django import forms
from .models import SkinAnalysis

class ImageUploadForm(forms.ModelForm):
    image = forms.ImageField(
        label='Upload Skin Image',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*',  # Accept all image types
                'onchange': 'previewImage(this);'  # For image preview JS function
            }
        )
    )

    class Meta:
        model = SkinAnalysis
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (limit to 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image size should not exceed 5MB.")
            
            # Check file extension
            allowed_extensions = ['jpg', 'jpeg', 'png']
            ext = image.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    f"Only {', '.join(allowed_extensions)} files are allowed."
                )
            
            # Check image dimensions (optional)
            from PIL import Image
            img = Image.open(image)
            if img.width < 50 or img.height < 50:
                raise forms.ValidationError(
                    "Image dimensions should be at least 50x50 pixels."
                )
            
        return image