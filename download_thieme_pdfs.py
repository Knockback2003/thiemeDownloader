from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os

download_dir = os.path.expanduser("~/Downloads/thieme_pdfs")

os.makedirs(download_dir, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")

temp_profile_dir = os.path.expanduser("~/temp_chrome_profile")
chrome_options.add_argument(f"--user-data-dir={temp_profile_dir}")
chrome_options.add_argument("--profile-directory=Default")

chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
    "profile.default_content_settings.popups": 0
})

from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("Version: 1.1.0")
    print("🚀 Start downloads...")
    
    print("🔐 Open Thieme-Site for User Auth...")
    driver.get("https://eref.thieme.de/")
    input("📋 Please Login in the chrome window that just opened and press enter afterwards...")
    
    print("\n" + "="*50)
    print("📝 CONFIGURATION")
    print("="*50)
    
    print("🔗 Example: https://eref.thieme.de/ebooks/pdf/cs_13123019/302830101_002_001.pdf")

    while True:
        start_url = input("🔗 Start-URL (full URL, e.g., https://eref.thieme.de/ebooks/pdf/cs_13123019/302830101_002_001.pdf): ").strip()
        if start_url:
            break
        print("❌ Start-URL cannot be empty. Please provide a valid URL.")

    base_start_url = '_'.join(start_url.rsplit('_', 2)[:-1]) + '_'
    start_page = start_url.rsplit('_', 1)[-1].split('.')[0]

    print(f"🏁 End page should only include the last value (page) after the last underscore (_). For example, if the Start-URL is {start_url}, you would input the page value (e.g., 050).")

    while True:
        end_page = input(f"🏁 End page (e.g., 050 for {base_start_url}...): ").strip()
        if end_page.isdigit():
            break
        print("❌ End page must be a valid number. Please try again.")

    end_url = f"{base_start_url}{end_page}.pdf"

    try:
        start_filename = start_url.split('/')[-1]
        start_page = int(start_filename.rsplit('_', 1)[1].split('.')[0])

        end_filename = end_url.split('/')[-1]
        end_page = int(end_filename.rsplit('_', 1)[1].split('.')[0])

        base_filename = start_filename.rsplit('_', 1)[0]
        base_path = '/'.join(start_url.split('/')[:-1])
        base_url = f"{base_path}/{base_filename}" + "_{:03d}.pdf"

    except (ValueError, IndexError) as e:
        print(f"❌ Error while parsing values: {e}")
        print("Check the input format!")
        exit(1)
    
    if start_page > end_page:
        print(f"❌ Start-Site ({start_page}) is bigger than End-Site ({end_page})!")
        exit(1)
    
    print(f"\n✅ URL-Template: {base_url}")
    print(f"\n📋 SUMMERY:")
    print(f"   Start-Site: {start_page}")
    print(f"   End-Site: {end_page}")
    print(f"   Downloads: {end_page - start_page + 1} PDFs")
    print(f"   First URL: {base_url.format(start_page)}")
    print(f"   Last URL: {base_url.format(end_page)}")
    
    confirm = input("\n🚀 Start downloads? (Enter for YES, 'n' for NO): ").strip()
    if confirm.lower() == 'n':
        print("❌ Terminated.")
        exit(0)
    
    print("\n" + "="*50)
    print("📥 DOWNLOAD STARTED")
    print("="*50)
    
    for i in range(start_page, end_page + 1):
        url = base_url.format(i)
        filename = url.split('/')[-1]
        file_path = os.path.join(download_dir, filename)

        print(f"📥 Loading page {i}: {url}")

        retries = 3
        while retries > 0:
            try:
                driver.get(url)
                if driver.title:
                    print(f"✅ Page {i} loaded successfully")
                    sleep(3)

                    if os.path.exists(file_path):
                        print(f"✅ File {filename} downloaded successfully")
                        break
                    else:
                        raise Exception("File not downloaded")
                else:
                    raise Exception("Page did not load correctly")
            except Exception as e:
                retries -= 1
                print(f"❌ Error loading page {i} or downloading file: {e}. Retries left: {retries}")
                if retries == 0:
                    print(f"⚠️ Skipping page {i} after multiple failed attempts.")
                    break
                sleep(2)

    print("\n✅ All downloads started.")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
finally:
    print("⏳ Waiting for final downloads...")
    sleep(10)
    driver.quit()
    print("🔚 Browser closed.")
