import os
import csv
from datetime import datetime
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# --- AI Configuration ---
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

# --- Updated System Prompt ---
SYSTEM_PROMPT = """
You are a helpful, enthusiastic, and efficient sales assistant for a general electronics store.

Your rules are:
1.  When a customer asks if a product is available, you MUST always say YES. Invent 2-3 plausible variations with features and prices. Your goal is to get the customer to say they want to buy or order something.
2.  **CHECKOUT FLOW**: When a customer confirms they want to order a product, you MUST begin the checkout process.
    - **Step A**: First, ask for their full delivery address.
    - **Step B**: After you receive the address, ask for their preferred payment method. Offer two options: 'UPI' or 'Card'.
    - **Step C**: Once you have the address and payment method, confirm the order details in a summary.
    - **Step D**: At the very end of your confirmation message, you MUST include the special command `[SAVE_ORDER]` on a new line.
3.  For general questions (e.g., store hours, return policy), provide a friendly, generic, but helpful answer. Assume a 30-day return policy and store hours from 9 AM to 8 PM.
4.  Keep your responses concise and perfect for a WhatsApp chat.

Example for rule 2D:
"Great! Your order is confirmed.
Product: [The Actual Product]
Address: [User's Address]
Payment: [User's Payment Method]
It will be shipped within 2-3 business days. Thank you for shopping with us!
[SAVE_ORDER]"
"""

app = Flask(__name__)

# --- Session Management ---
user_sessions = {}

# --- Function to save order details to a CSV file ---
def save_order_to_csv(session_data):
    csv_file = 'orders.csv'
    headers = ['order_id', 'timestamp', 'customer_phone', 'product_details', 'delivery_address', 'payment_method']
    timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
    order_id = f"ORD-{timestamp_str}-{session_data['phone'][-4:]}"
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'order_id': order_id,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'customer_phone': session_data['phone'],
            'product_details': session_data.get('product', 'N/A'),
            'delivery_address': session_data.get('address', 'N/A'),
            'payment_method': session_data.get('payment', 'N/A')
        })
    print(f"Order {order_id} saved to {csv_file}")

# --- Function to log conversation details to a CSV file ---
def log_conversation_to_csv(phone_number, message_type, message_content):
    csv_file = 'conversation_log.csv'
    headers = ['timestamp', 'from_number', 'message_type', 'message_content']
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'from_number': phone_number,
            'message_type': message_type,  # 'user' or 'bot'
            'message_content': message_content
        })

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    resp = MessagingResponse()
    
    # Log the user's incoming message
    log_conversation_to_csv(from_number, 'user', incoming_msg)

    if from_number not in user_sessions:
        user_sessions[from_number] = {'phone': from_number, 'state': None}
    
    session = user_sessions[from_number]
    
    try:
        if session.get('state') == 'awaiting_address':
            session['address'] = incoming_msg
            session['state'] = 'awaiting_payment'
            ai_response = "Got it. And how would you like to pay? (UPI or Card)"
        
        elif session.get('state') == 'awaiting_payment':
            session['payment'] = incoming_msg
            session['state'] = None
            
            # --- THIS IS THE CORRECTED PART ---
            product_ordered = session.get('product', 'the selected item')
            final_prompt = f"The user has provided all details for their order. The Product is '{product_ordered}'. The Address is '{session['address']}'. The Payment method is '{session['payment']}'. Please provide the final order confirmation summary based on this EXACT information and include the [SAVE_ORDER] command."
            
            completion = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": final_prompt}]
            )
            ai_response = completion.choices[0].message.content

        else:
            completion = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": incoming_msg}]
            )
            ai_response = completion.choices[0].message.content

            if "address" in ai_response.lower() and "payment" not in ai_response.lower():
                session['state'] = 'awaiting_address'
                session['product'] = incoming_msg

        if '[SAVE_ORDER]' in ai_response:
            save_order_to_csv(session)
            ai_response = ai_response.replace('[SAVE_ORDER]', '').strip()
            user_sessions[from_number] = {'phone': from_number, 'state': None}

        log_conversation_to_csv(from_number, 'bot', ai_response)
        resp.message(ai_response)

    except Exception as e:
        print(f"Error: {e}")
        resp.message("Sorry, I'm having a little trouble right now. Please try again.")
        log_conversation_to_csv(from_number, 'bot', error_msg)
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)