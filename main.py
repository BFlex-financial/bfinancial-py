from requests import post
import json

class HandlerPayments:
  def __init__(self, paymentsClass):
    self.payments = paymentsClass

class Client:
  def login(self, auth_key: str):
    self.auth = auth_key
    return HandlerPayments(paymentsClass=Payment(self))
  
def pix(
  amount: float,
  payer_email: str
) -> object:
  return {
    'method': "Pix",
    'payer_email': payer_email,
    'amount': amount
  }

def card(
  amount: float,

  number: str,
  cvv: str,
  expiration_year: int,
  expiration_month: int,

  payer_email: str,
  payer_name: str,
  payer_cpf: str
) -> object: 
  return {
    'method': "Card",
    'number': number,
    'cvv': cvv,
    'expiration_year': expiration_year,
    'expiration_month': expiration_month,
    'payer_email': payer_email,
    'payer_name': payer_name,
    'payer_cpf': payer_cpf,
    'amount': amount
  }

class Payment:
  def __init__(self, instance):
    self.__api_url = "http://127.0.0.1:8080"
    self.key = f"Bearer {instance.auth}";

  def create(self, data: object) -> object:
    if data['method'] != "Card" and data['method'] != "Pix":
      return {'error': "Internal error"}

    response = post(
      url=f"{self.__api_url}/payment/create",
      json=data,
      headers={
        'Content-type': "application/json",
        'Authorization-key': self.key  
      },
      stream=True
    )
    
    try:
      response_text = ""
      for chunk in response.iter_content(chunk_size=1024):
        response_text += chunk.decode('utf-8') 
      api_return = json.loads(response_text)
    except ValueError as e:
      return {'error': "Error parsing JSON"}
    return api_return.get('data', {'error': "No data field in response"})
