from twilio.rest import Client

class Message:
    @staticmethod
    def send(mobile,body_text):
        account_sid = 'AC89101338654575b3281d5dc0a3a286b4'
        auth_token = 'f2de53cb59d04d085202db27961c07b6'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_='+19494306759',
        body=body_text,
        to='+91'+mobile
        )
