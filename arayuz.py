import streamlit as st
import time
import os
import pandas as pd
import altair as alt

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="SkyVision AI",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MODERN CSS STİLİ (Mavi/Gökyüzü Teması) ---
st.markdown("""
<style>
    /* Genel Arkaplan Ayarları */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Kart Görünümü (Containerlar için) */
    .css-card {
        background-color: #262730;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    /* Başlık Stili */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #ffffff;
    }
    
    /* Özel Buton Stili - Mavi Gradient */
    div.stButton > button {
        background: linear-gradient(45deg, #2563EB, #06B6D4); /* Mavi - Turkuaz */
        color: white;
        border: none;
        border-radius: 10px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
    }
    
    /* Sidebar Düzenlemesi */
    section[data-testid="stSidebar"] {
        background-color: #1c1e24;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MODEL YÜKLEME FONKSİYONU ---
@st.cache_resource
def load_model_pipeline():
    # Placeholderlar
    loading_container = st.empty()
    
    with loading_container.container():
        st.info("Meteoroloji modülleri yükleniyor, lütfen bekleyiniz...")
        progress_bar = st.progress(0)
    
    # Lazy Import
    import torch
    from transformers import ViTImageProcessor, ViTForImageClassification
    
    progress_bar.progress(20)
    time.sleep(0.1)
    
    # --- DİKKAT: MODEL YOLUNU GÜNCELLEYİN ---
    # Hava durumu verisiyle eğitilmiş modelin klasör yolu buraya gelmeli.
    MODEL_YOLU = r"C:\Users\dila\Desktop\220501022_Bulut_Bilisim\model_dila" 
    
    if not os.path.exists(MODEL_YOLU):
        loading_container.empty()
        return None, None, None, None, f"Klasör Bulunamadı: {MODEL_YOLU}"

    try:
        progress_bar.progress(50)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Model Yükleme
        model = ViTForImageClassification.from_pretrained(MODEL_YOLU)
        processor = ViTImageProcessor.from_pretrained(MODEL_YOLU)
        model.to(device)
        
        progress_bar.progress(100)
        time.sleep(0.5)
        loading_container.empty() # Yükleme ekranını temizle
        
        return model, processor, device, torch, "Başarılı"
        
    except Exception as e:
        loading_container.empty()
        return None, None, None, None, str(e)

# --- 4. YÜKLEME VE BAŞLATMA ---
model, processor, device, torch, status_msg = load_model_pipeline()

# --- 5. HATA KONTROLÜ ---
if model is None:
    st.error(f"🚨 KRİTİK HATA: Model Yüklenemedi!\nSebep: {status_msg}")
    st.stop()

# --- YAN MENÜ ---
with st.sidebar:
    # Hava durumu ikonu
    st.image("https://img.icons8.com/fluency/96/partly-cloudy-day.png", width=80)
    st.title("SkyVision AI")
    st.caption("v2.1.0 | Weather Edition")
    
    st.markdown("---")
    
    with st.expander("ℹ️ Sistem Durumu", expanded=True):
        st.success("✅ Model Yüklendi")
        st.info(f"⚙️ İşlemci: {device.upper()}")
        st.warning(f"📂 Mod: Hava Tahmini")
    
    st.markdown("### 🛠️ Ayarlar")
    confidence_threshold = st.slider("Hassasiyet Eşiği (%)", 0, 100, 20)
    
    st.markdown("---")
    st.markdown("Geliştirici:")
    st.markdown("👩‍💻 **Dila Seray Tegün**")

# --- ANA EKRAN TASARIMI ---

# Header Kısmı
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("Yapay Zeka Hava Durumu Analizi")
    st.markdown("##### 🌦️ Fotoğrafı yükleyin, yapay zeka gökyüzünü analiz ederek hava durumunu tahmin etsin.")
with col_h2:
    pass

st.markdown("---")

# İki Kolonlu Yapı
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("📤 Görsel Yükleme")
    
    uploaded_file = st.file_uploader(
        "Manzara veya Gökyüzü Fotoğrafı Seçiniz", 
        type=["jpg", "jpeg", "png"], 
        label_visibility="visible"
    )
    
    if uploaded_file is not None:
        from PIL import Image
        image = Image.open(uploaded_file).convert("RGB")
        st.markdown("### Önizleme")
        st.image(image, caption='Analiz Edilecek Görüntü', use_container_width=True, channels="RGB")
        st.success("Görsel başarıyla işlendi.")
    else:
        # Boşken gösterilecek alan
        st.info("Başlamak için bir manzara veya gökyüzü fotoğrafı yükleyin.")
        st.image("https://cdn-icons-png.flaticon.com/512/1163/1163624.png", width=100)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("🌤️ Analiz Paneli")
    
    if uploaded_file is not None:
        if st.button("🚀 Atmosferi Tara", use_container_width=True):
            
            with st.spinner('Bulutlar taranıyor, ışık değerleri ölçülüyor...'):
                # Simüle edilmiş bekleme
                time.sleep(1)
                
                # TAHMİN İŞLEMİ
                inputs = processor(images=image, return_tensors="pt").to(device)
                
                with torch.no_grad():
                    outputs = model(**inputs)
                    logits = outputs.logits
                
                # Olasılıklar
                probs = torch.nn.functional.softmax(logits, dim=-1)
                
                # Model sınıf sayısına göre Top-K belirleme (max 5)
                k = min(5, len(model.config.id2label))
                top_k_prob, top_k_idx = torch.topk(probs, k)
                
                # EN İYİ TAHMİNİ AL
                best_label = model.config.id2label[top_k_idx[0][0].item()]
                best_score = top_k_prob[0][0].item()

            # Sonuç Gösterimi
            st.toast("Analiz Tamamlandı!", icon="✨")
            
            # Ana Metrik Kartı (Mavi/Turkuaz Tema)
            st.markdown(f"""
            <div style="background-color: #1F2937; padding: 15px; border-radius: 10px; border-left: 5px solid #06B6D4;">
                <h3 style="margin:0; color: #9CA3AF;">Tespit Edilen Hava:</h3>
                <h1 style="margin:0; color: #06B6D4; font-size: 36px;">{best_label}</h1>
                <p style="margin:0; font-size: 16px; color: white;">Güven Skoru: <b>%{best_score*100:.1f}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- MODERN GRAFİK (ALTAIR) ---
            st.markdown("#### 📊 Olasılık Dağılımı")
            
            # Veriyi Hazırla
            data = []
            for i in range(k):
                score = top_k_prob[0][i].item()
                label_name = model.config.id2label[top_k_idx[0][i].item()]
                data.append({"Hava Durumu": label_name, "Olasılık": score})
            
            df_chart = pd.DataFrame(data)
            
            # Grafik Çizimi
            chart = alt.Chart(df_chart).mark_bar(cornerRadiusTopRight=10, cornerRadiusBottomRight=10).encode(
                x=alt.X('Olasılık', axis=alt.Axis(format='%', title='Güven Oranı')),
                y=alt.Y('Hava Durumu', sort='-x', title='Sınıf'),
                color=alt.condition(
                    alt.datum.Olasılık == best_score,
                    alt.value('#06B6D4'),  # En yüksek skor Turkuaz
                    alt.value('#374151')   # Diğerleri gri
                ),
                tooltip=['Hava Durumu', alt.Tooltip('Olasılık', format='.1%')]
            ).properties(height=300)
            
            st.altair_chart(chart, use_container_width=True)

    else:
        st.warning("👈 Analiz sonuçlarını görmek için lütfen sol taraftan bir resim yükleyiniz.")
        st.markdown("""
        **Nasıl Çalışır?**
        1. Dışarıdan çektiğiniz bir fotoğrafı yükleyin.
        2. 'Atmosferi Tara' butonuna basın.
        3. Yapay zeka (Yağmurlu, Güneşli, Bulutlu vb.) tahmini yapsın.
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)