from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from .load_model import emotion_model  # Model yükleme dosyanız
import numpy as np
from PIL import Image
import io
from rest_framework.views import APIView
from rest_framework.response import Response

def image_upload_and_analyze(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            image_file = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            uploaded_file_url = fs.url(filename)

            # Resmi aç ve işle
            image = Image.open(image_file)
            image = image.resize((48, 48))  # Örnek olarak modelin beklediği boyuta getir
            image = image.convert('L')  # Gri skalaya dönüştür
            image_array = np.array(image)
            image_array = image_array / 255.0  # Normalizasyon
            image_array = image_array.reshape(1, 48, 48, 1)  # Modelin beklediği şekle getir

            # Modeli kullanarak analiz yap
            predictions = emotion_model.predict(image_array)
            emotion_index = np.argmax(predictions)
            emotions = ['Kızgın', 'Nefret', 'Korku', 'Mutlu', 'Üzgün', 'Şaşırmış', 'Normal']  # Duygu etiketleri
            predicted_emotion = emotions[emotion_index]

            return render(request, 'analysis_result.html', {
                'uploaded_file_url': uploaded_file_url,
                'predicted_emotion': predicted_emotion
            })

    else:
        form = ImageUploadForm()
    return render(request, 'home.html', {'form': form})
