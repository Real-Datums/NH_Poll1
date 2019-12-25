from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import csv
import datetime
import numpy as np



app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():

    in_arr = [0] # Start of inbound array
    # Respond to the message, and save information to all_text_records.csv
    with open('NH_Poll.csv', 'r') as csvFile:
        csv_reader = csv.reader(csvFile, delimiter=',')
        sent = []
        for row in csv_reader:
            if(len(row) > 0 and row[0] == '1'):
                sent.append(row[1])

    csvFile.close()

    out_arr = ''
    number = request.form['From']
    message_body = request.form['Body']

    print(sent)
    if sent.count(number) < 2:
        response = "Thank you for your response. To view results of the poll, visit @Real_Datums on Twitter."
        resp = MessagingResponse()
        resp.message(response)
        out_arr = [1] # Start of the outbound array
        out_arr.append(number)
        out_arr.append(datetime.datetime.now())
        out_arr.append(response)

    in_arr.append(number)
    in_arr.append(datetime.datetime.now())
    in_arr.append(message_body)



    with open('NH_Poll.csv', 'a') as csvFile:
        print('lol')
        writer = csv.writer(csvFile)
        writer.writerow(in_arr)
        writer.writerow(out_arr)
    csvFile.close()

    if sent.count(number) < 3:
        return str(resp)
    return

if __name__ == "__main__":

    from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'AC36c366d6db1c79fa38c3f17091699b31'
    auth_token = 'e92b42de65bd11409ece55f3d55288ad'

    client = Client(account_sid, auth_token)
    bod = """Your number was randomly selected for an automated poll. Have you personally been winning more since President Trump's election in 2016? Please Respond YES or NO"""
    base = '+1603534'

    suffix = np.random.choice(10000,1000, replace = False)
    suffix = suffix.astype(str)
    suffix = np.core.defchararray.zfill(suffix, 4)
    print(suffix)

    with open('NH_Poll.csv', 'r') as csvFile:
        csv_reader = csv.reader(csvFile, delimiter=',')
        sent = []
        for row in csv_reader:
            if(len(row) > 0 and row[0] == '1'):
                sent.append(row[1])

    csvFile.close()
    for suff in suffix:
        num = base + suff
        if(num not in sent):
            message = client.messages \
                    .create(
                         body=bod,
                            to=num,
                            from_='+12073608810'
                     )

            print(message.sid)  
            out_arr = [1]
            out_arr.append(num)
            out_arr.append(datetime.datetime.now())
            out_arr.append(bod)

            with open('NH_Poll.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(out_arr)
            csvFile.close()


    app.run(debug=True)
