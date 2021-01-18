from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import re
import pandas as pd
import os
from twilio.rest import Client
from action.message import Messages,count
from template.temp import Template
from spreadsheet.filepath import SPR_FOLDER
app = Flask(__name__)
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sql=['welcome_message.txt','thanking_message.txt','template_error_message.txt']
mas=[]
for i in sql:
    with open(os.path.join(THIS_FOLDER, i),'rb') as f:
        mas.append(f.read())
class BOT:
    def __init__(self,Id,msg):
        self.id=Id
        self.msg=msg
        self.__count=0
        self.first=False
        self.info=False
    def count(self,msg):
        self.__count+=1
        self.msg=msg
    def get_count(self):
        return self.__count
    def counter(self,msg):
        if not(self.first):
            co=[i+1 for i in range(count)]
            try:
                if int(msg.strip(" ,.()")) in co:
                    self.count(msg)
                    #print("message:",msg)
                    self.first=True
                    return Messages[int(msg.strip(" ,.()"))-1]
                else:
                    return "try to press"+"("+str(co[0])+"-"+str(co[-1])+")"
            except:
                return "try to press"+"("+str(co[0])+"-"+str(co[-1])+")"
        elif not(self.info):
            
            if BOT.store(msg,int(self.msg.strip(" ,.)("))):
                self.info=True
                return mas[1]
            else:
                self.count(self.msg)
                return mas[2]
            
            
            
            
    @staticmethod
    def Find_Links(string): 
    	# findall() has been used 
    	# with valid conditions for urls in string 
    	regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    	url = re.findall(regex,string)	 
    	return [x[0] for x in url] 
    def welcome():
        return mas[0]
    def store(msg,method):
        print("in")
        if Template[method-1] == "":
            return True
        s=Template[method-1].split("\n")
        m=[]
        try:
            for i in s:
                if re.findall(i, msg)[0] != None: 
                    m.append("".join(re.findall(i, msg)))
        except:
            return False
        if len(m) != 0:
            links=BOT.Find_Links(msg)
            if len(links) != 0:
                m.append(links)
            df=pd.DataFrame({"i"+str(i):[m[i]] for i in range(len(m))})
            #result=ds.append(df)
            print(df)
            try:
                df.to_csv(os.path.join(SPR_FOLDER,'data.csv'),mode='a',index=False,header=False)
                df.to_csv(os.path.join(THIS_FOLDER,'data.csv'),mode='a',index=False,header=False)
            except:
                pass
            #BOT.send(msg)
            return True
        else:
            return False
    def send(msg):
        # Your Account Sid and Auth Token from twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = os.environ['auth_sid']
        auth_token = os.environ['auth_token']
        client = Client(account_sid, auth_token)
        
        message = client.messages \
                        .create(
                             body=msg,
                             from_='+14155238886',
                             to='+8613267093249'
                         )
        return True
        
                    
obj=[]
@app.route("/")
def bot():
    return "Whatsapp chatbot"

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with a simple text message."""
    resp = MessagingResponse()
    phoneno=request.form.get('From')
    msg=request.form.get('Body')
    currentuser=None
    for i in obj:
        if i.id == phoneno:
            currentuser=i
    if currentuser == None:
        obj.append(BOT(phoneno,msg))
        currentuser=obj[-1]
        resp.message(BOT.welcome())
    else:
        rp=currentuser.counter(msg)
        if rp == None:
            obj.remove(currentuser)
        else:
            resp.message(rp)
            if currentuser.get_count() > 3:
                obj.remove(currentuser)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)