from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SkinAnalysis
from .forms import ImageUploadForm
from django.contrib import messages

def home(request):
    """Homepage view"""
    return render(request, 'home.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SkinAnalysis, SkinDisease
from .forms import ImageUploadForm
from django.contrib import messages
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
from scipy.spatial.distance import cosine
import os

# Initialize ResNet model globally for feature extraction
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

def preprocess_image(img_path):
    """Preprocess image for the model"""
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def extract_features(img_path):
    """Extract features from image using ResNet50"""
    img = preprocess_image(img_path)
    features = model.predict(img)
    return features.flatten()

def compute_similarity(features1, features2):
    """Compute cosine similarity between two feature vectors"""
    return 1 - cosine(features1, features2)

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
                # Extract features from uploaded image
                uploaded_features = extract_features(analysis.image.path)
                
                # Compare with all trained images
                best_match = None
                highest_similarity = -1
                
                for skin_disease in SkinDisease.objects.all():
                    # Extract features from trained image
                    trained_features = extract_features(skin_disease.image.path)
                    
                    # Calculate similarity
                    similarity = compute_similarity(uploaded_features, trained_features)
                    
                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        best_match = skin_disease
                
                # Update analysis with results
                if best_match and highest_similarity > 0.7:  # Confidence threshold
                    analysis.detected_disease = best_match
                    analysis.confidence_score = highest_similarity
                    analysis.diagnosis = f"Detected possible {best_match.name}"
                    analysis.recommendations = (
                        f"Based on our analysis, your image shows characteristics similar to {best_match.name}.\n\n"
                        f"Recommended Actions:\n{best_match.recommended_actions}\n\n"
                        f"Prevention Tips:\n{best_match.prevention_tips}\n\n"
                        f"If you notice these emergency symptoms:\n{best_match.emergency_symptoms}\n"
                        f"Please seek immediate medical attention."
                    )
                    
                    # Set flags based on severity
                    if best_match.severity_level == 'High':
                        analysis.requires_immediate_attention = True
                        analysis.doctor_consultation_recommended = True
                    
                    analysis.analysis_notes = (
                        f"Match Confidence: {highest_similarity:.2%}\n"
                        f"Severity Level: {best_match.severity_level}\n"
                        f"Common Symptoms: {best_match.symptoms}\n"
                        f"Treatment Options: {best_match.treatment_options}"
                    )
                else:
                    analysis.diagnosis = "No confident match found"
                    analysis.confidence_score = highest_similarity if highest_similarity > 0 else 0
                    analysis.recommendations = (
                        "Our system couldn't make a confident match with known conditions. "
                        "Please consult a healthcare professional for accurate diagnosis."
                    )
                    analysis.doctor_consultation_recommended = True
                
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
