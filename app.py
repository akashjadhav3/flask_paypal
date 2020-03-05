from flask import Flask,render_template,jsonify, request
import paypalrestsdk

app=Flask(__name__)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AczmCkpo9D4Q4OoggedheZ1uE0ugMWybo9xoRnOnhP3dIVBLjUt8TqkHmtEP28zU0vVOavKJBwfsvCML",
  "client_secret": "EIyySRqipXpPq_oqyMz9JQ-H1c1TZuegwbd_0FZqMFALwMCa6onDcBaYm4sf7_BERTaePS_kb3-2ZMqZ" })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment',methods=['POST'])
def payment():
    payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
        "payment_method": "paypal"},
    "redirect_urls": {
        "return_url": "http://localhost:3000/payment/execute",
        "cancel_url": "http://localhost:3000/"},
    "transactions": [{
        "item_list": {
            "items": [{
                "name": "testitem",
                "sku": "12345",
                "price": "500.00",
                "currency": "USD",
                "quantity": 1}]},
        "amount": {
            "total": "500.00",
            "currency": "USD"},
        "description": "This is the payment transaction description."}]})
    if payment.create():
        print("success!!!")
        print(payment.id)
    else:
        print(payment.error)

    return jsonify({"paymentID":payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])
    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute success!')
        success=True
    else:
        print(payment.error)
    return jsonify({'success':success})

if __name__=='__main__':
    app.run(debug=True)