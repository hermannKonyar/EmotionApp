from tensorflow.keras.models import load_model

def load_emotion_model():
    model = load_model('/Users/hermann/Desktop/projelerim/Python/DeepLearning/EmotionApp/Analysis/models/emotion_model.h5')
    return model

# Modeli yükle
emotion_model = load_emotion_model()
