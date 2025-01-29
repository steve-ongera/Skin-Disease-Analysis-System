# Skin Disease Analysis System

![Alt text](https://github.com/steve-ongera/Skin-Disease-Analysis-System/blob/main/screenshot.PNG)


## Overview
A Django-based web application that uses machine learning to analyze skin conditions and provide preliminary medical insights. The system helps users identify potential skin conditions and offers recommendations while emphasizing the importance of professional medical consultation.

## Features
- 🔒 Secure user authentication and data privacy
- 📸 Image upload and analysis
- 🤖 AI-powered skin condition detection
- 📊 Confidence scoring and severity assessment
- 📋 Detailed recommendations and prevention tips
- 📆 Analysis history tracking
- 🏥 Emergency symptom alerts
- 👨‍⚕️ Professional consultation recommendations

## Technologies Used
- Python 3.8+
- Django 5.1+
- TensorFlow 2.x
- Bootstrap 5
- SQLite/PostgreSQL
- Pillow (Python Imaging Library)

## Installation

### Prerequisites
```bash
# Install Python 3.8 or higher
python --version

# Install pip (Python package manager)
pip --version
```

### Setup Steps
1. Clone the repository:
```bash
git clone https://github.com/yourusername/skin-disease-analysis.git
cd skin-disease-analysis
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

5. Initialize the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Load initial disease data:
```bash
python manage.py loaddata diseases
```

8. Run the development server:
```bash
python manage.py runserver
```

## Project Structure
```
skin_disease_analysis/
├── manage.py
├── requirements.txt
├── .env
├── README.md
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
│   └── skin_images/
├── ml_models/
│   └── skin_disease_model.h5
├── training_data/
│   ├── melanoma/
│   ├── eczema/
│   └── ...
└── skin_analysis/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── ml_model.py
    └── templates/
        └── skin_analysis/
            ├── base.html
            ├── home.html
            ├── upload.html
            ├── analysis.html
            └── history.html
```

## Machine Learning Model

### Training the Model
1. Prepare your training data:
```bash
training_data/
├── disease_1/
│   ├── image1.jpg
│   ├── image2.jpg
├── disease_2/
│   ├── image1.jpg
│   └── image2.jpg
```

2. Run the training script:
```bash
python manage.py train_model
```

### Model Architecture
- Input layer: 224x224x3
- Convolutional layers with max pooling
- Dense layers for classification
- Output: Disease probabilities

## Usage

### User Registration
1. Navigate to `/register`
2. Create an account with email verification
3. Log in to access the system

### Analyzing Skin Conditions
1. Click "Upload Image" on the dashboard
2. Select a clear image of the skin condition
3. Wait for analysis results
4. Review recommendations and severity assessment

### Viewing History
1. Navigate to "History" in the dashboard
2. View all previous analyses
3. Track condition changes over time

## Security Features
- Secure image upload handling
- User data encryption
- Session management
- CSRF protection
- XSS prevention
- Secure password handling

## API Documentation
The system provides REST APIs for:
- Image upload
- Analysis retrieval
- History access

### Example API Usage
```python
import requests

# Upload image for analysis
response = requests.post(
    'api/analyze',
    files={'image': open('skin_image.jpg', 'rb')},
    headers={'Authorization': 'Token your_auth_token'}
)
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Testing
Run the test suite:
```bash
python manage.py test
```

## Deployment
### Production Settings
1. Set DEBUG=False
2. Configure production database
3. Set up static file serving
4. Configure email backend
5. Set up SSL certificate

### Server Requirements
- 2GB RAM minimum
- 10GB storage
- SSL certificate
- PostgreSQL database

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This application is not a substitute for professional medical advice. Always consult healthcare professionals for medical decisions.

## Support
For support, email: steveongera001@gmail.com

## Acknowledgments
- TensorFlow team
- Django community
- Medical professionals who provided guidance