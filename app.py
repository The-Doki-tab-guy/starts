from flask import Flask, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os
import logging

app = Flask(__name__, static_folder='.')
logging.basicConfig(level=logging.INFO)

ATERNOS_EMAIL = os.getenv('ATERNOS_EMAIL')
ATERNOS_PASSWORD = os.getenv('ATERNOS_PASSWORD')

if not ATERNOS_EMAIL or not ATERNOS_PASSWORD:
    raise ValueError("Missing ATERNOS_EMAIL or ATERNOS_PASSWORD env vars")

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/start', methods=['POST'])
def start_server():
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(15)
        
        logging.info("Logging in to Aternos...")
        driver.get('https://aternos.org/login')
        
        # Wait for login form and fill it
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'user'))
        )
        driver.find_element(By.NAME, 'user').send_keys(ATERNOS_EMAIL)
        driver.find_element(By.NAME, 'password').send_keys(ATERNOS_PASSWORD)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # Wait for redirect to server page
        WebDriverWait(driver, 15).until(
            lambda d: 'server' in d.current_url
        )
        logging.info("Login successful, navigating to server...")
        
        time.sleep(2)
        
        # Find and click start button
        logging.info("Looking for start button...")
        start_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "start") or contains(text(), "Start")]'))
        )
        start_btn.click()
        logging.info("Start button clicked")
        
        # Wait for confirmation
        time.sleep(2)
        
        return jsonify({'success': True, 'message': 'Server starting... check Aternos in 10-20 seconds'}), 200
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': f'Failed to start server: {str(e)}'}), 500
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
