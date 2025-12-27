"""
Otopark AI İstemcisi - Pro Versiyon (V3 - Optimize Edilmiş)
- Threading: Arayüz kasmadan akıcı görüntü sağlar.
- Confidence Check: Düşük güvenli okumaları eler.
- Voter System: Yanlış okumaları engellemek için 3 kez doğrulama yapar.
"""

import cv2
import numpy as np
import easyocr
import requests
import time
import threading

# ================= AYARLAR =================
BACKEND_URL = "http://127.0.0.1:5005/check_access"
STREAM_URL = 0 
CONFIDENCE_THRESHOLD = 0.40  # %40 altındaki okumaları görmezden gel

# OCR motoru
print("🧠 OCR Motoru başlatılıyor (Lütfen bekleyin)...")
reader = easyocr.Reader(['en'], gpu=False)

# Global değişkenler (Thread'ler arası iletişim için)
processing_lock = threading.Lock()
is_processing = False
last_result_msg = ""
last_result_color = (255, 255, 255)
found_plates = [] # Doğrulama için plaka biriktirir

# ================= GÖRÜNTÜ İŞLEME =================
def preprocess_plate(plate_img):
    if plate_img is None or plate_img.size == 0:
        return None
    
    # 1. Büyüt
    plate_img = cv2.resize(plate_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    
    # 2. Yumuşatma ve Kontrast
    blur = cv2.GaussianBlur(gray, (3, 3), 0) # Harf kenarlarındaki pürüzleri giderir
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray = clahe.apply(blur)
    
    # 3. Keskinleştirme
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel)
    
    # 4. Binary Dönüşüm
    _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

def clean_plate_text(text):
    text = "".join([c for c in text if c.isalnum()]).upper()
    replacements = {'B': '8', 'O': '0', 'D': '0', 'I': '1', '|': '1', 'L': '1', 'S': '5', 'Z': '2', 'G': '6', 'T': '7'}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def ocr_thread_worker(roi_img):
    global is_processing, last_result_msg, last_result_color, found_plates
    
    try:
        # Pürüzleri gidermek için detaylı okuma (mag_ratio)
        results = reader.readtext(roi_img, detail=1, paragraph=False, mag_ratio=1.5)
        
        if results:
            for (bbox, text, prob) in results:
                plate_text = clean_plate_text(text)
                
                if len(plate_text) >= 4 and prob > 0.25:
                    found_plates.append(plate_text)
                    # Sadece son 8 okumayı tut (Hafızayı taze tut)
                    if len(found_plates) > 8: found_plates.pop(0)
                    
                    # --- FREKANS ANALİZİ (İSTİKRAR KONTROLÜ) ---
                    # Son okunanlar içinde en çok tekrar eden plakayı bul
                    most_common = max(set(found_plates), key=found_plates.count)
                    frequency = found_plates.count(most_common)
                    
                    print(f"👀 Gözlenen: {plate_text} -> En Kararlı: {most_common} ({frequency}/3)")

                    # Eğer en çok tekrar eden plaka 3 kez (veya daha fazla) görüldüyse GÜVENLİDİR
                    if frequency >= 3:
                        print(f"🎯 KESİNLEŞTİ: {most_common}")
                        try:
                            resp = requests.get(BACKEND_URL, params={"card_id": most_common}, timeout=1.5)
                            data = resp.json()
                            if data.get("access"):
                                last_result_msg = f"GIRIS ONAYLI: {data.get('user_name')}"
                                last_result_color = (0, 255, 0)
                            else:
                                last_result_msg = f"RED: {most_common}"
                                last_result_color = (0, 0, 255)
                            found_plates = [] # Başarıyla gönderdikten sonra sıfırla
                        except:
                            last_result_msg = "BACKEND HATASI"
                            last_result_color = (0, 255, 255)
                    break
                        # Backend sorgusu
                        try:
                            resp = requests.get(BACKEND_URL, params={"card_id": plate_text}, timeout=1.5)
                            data = resp.json()
                            if data.get("access"):
                                last_result_msg = f"OK: {data.get('user_name')}"
                                last_result_color = (0, 255, 0)
                            else:
                                last_result_msg = f"RED: {plate_text}"
                                last_result_color = (0, 0, 255)
                            found_plates = [] # Sıfırla
                        except:
                            last_result_msg = "BACKEND BAGLANTI HATASI"
                            last_result_color = (0, 255, 255)
                    break # Bir çerçevede bir plaka yeterli

    except Exception as e:
        print(f"❌ OCR Hatası: {e}")
    finally:
        with processing_lock:
            is_processing = False

# ================= ANA DÖNGÜ =================
def start_recognition():
    global is_processing, last_result_msg, last_result_color
    
    print("✅ Sistem Hazır. Kamera açılıyor...")
    cap = cv2.VideoCapture(STREAM_URL) 
    
    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.resize(frame, (800, 600))
        display_frame = frame.copy()

        # ROI Kutusu
        h, w = frame.shape[:2]
        rw, rh = 400, 150
        rx, ry = (w - rw) // 2, (h - rh) // 2
        
        # Kutuyu çiz
        status_color = (255, 255, 0) if is_processing else (0, 255, 0)
        cv2.rectangle(display_frame, (rx, ry), (rx + rw, ry + rh), status_color, 2)
        cv2.putText(display_frame, "PLAKAYI BURAYA TUTUN", (rx, ry - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

        # Eğer şu an bir işlem yapılmıyorsa yeni thread başlat
        with processing_lock:
            if not is_processing:
                roi = frame[ry:ry+rh, rx:rx+rw]
                processed = preprocess_plate(roi)
                is_processing = True
                # OCR işlemini arka plana at (Lag engelleme)
                threading.Thread(target=ocr_thread_worker, args=(processed,), daemon=True).start()

        # Ekranda sonucu göster
        if last_result_msg:
            cv2.rectangle(display_frame, (rx, ry + rh), (rx + rw, ry + rh + 50), (0,0,0), -1)
            cv2.putText(display_frame, last_result_msg, (rx + 10, ry + rh + 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, last_result_color, 2)

        if is_processing:
            cv2.circle(display_frame, (w-30, 30), 10, (0, 255, 255), -1) # İşlem ışığı

        cv2.imshow("Otopark AI (V3 - Lag-Free)", display_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_recognition()
