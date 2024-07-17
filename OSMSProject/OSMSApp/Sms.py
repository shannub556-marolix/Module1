from twilio.rest import Client

class Message:
    @staticmethod
    def send(body_text):
        account_sid = 'AC9aeabca407eb7b0ebcd2918b0af5b50e' 
        auth_token = ''            #Please remove # before this token after downloading this code  
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_='+15733525401',
        body=body_text,
        to='+919550685733'
        )
