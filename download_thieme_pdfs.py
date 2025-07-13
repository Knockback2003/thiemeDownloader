from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os

# === CONFIG ===
download_dir = os.path.expanduser("~/Downloads/thieme_pdfs")  # Zielordner

# === SETUP ===
os.makedirs(download_dir, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
# chrome_options.add_argument("--headless=new")  # Nur aktivieren, wenn GUI nicht verfügbar ist

# Temporäres Profil verwenden (um Konflikte zu vermeiden)
temp_profile_dir = os.path.expanduser("~/temp_chrome_profile")
chrome_options.add_argument(f"--user-data-dir={temp_profile_dir}")
chrome_options.add_argument("--profile-directory=Default")

chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
    "profile.default_content_settings.popups": 0
})

# ChromeDriver automatisch verwalten
from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# === DOWNLOAD-PROZESS ===
try:
    print("🚀 Starte Downloads...")
    
    # Zuerst zur Thieme-Seite gehen für manuelle Anmeldung
    print("🔐 Öffne Thieme-Seite für Anmeldung...")
    driver.get("https://eref.thieme.de/")
    input("📋 Bitte melde dich in dem geöffneten Browser an und drücke dann Enter um fortzufahren...")
    
    # Interaktive Eingabe der Parameter
    print("\n" + "="*50)
    print("📝 KONFIGURATION")
    print("="*50)
    
    # URL-Beispiel eingeben
    print("🔗 Beispiel-URL: https://eref.thieme.de/ebooks/pdf/cs_13123019/302830101_003_001.pdf")
    example_url = input("📥 Gib eine Beispiel-URL ein: ").strip()
    
    # Kapitel extrahieren oder eingeben
    print(f"\n📖 Beispiel: Für Kapitel 003 gib '003' ein")
    chapter = input("📖 Kapitel (3-stellig, z.B. 003): ").strip().zfill(3)
    
    # Seiten-Bereich eingeben
    start_page = int(input("🔢 Startseite: ").strip())
    end_page = int(input("🔢 Endseite: ").strip())
    
    # Base-URL aus der Beispiel-URL ableiten
    if example_url:
        # URL-Template erstellen
        base_url = example_url.rsplit('_', 1)[0] + "_{:03d}.pdf"
        print(f"\n✅ URL-Template: {base_url}")
    else:
        print("❌ Keine URL eingegeben!")
        exit(1)
    
    print(f"\n📋 ZUSAMMENFASSUNG:")
    print(f"   Kapitel: {chapter}")
    print(f"   Seiten: {start_page} bis {end_page}")
    print(f"   Downloads: {end_page - start_page + 1} PDFs")
    
    confirm = input("\n🚀 Downloads starten? (Enter für JA, 'n' für Abbruch): ").strip()
    if confirm.lower() == 'n':
        print("❌ Abgebrochen.")
        exit(0)
    
    print("\n" + "="*50)
    print("📥 DOWNLOAD GESTARTET")
    print("="*50)
    
    for i in range(start_page, end_page + 1):
        url = base_url.format(i)
        print(f"📥 Lade Seite {i}: {url}")
        
        try:
            driver.get(url)
            print(f"✅ Seite {i} geladen")
            sleep(3)  # Etwas mehr Zeit für den Download
        except Exception as e:
            print(f"❌ Fehler bei Seite {i}: {e}")
            continue
            
    print("\n✅ Alle Downloads angestoßen.")
    
except Exception as e:
    print(f"❌ Allgemeiner Fehler: {e}")
finally:
    print("⏳ Warte auf finale Downloads...")
    sleep(10)  # Mehr Zeit für letzte Downloads
    driver.quit()
    print("🔚 Browser geschlossen.")
