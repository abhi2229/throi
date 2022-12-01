import logging
from os import O_TRUNC
from flask import Flask,render_template,request
import pickle
import numpy as np
import smtplib
import requests
app = Flask(__name__)
logging.basicConfig(filename='logfile.log', filemode='a',level=logging.INFO,format="%(asctime)s : %(levelname)s : %(message)s", datefmt="%Y-%m-%D %H %M %S")

with open("src\Thyroid_model.pkl","rb") as model_file:
    model=pickle.load(model_file)


def sent_Email(receiver_mail,mainmessage):

    server=smtplib.SMTP('smtp.outlook.com',587)

    server.starttls()

    server.login('soumyadeep4066@outlook.com','Tatan@1234')

    subj="YOUR THYROID REPORT "

    message_text = mainmessage

    #body of The mail

    msg = "Subject: %s\n\n%s" % ( subj, message_text)

    sender_mail='soumyadeep4066@outlook.com'
    server.sendmail(receiver_mail,sender_mail,msg)

@app.route('/')
def index():
   try:
       logging.info("===HOME PAGE RENDERED===")
       return render_template('home.html')
   except:
       logging.error("===PAGE RENDERING FAIL===")
   
@app.route("/about", methods = ["GET", "POST"])
def about():
    return render_template('moreinfo.html')


@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":
        Emailaddress=(request.form.get('Email Address'))
        Name= request.form.get('Name')
        print(Emailaddress)
        print(Name)
    return render_template('predict.html')

@app.route("/predictresult", methods = ["GET", "POST"])
def predictresult():
    try:
        if request.method == "POST":
            logging.info("===CALLING METHOD IS POST METHOD===")
            Age=float(request.form.get('age'))
            Sex= request.form.get('sex')
            Level_thyroid_stimulating_hormone= float(request.form.get('TSH'))
            Total_thyroxine_TT4= float(request.form.get('TT4'))
            Free_thyroxine_index=float(request.form.get('FTI'))
            On_thyroxine= request.form.get('on_thyroxine')
            On_antithyroid_medication= request.form.get('on_antithyroid_medication')
            Goitre= request.form.get('goitre')
            Hypopituitary = request.form.get('hypopituitary')
            Psychological_symptoms = request.form.get('psych')
            T3_measured= request.form.get('T3_measured')
            logging.info("===DATA COLLECTED SUCCESSFULY===")
    except:
        logging.error("===INVALID INPUT===")
    logging.info("===CONVERTING CATEGORICAL VALUES INTO NUMERICAL VALUES===")
    #Sex
    if Sex=="Male":
        Sex=1
    else:
        Sex=0
    #On_thyroxine
    if On_thyroxine=="True":
        On_thyroxine=1
    else:
        On_thyroxine=0

    #On_antithyroid_medication
    if On_antithyroid_medication=="True":
        On_antithyroid_medication=1
    else:
        On_antithyroid_medication=0
        
    #Goitre
    if Goitre=="True":
        Goitre=1
    else:
        Goitre=0

    #Hypopituitary
    if Hypopituitary=="True":
        Hypopituitary=1
    else:
        Hypopituitary=0

    #Psychological_symptoms
    if Psychological_symptoms=="True":
        Psychological_symptoms=1
    else:
        Psychological_symptoms=0

    #T3_measured
    if T3_measured=="True":
        T3_measured=1
    else:
        T3_measured=0
    logging.info("===CATEGORICAL VALUES ARE CONVERTED SUCCESSFULLY===")



    logging.info("===CREATING AN ARRAY WITH INPUT VALUES===")
    arr=np.array([[Age,Sex,Level_thyroid_stimulating_hormone,Total_thyroxine_TT4,Free_thyroxine_index,
    On_thyroxine,On_antithyroid_medication,Goitre,Hypopituitary,Psychological_symptoms,T3_measured]])
    logging.info("===PASSING THIS ARRAY TO OUR MODEL FOR PREDICTION===")
    try:
        pred=model.predict(arr)
    except:
        logging.error("===DUE TO SOME REASON MODEL IS UNABLE TO PREDICT===")

    logging.info("===CONVERTING PREDICTED VALUE INTO ITS CORRESPONDING OUTPUT===")
    if pred==0:
        res_Val="Compensated Hypothyroid"
    elif pred==1:
        res_Val="No Thyroid"
    elif pred==2:
        res_Val='Primary Hypothyroid'
    elif pred==3:
        res_Val='Secondary Hypothyroid'

        
    Output=f"Patient has {res_Val}"
    #sent_Email('soumyadeep4066@gmail.com', 'Bolo Radhe Radhe')
    logging.info("===OUTPUT PASSED===")
    return render_template('predictresult.html',output=Output)



    return render_template("home.html")

if __name__ == "__main__":
    app.run()
