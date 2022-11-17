from datetime import datetime
from patholib import Path

def main():
    with sync_playwright() as playwright:
        response = validate_rvm(playwright, folio=barcode_folio, cod=cod_verif)


def validate_rvm(playwright, folio, cod):
    time = datetime.now()
    dir_name = time.strftime("%Y-%m-%d-%H-%M-%S")

    chromium = playwright.chromium
    browser = chromium.launch(
        # executable_path="/ms-playwright/webkit-1641/pw_run.sh",
        proxy={"server": "http://lum-customer-hl_ed8dfd4a-zone-data_center-country-cl:rb9601f3ildw@zproxy.lum-superproxy.io:22225"},
    )
    context = chromium.launch_persistent_context(
        user_data_dir=Path(f"/tmp/{dir_name}"),
        headless=True,
        args=[
            "--autoplay-policy=user-gesture-required",
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-breakpad",
            "--disable-client-side-phishing-detection",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-dev-shm-usage",
            "--disable-domain-reliability",
            "--disable-extensions",
            "--disable-features=AudioServiceOutOfProcess",
            "--disable-hang-monitor",
            "--disable-ipc-flooding-protection",
            "--disable-notifications",
            "--disable-offer-store-unmasked-wallet-cards",
            "--disable-popup-blocking",
            "--disable-print-preview",
            "--disable-prompt-on-repost",
            "--disable-renderer-backgrounding",
            "--disable-setuid-sandbox",
            "--disable-speech-api",
            "--disable-sync",
            "--disk-cache-size=33554432",
            "--hide-scrollbars",
            "--ignore-gpu-blacklist",
            "--metrics-recording-only",
            "--mute-audio",
            "--no-default-browser-check",
            "--no-first-run",
            "--no-pings",
            "--no-sandbox",
            "--no-zygote",
            "--password-store=basic",
            "--use-gl=swiftshader",
            "--use-mock-keychain",
            "--single-process",
            "--disable-gpu",
            "--font-render-hinting=none",
        ]
    )

    page = context.pages[0]  # Open a new page/tab in incognito browser

    # context = browser.new_context()
    # page = context.new_page()

    page.goto("https://www.registrocivil.cl/OficinaInternet/verificacion/verificacioncertificado.srcei")
    page.wait_for_timeout(2000)

    input_folio = page.locator("#ver_inputFolio")
    # input_folio.wait_for()
    input_folio.type(folio, delay=100)

    input_cv = page.locator("#ver_inputCodVerificador")
    # input_cv.wait_for()
    input_cv.type(cod, delay=100)

    page.evaluate("document.getElementById('ver_btnConsultar').click()")

    page.wait_for_timeout(5000)

    # Validate
    error_attr = page.locator("div#ver_msgError").get_attribute("style")
    if "block" in error_attr:  # if not valid
        browser.close()
        return {"message": "Invalid document"}

    browser.close()
    return {"message": "Validation success"}


if __name__ == "__main__":
    main()