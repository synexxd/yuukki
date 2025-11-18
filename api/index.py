from flask import Flask, jsonify, render_template_string
import requests
from bs4 import BeautifulSoup
import random
import logging
import os
import json
from datetime import datetime

app = Flask(__name__)

# Loglama ayarı
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global değişken tarama sonuçları için
scan_results = {
    "last_scan": None,
    "discord_boxes": [],
    "total_scanned": 0,
    "scan_history": []
}

def get_random_words_from_tdk(count=25):
    """
    Günlük hayatta sık kullanılan Türkçe ve İngilizce kelimeler
    """
    try:
        # Günlük hayatta sık kullanılan Türkçe ve İngilizce kelimeler (Türkçe karakter YOK)
        common_words = [
            # Türkçe kelimeler (Türkçe karakter yok)
            "araba", "ev", "is", "okul", "sokak", "cadde", "park", "bahce", "oda", "mutfak",
            "banyo", "yatak", "masa", "sandalye", "kapı", "pencere", "perde", "halı", "lamba",
            "telefon", "bilgisayar", "tablet", "klavye", "fare", "ekran", "yazıcı", "kamera",
            "televizyon", "radyo", "muzik", "film", "dizi", "oyun", "kitap", "defter", "kalem",
            "canta", "ayakkabı", "elbise", "gomlek", "pantolon", "etek", "ceket", "mont", "kazak",
            "tisort", "sweatshirt", "ayak", "el", "bas", "yuz", "goz", "kulak", "burun", "agız",
            "sac", "dis", "dil", "boyun", "omuz", "kol", "bilek", "parmak", "gogus", "karın",
            "sırt", "kalca", "bacak", "diz", "ayak", "topuk", "tırnak", "cilt", "kan", "kemik",
            "kas", "beyin", "kalp", "akciger", "mide", "karaciger", "bobrek", "mesane", "bagırsak",
            "yemek", "su", "ekmek", "peynir", "zeytin", "yumurta", "sut", "yoğurt", "bal", "recel",
            "cay", "kahve", "meyve", "sebze", "et", "tavuk", "balık", "makarna", "pilav", "corba",
            "salata", "tatlı", "kek", "pasta", "dondurma", "cikolata", "bisküvi", "kraker", "cips",
            "mama", "bebek", "cocuk", "genc", "yetişkin", "yaşlı", "adam", "kadın", "erkek", "kız",
            "oglan", "anne", "baba", "kardes", "dede", "nene", "amca", "hala", "dayı", "teyze",
            "arkadas", "komşu", "is", "meslek", "doktor", "muhendis", "ogretmen", "ogrenci", "memur",
            "asker", "polis", "itfaiye", "suruçu", "avukat", "hakim", "savcı", "mimar", "ressam",
            "muzisyen", "yazar", "sair", "gazeteci", "sporcu", "futbol", "basketbol", "voleybol",
            "tenis", "yuzme", "kosu", "yuruyuş", "bisiklet", "araba", "otobus", "tren", "ucak",
            "gemi", "metro", "taksi", "tramvay", "durak", "istasyon", "liman", "havalimanı",
            "yol", "harita", "navigasyon", "trafik", "ısık", "kavşak", "köprü", "tünel", "otoyol",
            
            # İngilizce kelimeler
            "car", "home", "house", "work", "job", "school", "street", "road", "park", "garden",
            "room", "kitchen", "bathroom", "bed", "table", "chair", "door", "window", "curtain",
            "carpet", "lamp", "phone", "computer", "laptop", "tablet", "keyboard", "mouse", "screen",
            "printer", "camera", "tv", "television", "radio", "music", "movie", "series", "game",
            "book", "notebook", "pen", "pencil", "bag", "shoes", "clothes", "shirt", "pants",
            "skirt", "jacket", "coat", "sweater", "tshirt", "sweatshirt", "foot", "hand", "head",
            "face", "eye", "ear", "nose", "mouth", "hair", "tooth", "tongue", "neck", "shoulder",
            "arm", "wrist", "finger", "chest", "stomach", "back", "hip", "leg", "knee", "ankle",
            "heel", "nail", "skin", "blood", "bone", "muscle", "brain", "heart", "lung", "stomach",
            "liver", "kidney", "bladder", "intestine", "food", "water", "bread", "cheese", "olive",
            "egg", "milk", "yogurt", "honey", "jam", "tea", "coffee", "fruit", "vegetable", "meat",
            "chicken", "fish", "pasta", "rice", "soup", "salad", "dessert", "cake", "icecream",
            "chocolate", "cookie", "cracker", "chips", "baby", "child", "kid", "young", "adult",
            "old", "man", "woman", "male", "female", "boy", "girl", "mother", "father", "parent",
            "brother", "sister", "sibling", "grandfather", "grandmother", "uncle", "aunt", "friend",
            "neighbor", "work", "job", "profession", "doctor", "engineer", "teacher", "student",
            "officer", "soldier", "police", "firefighter", "driver", "lawyer", "judge", "architect",
            "artist", "painter", "musician", "writer", "poet", "journalist", "athlete", "sports",
            "football", "soccer", "basketball", "volleyball", "tennis", "swimming", "running",
            "walking", "bicycle", "bike", "bus", "train", "plane", "airplane", "ship", "boat",
            "subway", "taxi", "tram", "stop", "station", "port", "airport", "road", "street",
            "map", "navigation", "traffic", "light", "intersection", "bridge", "tunnel", "highway",
            
            # Teknoloji kelimeleri
            "tech", "code", "web", "internet", "network", "wifi", "data", "cloud", "server",
            "client", "app", "application", "software", "hardware", "device", "gadget", "digital",
            "online", "offline", "website", "blog", "social", "media", "email", "message", "chat",
            "video", "audio", "image", "photo", "picture", "file", "folder", "document", "pdf",
            "word", "excel", "powerpoint", "windows", "mac", "linux", "android", "ios", "apple",
            "google", "microsoft", "amazon", "facebook", "instagram", "twitter", "youtube",
            "whatsapp", "telegram", "discord", "zoom", "skype", "meet", "team", "work", "office",
            
            # Renkler
            "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black",
            "white", "gray", "silver", "gold", "color", "colour", "dark", "light", "bright",
            
            # Sayılar
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "first", "second", "third", "fourth", "fifth", "number", "count", "digital",
            
            # Zaman ve mevsimler
            "time", "day", "night", "morning", "evening", "afternoon", "week", "month", "year",
            "today", "tomorrow", "yesterday", "now", "later", "soon", "early", "late", "fast",
            "slow", "quick", "minute", "hour", "second", "clock", "watch", "calendar", "date",
            "spring", "summer", "autumn", "fall", "winter", "season", "weather", "sun", "rain",
            "snow", "wind", "cloud", "storm", "hot", "cold", "warm", "cool", "dry", "wet",
            
            # Duygular
            "happy", "sad", "angry", "excited", "bored", "tired", "sleepy", "hungry", "thirsty",
            "love", "like", "hate", "want", "need", "hope", "fear", "worry", "think", "feel",
            
            # Eylemler
            "go", "come", "run", "walk", "jump", "swim", "eat", "drink", "sleep", "wake",
            "work", "play", "study", "read", "write", "speak", "talk", "listen", "watch",
            "see", "look", "find", "search", "buy", "sell", "give", "take", "make", "create",
            "build", "break", "fix", "clean", "wash", "cook", "drive", "fly", "travel", "visit"
        ]
        
        # Türkçe karakter kontrolü yap ve filtrele
        filtered_words = []
        for word in common_words:
            # Türkçe karakter kontrolü (ı, İ, ğ, Ğ, ü, Ü, ş, Ş, ö, Ö, ç, Ç)
            if not any(char in word for char in ['ı', 'İ', 'ğ', 'Ğ', 'ü', 'Ü', 'ş', 'Ş', 'ö', 'Ö', 'ç', 'Ç']):
                filtered_words.append(word)
        
        # Benzersiz kelimeler
        unique_words = list(set(filtered_words))
        
        # Rastgele kelimeler seç
        selected_words = random.sample(unique_words, min(count, len(unique_words)))
        logger.info(f"Seçilen {len(selected_words)} kelime: {selected_words}")
        return selected_words
        
    except Exception as e:
        logger.error(f"Kelimeler alınırken hata: {str(e)}")
        # Fallback kelimeler
        return ["test", "demo", "example", "sample", "temp", "random", "check", "mail", "discord", "verify"]

def check_discord_mail(box_name):
    """
    Yopmail'de Discord maili kontrol eder
    """
    try:
        url = f"https://yopmail.com/en/inbox.php?login={box_name}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        # Session oluştur
        session = requests.Session()
        session.headers.update(headers)
        
        # İstek yap
        response = session.get(url, timeout=15)
        
        if response.status_code != 200:
            return {"status": "error", "message": f"Yopmail'e erişilemedi: {response.status_code}"}

        soup = BeautifulSoup(response.content, 'html.parser')

        # Mail konularını bul
        mail_subjects = []
        
        # Farklı selector denemeleri
        selectors = [
            'div.lm', 'div.m', 'span.lm', 'span.m',
            '.lm', '.m', '[class*="lm"]', '[class*="m"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 2 and text not in mail_subjects:
                    mail_subjects.append(text)
        
        if not mail_subjects:
            return {
                "status": "no_emails", 
                "message": "Gelen kutusunda hiç mail yok veya mail bulunamadı.",
                "box_name": box_name
            }

        # Discord maillerini ara
        discord_keywords = ['discord', 'verify', 'confirmation', 'activation', 'code', 'security', 'login', 'account']
        discord_mails = []
        
        for subject in mail_subjects:
            subject_lower = subject.lower()
            if any(keyword in subject_lower for keyword in discord_keywords):
                discord_mails.append(subject)

        result = {
            "status": "success",
            "box_name": box_name,
            "total_emails": len(mail_subjects),
            "discord_emails": discord_mails,
            "has_discord": len(discord_mails) > 0,
            "all_emails": mail_subjects[:5],  # İlk 5 maili göster
            "yopmail_url": f"https://yopmail.com/en/inbox.php?login={box_name}"
        }
        
        return result

    except requests.RequestException as e:
        return {"status": "error", "message": f"Bağlantı hatası: {str(e)}", "box_name": box_name}
    except Exception as e:
        return {"status": "error", "message": f"Beklenmeyen hata: {str(e)}", "box_name": box_name}

# HTML Template (Aynı kalacak, yukarıdaki template'i kullan)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Mail Scanner</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #5865F2, #7289DA);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .discord-box {
            background: #edf2ff;
            border-left: 4px solid #5865F2;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .no-discord {
            background: #f8f9fa;
            border-left: 4px solid #6c757d;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .btn {
            background: #5865F2;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }
        .btn:hover {
            background: #4752c4;
        }
        .btn-scan {
            background: #57F287;
            color: black;
        }
        .btn-scan:hover {
            background: #45d472;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .discord-count {
            background: #57F287;
            color: black;
        }
        .email-item {
            background: #f8f9fa;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid #5865F2;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .success { color: #57F287; }
        .error { color: #ED4245; }
        .warning { color: #FEE75C; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Discord Mail Scanner</h1>
        <p>Yopmail hesaplarında Discord kayıt maillerini tarar</p>
    </div>

    <div class="container">
        <h2>🔧 İşlemler</h2>
        <button class="btn btn-scan" onclick="startScan()">🚀 Tarama Başlat (25 Rastgele Kelime)</button>
        <button class="btn" onclick="location.reload()">🔄 Sayfayı Yenile</button>
        
        <div id="loading" class="loading">
            <h3>⏳ Tarama devam ediyor...</h3>
            <p>Lütfen bekleyiniz. Bu işlem birkaç dakika sürebilir.</p>
        </div>
    </div>

    <div class="container">
        <h2>📊 İstatistikler</h2>
        <div class="stats">
            <div class="stat-card">
                <h3>Toplam Taranan</h3>
                <p style="font-size: 24px; font-weight: bold;">{{ total_scanned }}</p>
            </div>
            <div class="stat-card discord-count">
                <h3>Discord Bulunan</h3>
                <p style="font-size: 24px; font-weight: bold;">{{ discord_count }}</p>
            </div>
            <div class="stat-card">
                <h3>Son Tarama</h3>
                <p style="font-size: 16px;">{{ last_scan }}</p>
            </div>
        </div>
    </div>

    <div class="container">
        <h2>🎯 Discord Bulunan Hesaplar</h2>
        {% if discord_boxes %}
            {% for box in discord_boxes %}
            <div class="discord-box">
                <h3>📧 {{ box.box_name }}@yopmail.com</h3>
                <p><strong>Toplam Mail:</strong> {{ box.total_emails }}</p>
                <p><strong>Discord Mailleri:</strong></p>
                {% for email in box.discord_emails %}
                    <div class="email-item">{{ email }}</div>
                {% endfor %}
                <p><a href="{{ box.yopmail_url }}" target="_blank">🔗 Yopmail'de Görüntüle</a></p>
                <small>Bulunma Zamanı: {{ box.found_time }}</small>
            </div>
            {% endfor %}
        {% else %}
            <p>Henüz Discord maili bulunamadı. Tarama başlatın!</p>
        {% endif %}
    </div>

    <div class="container">
        <h2>📝 Son Tarama Detayları</h2>
        {% if last_scan_details %}
            <p><strong>Tarama Zamanı:</strong> {{ last_scan_details.timestamp }}</p>
            <p><strong>Taranan Kelimeler:</strong> {{ last_scan_details.words|join(', ') }}</p>
            <p><strong>Sonuç:</strong> {{ last_scan_details.discord_found }} adet Discord maili bulundu</p>
        {% else %}
            <p>Henüz tarama yapılmadı.</p>
        {% endif %}
    </div>

    <script>
        function startScan() {
            document.getElementById('loading').style.display = 'block';
            
            fetch('/scan')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    location.reload();
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    alert('Tarama sırasında hata oluştu: ' + error);
                });
        }
        
        // 30 saniyede bir sayfayı yenile (opsiyonel)
        setInterval(() => {
            if (document.getElementById('loading').style.display === 'none') {
                location.reload();
            }
        }, 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Ana sayfa - HTML arayüz"""
    return render_template_string(HTML_TEMPLATE, 
        total_scanned=scan_results["total_scanned"],
        discord_count=len(scan_results["discord_boxes"]),
        last_scan=scan_results["last_scan"] or "Henüz tarama yapılmadı",
        discord_boxes=scan_results["discord_boxes"][-10:],  # Son 10 kayıt
        last_scan_details=scan_results["scan_history"][-1] if scan_results["scan_history"] else None
    )

@app.route('/check/<box_name>')
def check_single_box(box_name):
    """Belirli bir Yopmail kutusunu kontrol et"""
    result = check_discord_mail(box_name)
    
    # Discord bulunduysa global listeye ekle
    if result.get('has_discord'):
        discord_data = {
            'box_name': box_name,
            'discord_emails': result['discord_emails'],
            'total_emails': result['total_emails'],
            'yopmail_url': f"https://yopmail.com/en/inbox.php?login={box_name}",
            'found_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Aynı kutu zaten yoksa ekle
        if not any(box['box_name'] == box_name for box in scan_results["discord_boxes"]):
            scan_results["discord_boxes"].append(discord_data)
            scan_results["total_scanned"] += 1
        
        logger.info(f"🎯 DİSCORD BULUNDU: {box_name} - {result['discord_emails']}")
    
    return jsonify(result)

@app.route('/scan')
def scan_boxes():
    """Rastgele kelimelerle Yopmail kutularını tara"""
    try:
        # Rastgele kelimeler al
        words = get_random_words_from_tdk(25)
        results = []
        discord_found = []
        
        logger.info(f"🔍 {len(words)} kelime ile tarama başlatılıyor...")
        
        for word in words:
            # Her istek arasında kısa bekleme
            import time
            time.sleep(1)
            
            result = check_discord_mail(word)
            results.append(result)
            
            # Discord bulunduysa kaydet
            if result.get('has_discord'):
                discord_data = {
                    'box_name': word,
                    'discord_emails': result['discord_emails'],
                    'total_emails': result['total_emails'],
                    'yopmail_url': f"https://yopmail.com/en/inbox.php?login={word}",
                    'found_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Aynı kutu zaten yoksa ekle
                if not any(box['box_name'] == word for box in scan_results["discord_boxes"]):
                    scan_results["discord_boxes"].append(discord_data)
                    discord_found.append(discord_data)
                
                logger.info(f"🎯 DİSCORD BULUNDU: {word} - {result['discord_emails']}")
            
            scan_results["total_scanned"] += 1
        
        # Tarama geçmişini güncelle
        scan_history = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'words': words,
            'total_checked': len(words),
            'discord_found': len(discord_found),
            'discord_boxes': [box['box_name'] for box in discord_found]
        }
        scan_results["scan_history"].append(scan_history)
        scan_results["last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Sonuçları döndür
        response = {
            "scan_summary": {
                "total_checked": len(words),
                "discord_found_count": len(discord_found),
                "discord_boxes": discord_found,
                "checked_words": words
            },
            "detailed_results": results
        }
        
        # Discord bulunanları özel logla
        if discord_found:
            logger.info(f"🎯 TARAMA SONUCU: {len(discord_found)} kutuda Discord maili bulundu!")
            for found in discord_found:
                logger.info(f"   📧 {found['box_name']}: {found['discord_emails']}")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Tarama sırasında hata: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/results')
def get_results():
    """Sadece sonuçları JSON olarak döndür"""
    return jsonify(scan_results)

@app.route('/clear')
def clear_results():
    """Sonuçları temizle"""
    scan_results["discord_boxes"] = []
    scan_results["total_scanned"] = 0
    scan_results["scan_history"] = []
    scan_results["last_scan"] = None
    return jsonify({"status": "success", "message": "Sonuçlar temizlendi"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)