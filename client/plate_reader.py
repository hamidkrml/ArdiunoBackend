"""
Otopark AI İstemcisi - Pro Versiyon
Görüntü İşleme + Plaka Tanıma + Backend Entegrasyonu
"""

import cv2
import numpy as np
import easyocr
import requests
import time

# ================= AYARLAR =================
# Docker üzerindeki backend adresimiz (Mac'te 5005 portu)
BACKEND_URL = "http://127.0.0.1:5005/check_access"

# TEST İÇİN: Kendi kameranı (Webcam) kullanmak için 0 yap
# GERÇEK KULLANIMDA: ESP32-CAM adresini yaz (Örn: "http://192.168.4.1:81/stream")
STREAM_URL = 0 

# OCR motoru (Sadece rakamlar ve İngilizce harfler için optimize)
print("🧠 OCR Motoru başlatılıyor (Lütfen bekleyin)...")
reader = easyocr.Reader(['en'], gpu=False)

# ================= GÖRÜNTÜ İŞLEME =================
def get_plate_region(frame):
    """
    Görüntüdeki plaka olabilecek dikdörtgen bölgeleri bulur (Localization)
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Gürültü temizleme ve kenar bulma
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(bfilter, 30, 200)
    
    # Kontürleri bul
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(keypoints[0], key=cv2.contourArea, reverse=True)[:10]
    
    location = None
    for contour in contours:
        # Dikdörtgen formuna yakınlık kontrolü
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    
    return location

def preprocess_plate(plate_img):
    """
    Plaka bölgesini OCR için optimize eder
    """
    if plate_img is None or plate_img.size == 0:
        return None
        
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    
    # Adaptive threshold ile ışık patlamalarını engelle (AirPlay/Güneş ışığı çözümü)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    return thresh

# ================= ANA DÖNGÜ =================
def start_recognition():
    print("✅ Sistem Hazır. Kameraya bağlanılıyor...")
    # Not: Eğer STREAM_URL çalışmazsa burayı 0 (webcam) yapabilirsin.
    cap = cv2.VideoCapture(STREAM_URL) 
    
    last_request_time = 0
    cooldown = 3 # Aynı plakayı 3 saniyede bir sor
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Görüntü koptu, yeniden bağlanılıyor...")
            time.sleep(2)
            cap = cv2.VideoCapture(STREAM_URL)
            continue

        # Ekranı küçült (işleme hızı için)
        frame = cv2.resize(frame, (800, 600))
        display_frame = frame.copy()

        # 1. Plaka bölgesini bul
        location = get_plate_region(frame)
        
        if location is not None:
            # Plaka çevresine çizgi çek
            cv2.drawContours(display_frame, [location], -1, (0, 255, 0), 2)
            
            # 2. Plakayı kes (Crop)
            mask = np.zeros(frame.shape[:2], np.uint8)
            cv2.drawContours(mask, [location], 0, 255, -1)
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            cropped_plate = frame[topx:bottomx+1, topy:bottomy+1]
            
            # 3. OCR tara
            processed_plate = preprocess_plate(cropped_plate)
            
            # Her 30 karede bir veya 's' tuşuna basınca backend'e sor
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s') or (time.time() - last_request_time > cooldown):
                
                results = reader.readtext(processed_plate, detail=0)
                
                if results:
                    plate_text = "".join(results).replace(" ", "").upper()
                    print(f"🔍 Okunan Plaka: {plate_text}")
                    
                    # 4. BACKEND ENTEGRASYONU
                    try:
                        response = requests.get(
                            BACKEND_URL, 
                            params={"card_id": plate_text},
                            timeout=2
                        )
                        data = response.json()
                        
                        if data.get("access"):
                            color = (0, 255, 0) # Yeşil
                            msg = f"GECIS ONAYLANDI: {data.get('user_name')}"
                        else:
                            color = (0, 0, 255) # Kırmızı
                            msg = f"YETKISIZ: {plate_text}"
                            
                        last_request_time = time.time()
                        
                        # Ekrana sonucu yaz
                        cv2.putText(display_frame, msg, (20, 50), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                        print(f"📡 Backend Yanıtı: {msg}")
                        
                    except Exception as e:
                        print(f"❌ Backend Bağlantı Hatası: {e}")

        cv2.imshow("Otopark AI Kontrol Paneli", display_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_recognition()
