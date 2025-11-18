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

def get_random_words_from_tdk(count=20):
    """
    Türkçe karakter içermeyen random kelimeler
    """
    try:
        # Türkçe karakter İÇERMEYEN kelimeler
        tdk_words = [
            "araba", "bilgisayar", "kitap", "defter", "kalem", "masa", "sandalye", 
            "pencere", "kapi", "ev", "bahce", "agac", "cicek", "hayvan", "kus", 
            "kedi", "kopek", "balik", "yemek", "su", "hava", "toprak", "tas", 
            "demir", "altin", "gumus", "bakir", "kagit", "cam", "plastik", 
            "dergi", "gazete", "televizyon", "radyo", "telefon", "internet", 
            "program", "yazilim", "donanim", "sistem", "ag", "sunucu", "veri", 
            "bilgi", "haber", "mesaj", "mektup", "paket", "kutu", "canta", 
            "ayakkabi", "elbise", "sapka", "eldiven", "atki", "mont", "ceket", 
            "pantolon", "etek", "gomlek", "tisort", "kazak", "hirka", "bermuda", 
            "corap", "iclik", "mayo", "bikini", "sutyen", "kulot", "pijama", 
            "terlik", "sandalet", "bot", "cizme", "spor", "kosu", "yuruyus", 
            "yuzme", "futbol", "basketbol", "voleybol", "tenis", "yuzme", 
            "jimnastik", "boks", "gures", "judo", "karate", "taekwondo", "aikido", 
            "yoga", "pilates", "meditasyon", "nehir", "gol", "deniz", "okyanus", 
            "ada", "yarimada", "kita", "dag", "tepe", "vadi", "ova", "plato", 
            "orman", "koru", "bahce", "tarla", "ciftlik", "koy", "kasaba", "sehir", 
            "ilce", "il", "bolge", "ulke", "kita", "dunya", "evren", "uzay", 
            "gezegen", "yildiz", "galaksi", "samanyolu", "andromeda", "uzayli",
            "mac", "sicak", "soguk", "isik", "karanlik", "ses", "muzik", "film", 
            "dizi", "oyun", "kart", "zar", "pul", "para", "bank", "kredi", 
            "hesap", "numara", "sifre", "guvenlik", "kilit", "anahtar", "kapi", 
            "pencere", "duvar", "tavan", "zemin", "hal", "perde", "lamba", 
            "sis", "bulut", "yagmur", "kar", "dolu", "firtina", "kasirga", 
            "deprem", "sel", "yangin", "kaza", "saglik", "hastane", "doktor", 
            "hemstre", "ilac", "tedavi", "ameliyat", "as", "bagisiklik", 
            "spor", "antrenman", "mac", "takim", "oyuncu", "saha", "stadyum", 
            "salon", "havuz", "deniz", "plaj", "kum", "tas", "kaya", "magara", 
            "orman", "agac", "yaprak", "dal", "koku", "meyve", "sebze", "et", 
            "sut", "yumurta", "ekmek", "peynir", "zeytin", "bal", "recel", 
            "cay", "kahve", "sut", "meyve", "sebze", "makarna", "pilav", "corba", 
            "salata", "tatli", "kek", "pasta", "borek", "pizza", "hamburger", 
            "sandvic", "tost", "salata", "mez", "kebap", "lahmacun", "pide", 
            "baklava", "kadayif", "lokum", "helva", "sutlac", "kazandibi", 
            "komposto", "hos", "afiyet", "lezzet", "tuz", "seker", "biber", 
            "baharat", "yag", "sirke", "limon", "sarimsak", "sogan", "domates", 
            "biber", "patlican", "kabak", "havuc", "patates", "sogan", "marul", 
            "maydanoz", "tere", "roka", "nane", "fesle", "kimyon", "zerdecal", 
            "zencefil", "tarcin", "karanfil", "vanilya", "kakao", "cikolata", 
            "sekerleme", "sakiz", "cubuk", "kraker", "bisk", "cips", "patlak", 
            "misir", "findik", "ceviz", "badem", "fistik", "kayisi", "uzum", 
            "incir", "nar", "elma", "armut", "ayva", "muz", "portakal", "mandalina", 
            "limon", "greyfurt", "kivi", "ananas", "karpuz", "kavun", "cilek", 
            "visne", "kiraz", "erik", "seftali", "kayisi", "dut", "ahududu", 
            "bogurtlen", "mavi", "yesil", "kirmizi", "sari", "turuncu", "mor", 
            "pembe", "kahve", "siyah", "beyaz", "gri", "gumus", "altin", "bronz",
            "alpha", "beta", "gamma", "delta", "omega", "sigma", "lambda", "zeta",
            "tech", "code", "web", "net", "app", "soft", "hard", "data", "info",
            "cloud", "server", "client", "admin", "user", "guest", "test", "demo"
        ]
        
        # Türkçe karakter kontrolü yap ve filtrele
        filtered_words = []
        for word in tdk_words:
            if not any(char in word for char in ['ı', 'İ', 'ğ', 'Ğ', 'ü', 'Ü', 'ş', 'Ş', 'ö', 'Ö', 'ç', 'Ç']):
                filtered_words.append(word)
        
        # Rastgele kelimeler seç
        selected_words = random.sample(filtered_words, min(count, len(filtered_words)))
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
        discord_keywords = ['discord', 'verify', 'confirmation', 'activation', 'code', 'security', 'login']
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

# HTML Template
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
        <button class="btn btn-scan" onclick="startScan()">🚀 Tarama Başlat (15 Rastgele Kelime)</button>
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
        words = get_random_words_from_tdk(15)
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
                logger.info(f"   📧 {found['box_name']}: {found['emails']}")
        
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
