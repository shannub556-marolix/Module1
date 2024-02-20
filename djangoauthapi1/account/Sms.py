from twilio.rest import Client

class Message:
    @staticmethod
    def send(mobile,body_text):
        account_sid = '#AC9aeabca407eb7b0ebcd2918b0af5b50e'         #Please remove # before this token after downloading this code
        auth_token = '#0b5ed139c3e1bf13a9e4d81807c24a56'            #Please remove # before this token after downloading this code  
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_='+15733525401',
        body=body_text,
        to='+91'+mobile
        )
