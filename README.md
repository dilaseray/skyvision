# ⛅ SkyVision AI — Gelişmiş Hava Durumu Tespit Sistemi

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C)
![Model](https://img.shields.io/badge/Model-ViT--Base-yellow)
![Status](https://img.shields.io/badge/Status-Completed-success)

**SkyVision AI**, **Vision Transformer (ViT)** mimarisini kullanarak fotoğraflardan hava durumu tahmini yapan bir derin öğrenme projesidir. Streamlit arayüzü sayesinde görsel yükleyip saniyeler içinde sınıf tahmini ve olasılık dağılımını görebilirsin.

---

## 🚀 Proje Özeti

Bu proje; görüntü işleme + derin öğrenme ile **hava durumu olaylarını sınıflandırmayı** hedefler. Geleneksel CNN yerine **Google ViT** tabanlı `google/vit-base-patch16-224` modeli üzerinde **transfer learning (fine-tuning)** yaklaşımı uygulanmıştır.

### Öne Çıkanlar
- **⚡ Yüksek doğruluk:** Eğitim çıktısında **%99.80 accuracy** raporlanmıştır.
- **📊 11 sınıf:** Farklı hava durumu olaylarını ayırt eder.
- **📈 Görsel çıktı:** Streamlit arayüzünde olasılıkları grafiksel sunar.
- **☁️ Taşınabilir:** Yerel veya bulut ortamına uygundur.

---

## 🔗 Model ve Dataset

### ✅ Eğitilmiş Model (indir)
- Google Drive: **Eğitilmiş model linki**
  - https://drive.google.com/file/d/1ovE_C4R-S2Y94OwEhprlEZ8QsQU1VmdT/view?usp=sharing

> Model dosyalarını indirip proje içindeki `model_dila/` klasörüne yerleştirmen gerekir.

### ✅ Dataset (kaynak)
- Kaggle: **Weather Dataset**
  - https://www.kaggle.com/datasets/jehanbhathena/weather-dataset

---

## 🧠 Model Performansı

Eğitim boyunca **Validation Accuracy** ve **Loss** değişimi:

![Eğitim Sonuçları Grafiği](grafik.jpg)

- **Backbone:** `google/vit-base-patch16-224`
- **En yüksek başarı (Accuracy):** %99.80
- **Epoch:** 10

---

## 🏷️ Sınıflar (Labels)

Model aşağıdaki 11 sınıfı tanıyacak şekilde eğitilmiştir:

1. **Dew** (Çiy)  
2. **Fog/Smog** (Sis/Duman)  
3. **Frost** (Don)  
4. **Glaze** (Buzlanma)  
5. **Hail** (Dolu)  
6. **Lightning** (Yıldırım)  
7. **Rain** (Yağmur)  
8. **Rainbow** (Gökkuşağı)  
9. **Rime** (Kırağı)  
10. **Sandstorm** (Kum Fırtınası)  
11. **Snow** (Kar)

---

## 📂 Proje Yapısı

```text
SkyVision-AI/
├── model_dila/                    # Eğitilmiş model dosyaları (config.json, model.safetensors vb.)
├── arayuz.py                      # Streamlit web arayüzü
├── egitim_sonuclari_grafigi.png   # Eğitim/performans grafiği
├── requirements.txt               # Bağımlılıklar
└── README.md
