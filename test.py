from main import Client, pix


client = Client().login("admin")
payment = client.payments
payment_data = payment.create(pix(
  amount=22.0,
  payer_email="test@gmail.com"
))

print(payment_data)