import base64

# --- Proof of Work ---
page.wait_for_timeout(3000)
page.screenshot(path="proof.png")
b64_img = base64.b64encode(page.screenshot()).decode('utf-8')
