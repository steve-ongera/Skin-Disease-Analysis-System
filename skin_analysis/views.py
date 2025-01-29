from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SkinAnalysis
from .forms import ImageUploadForm
from django.contrib import messages

def home(request):
    """Homepage view"""
    return render(request, 'home.html')

@login_required
def upload_image(request):
    """Handle image upload and analysis"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = SkinAnalysis(
                user=request.user,
                image=request.FILES['image']
            )
            analysis.save()
            
            try:
                # Process the image (implement your analysis logic here)
                analysis.diagnosis = "Sample Diagnosis"  # Replace with actual analysis
                analysis.confidence_score = 0.85  # Replace with actual score
                analysis.recommendations = "Sample recommendations"  # Replace with actual recommendations
                analysis.save()
                
                messages.success(request, 'Image uploaded and analyzed successfully!')
                return redirect('skin_analysis:analysis', analysis_id=analysis.id)
            except Exception as e:
                messages.error(request, f'Error processing image: {str(e)}')
                return redirect('skin_analysis:upload')
    else:
        form = ImageUploadForm()
    
    return render(request, 'upload.html', {'form': form})

@login_required
def view_analysis(request, analysis_id):
    """View analysis results"""
    analysis = get_object_or_404(SkinAnalysis, id=analysis_id, user=request.user)
    
    # Convert confidence score to percentage (0-100 range)
    confidence_percentage = analysis.confidence_score * 100 if analysis.confidence_score <= 1 else analysis.confidence_score
    
    context = {
        'analysis': analysis,
        'severity': 'High' if confidence_percentage > 80 else 'Medium',
        'recommendations': analysis.recommendations.split('\n') if analysis.recommendations else [],
    }
    
    # Update the confidence score to percentage
    analysis.confidence_score = confidence_percentage
    
    return render(request, 'analysis.html', context)

@login_required
def analysis_history(request):
    """View user's analysis history"""
    analyses = SkinAnalysis.objects.filter(user=request.user).order_by('-upload_date')
    return render(request, 'history.html', {'analyses': analyses})
