import os
import numpy as np
import pickle
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from django.shortcuts import render


# Load model and tokenizer once when server starts
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = load_model(os.path.join(BASE_DIR, 'sentiment/ml_model/sentiment_model.h5'))

with open(os.path.join(BASE_DIR, 'sentiment/ml_model/tokenizer.pkl'), 'rb') as f:
    tokenizer = pickle.load(f)

# Define your label list as per training
labels = ['Positive', 'Neutral', 'Negative']  # Update based on your model output
def index(request):
    return render(request, 'sentiment/index.html')

@csrf_exempt
def predict_sentiment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('headline', '')

            if not message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Preprocess input
            seq = tokenizer.texts_to_sequences([message])
            padded = pad_sequences(seq, maxlen=100, dtype='int32', value=0) # Use the same maxlen as during training

            # Predict
            print("MESAGE : ",message)
            prediction = model.predict(padded)
            print("Predicted : ", prediction)
            predicted_label = labels[np.argmax(prediction)]
            confidence = float(np.max(prediction))

            return JsonResponse({
                'sentiment': predicted_label,
                'confidence': round(confidence, 4)
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'POST request required'}, status=405)