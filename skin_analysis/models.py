from django.db import models
from django.contrib.auth.models import User

class SkinDisease(models.Model):
    """Database of known skin diseases"""
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='trained_images/')
    description = models.TextField()
    symptoms = models.TextField()
    severity_level = models.CharField(max_length=20, 
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    recommended_actions = models.TextField()
    prevention_tips = models.TextField()
    emergency_symptoms = models.TextField()
    treatment_options = models.TextField()
    
    def __str__(self):
        return self.name
    

class SkinAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='skin_images/')
    upload_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField(null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)

    # Analysis results
    detected_disease = models.ForeignKey(SkinDisease, on_delete=models.SET_NULL, null=True)
    confidence_score = models.FloatField(null=True)
    analysis_notes = models.TextField(blank=True)
    
    # Follow-up
    requires_immediate_attention = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    doctor_consultation_recommended = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Analysis for {self.user.username} on {self.upload_date}"