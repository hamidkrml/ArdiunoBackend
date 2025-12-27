"""
Otopark AI İstemcisi - V4 Google Cloud Vision Versiyonu
- Google Cloud Vision: Dünyanın en iyi OCR sistemi.
- Threading: Arayüz kasmadan akıcı görüntü sağlar.
- Stability: Doğru okunan plakayı bekleyen oylama sistemi.
"""

import cv2
import numpy as np
import requests
import time
import threading
import base64
import json

# ================= AYARLAR =================
BACKEND_URL = "http://127.0.0.1:5005/check_access"
STREAM_URL = 0 
GOOGLE_API_KEY = "AIzaSyCLgBaPvV-fvxNYbw83NSE15N6c-Mz17hs"
GOOGLE_VISION_URL = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_API_KEY}"

# Global değişkenler
processing_lock = threading.Lock()
is_processing = False
last_result_msg = ""
last_result_color = (255, 255, 255)
found_plates = []

# ================= GOOGLE VISION OCR =================
def google_vision_ocr(image_np):
    """Görüntüyü Google Cloud Vision'a gönderir ve metni döner"""
    try:
        # Görüntüyü encode et (Base64)
        _, buffer = cv2.imencode('.jpg', image_np)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # İstek gövdesi
        request_body = {
            "requests": [
                {
                    "image": {"content": img_base64},
                    "features": [{"type": "TEXT_DETECTION"}]
                }
            ]
        }
        
        # Timeout süresini 10 yaptık (Bağlantı yavaşsa hata vermesin)
        response = requests.post(GOOGLE_VISION_URL, json=request_body, timeout=10)
        response.raise_for_status()
            
        res_json = response.json()
        
        # Annotations içinden metni çek
        if "responses" in res_json and res_json["responses"]:
            annotations = res_json["responses"][0].get("textAnnotations", [])
            if annotations:
                return annotations[0]["description"]
        return None
    except requests.exceptions.Timeout:
        print("🕒 Google Vision: Zaman aşımı! İnternet yavaş olabilir.")
        return "TIMEOUT"
    except requests.exceptions.ConnectionError:
        print("🌐 Google Vision: Bağlantı hatası! İnternet veya DNS sorunu.")
        return "CONN_ERR"
    except Exception as e:
        print(f"❌ Google Vision Hatası: {e}")
        return None

def clean_plate_text(text):
    """Sadece harf ve rakamları tutar ve temizler"""
    if not text or text in ["TIMEOUT", "CONN_ERR"]: return ""
    text = text.replace("\n", " ").upper()
    # Harf ve rakam dışındaki her şeyi sil
    clean = "".join([c for c in text if (c.isalnum() or c == ' ')])
    return clean.strip()

def ocr_thread_worker(roi_img):
    global is_processing, last_result_msg, last_result_color, found_plates
    
    try:
        raw_text = google_vision_ocr(roi_img)
        
        if raw_text:
            plate_text = clean_plate_text(raw_text)
            
            if len(plate_text) >= 4:
                found_plates.append(plate_text)
                if len(found_plates) > 5: found_plates.pop(0)
                
                # En çok tekrar eden plakayı bul
                most_common = max(set(found_plates), key=found_plates.count)
                frequency = found_plates.count(most_common)
                
                print(f"👀 Gözlenen (Google): {plate_text} -> Kararlı: {most_common} ({frequency}/2)")

                # Google çok güçlü olduğu için 2 kez görmesi yeterli
                if frequency >= 2:
                    print(f"🎯 KESİNLEŞTİ: {most_common}")
                    try:
                        resp = requests.get(BACKEND_URL, params={"card_id": most_common}, timeout=2)
                        data = resp.json()
                        if data.get("access"):
                            last_result_msg = f"GIRIS ONAYLI: {data.get('user_name')}"
                            last_result_color = (0, 255, 0)
                        else:
                            last_result_msg = f"RED: {most_common}"
                            last_result_color = (0, 0, 255)
                        found_plates = []
                    except:
                        last_result_msg = "BACKEND HATASI"
                        last_result_color = (0, 255, 255)
    except Exception as e:
        print(f"❌ Worker Hatası: {e}")
    finally:
        with processing_lock:
            is_processing = False

# ================= ANA DÖNGÜ =================
def start_recognition():
    global is_processing, last_result_msg, last_result_color
    
    print("✅ Google Vision Sistemi Hazır. Kamera açılıyor...")
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
        cv2.putText(display_frame, "GOOGLE VISION TEST", (rx, ry - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

        # Yeni işlem başlat
        with processing_lock:
            if not is_processing:
                roi = frame[ry:ry+rh, rx:rx+rw]
                is_processing = True
                threading.Thread(target=ocr_thread_worker, args=(roi,), daemon=True).start()

        # Sonucu ekranda göster
        if last_result_msg:
            cv2.rectangle(display_frame, (rx, ry + rh), (rx + rw, ry + rh + 50), (0,0,0), -1)
            cv2.putText(display_frame, last_result_msg, (rx + 10, ry + rh + 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, last_result_color, 2)

        if is_processing:
            cv2.circle(display_frame, (w-30, 30), 10, (0, 255, 255), -1)

        cv2.imshow("Otopark AI (Google Vision Mode)", display_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_recognition()
