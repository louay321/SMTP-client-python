import smtplib

from string import Template #this will contain header and body for the email
"""""
MIME is message object i'll use because i was trying
over and over to send mail to gmail account and 
google accounts always rejected it
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'MyEmail'
PASSWORD = 'MyPassword'

#instead of using database i'll use a txt file with contacts names and emails (contacts.txt)

def get_contacts(filename):

    names = [] #first data in file is contact's name
    emails = [] # second one is contact's email
    with open(filename, mode='r', encoding='utf-8') as contacts_file: #here i open the file in reading mode
        for contact in contacts_file:
            names.append(contact.split()[0]) #add a name to list of names
            emails.append(contact.split()[1]) #add an email to list of emails
    return names, emails


def read_template(filename):

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main():
    names, emails = get_contacts('contacts.txt')  # read contacts from contacts.txt file
    message_template = read_template('message.txt') #the template i wrote in message.txt

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    #send the email for each contact in the list:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message

        #this will replace the actual person's name in the template since i left it as variable PERSON_NAME
        message = message_template.substitute(PERSON_NAME=name.title())

        # parameters of the message 'Header'
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "this is just a test"

        #here i add in the message body as plain text
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

    #close the connection and terminate the Session
    s.quit()


if __name__ == '__main__': #start the program
    main()