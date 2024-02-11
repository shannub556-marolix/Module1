from twilio.rest import Client

class Message:
    @staticmethod
    def send(mobile,body_text):
        account_sid = 'AC89101338654575b3281d5dc0a3a286b4'
        auth_token = 'f0e264a1ff5b6360ad849dc246aac391'            #Please remove # before this token after downloading this code  
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_='+19494306759',
        body=body_text,
        to='+91'+mobile
        )
