from playwright.sync_api import sync_playwright
import pyotp
import time
import pytest

def get_totp_code(secret_key):
    try:
        print(f"Pokúšam sa vygenerovať kód s kľúčom: {secret_key}")
        totp = pyotp.TOTP(secret_key)
        code = totp.now()
        print(f"Úspešne vygenerovaný kód: {code}")
        return code
    except Exception as e:
        print(f"Chyba pri generovaní kódu: {str(e)}")
        return None

@pytest.mark.parametrize("credentials", [
    {
        "email": "tomas.krisica@w1kvs.onmicrosoft.com",  # Tu doplň svoj email
        "password": "Tomas07052003",  # Tu doplň svoje heslo
        "totp_key": "rhrsckmdnpm6zlmr"
    }
])
def test_powerapps_login(credentials):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        
        context = browser.new_context()
        page = context.new_page()
        
        try:
            print("Otváram make.powerapps.com...")
            page.goto('https://org57b3585d.crm4.dynamics.com/main.aspx?appid=0315801e-2fcf-ef11-8ee9-000d3a6576c9&pagetype=entitylist&etn=tom_student1&viewid=6c874a3c-91ba-4991-b94d-795c116e34c5&viewType=1039&lid=1741177896109')
            
            # Čakanie na prihlasovací formulár
            print("Čakám na prihlasovací formulár...")
            page.wait_for_selector('input[type="email"]', state='visible', timeout=30000)
            
            # Zadanie emailu
            print("Zadávam email...")
            email_input = page.locator('input[type="email"]')
            email_input.fill(credentials["email"])
            page.click('input[type="submit"]')
            
            # Čakanie na pole pre heslo
            print("Čakám na pole pre heslo...")
            page.wait_for_selector('input[type="password"]', state='visible', timeout=30000)
            
            # Po zadaní hesla:
            print("Zadávam heslo...")
            password_input = page.locator('input[type="password"]')
            password_input.fill(credentials["password"])
            page.click('input[type="submit"]')
            
            # Dlhšie čakanie na načítanie
            time.sleep(5)
            
            
            # Čakanie a zadanie verifikačného kódu
            print("Zadávam verifikačný kód...")
            totp_code = get_totp_code(credentials["totp_key"])
            page.fill('input[aria-label="Code"]', totp_code)
            page.click('input[type="submit"]')

            # Čakanie na tlačidlo Yes a kliknutie
            print("Čakám na tlačidlo Yes...")
            page.wait_for_selector('text=Yes', state='visible', timeout=10000)
            page.click('text=Yes')
            
            print("Prihlásenie úspešné!")
            time.sleep(10)  # počkáme na konci
            
        except Exception as e:
            print(f"Nastala chyba: {str(e)}")
            raise e
        
        finally:
            browser.close()
