from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def create_pdf(name,items,email):
    class PDF(FPDF):
        def header(self):
            # Logo
            self.image('download.png', 10, 8, 25)
            # font
            self.set_font('helvetica', 'B', 20)
            # Padding
            self.cell(40)
            # Title
            self.cell(120, 10, 'Thanks for Shoping with us', border=True, ln=1, align='C')
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Set position of the footer
            self.set_y(-15)
            # set font
            self.set_font('helvetica', 'I', 8)
            # Set font color grey
            self.set_text_color(169, 169, 169)
            # Page number
            self.cell(0, 10, f'Page {self.page_no()}', align='C')

    # Create a PDF object
    pdf = PDF('P', 'mm', 'Letter')

    # get total page numbers
    pdf.alias_nb_pages()

    # Set auto page break
    pdf.set_auto_page_break(auto = True, margin = 15)

    #Add Page
    pdf.add_page()

    # specify font
    pdf.set_font('helvetica', 'BIU', 16)

    pdf.set_font('times', '', 12)
    pdf.cell(0, 10, f'Dear '+ name +' thanks for chossing us', ln=1)
    pdf.cell(0, 10, f'', ln=1)

    pdf.cell(0, 10, f'Dear ' + name + ' Here your items: ', ln=1)
    for i in range(len(items)//3):
        pdf.cell(0, 10, f'item: '+ items[i*3]+'     amount: '+ items[i*3+1] +'    price: '+items[i*3+2]+'', ln=1)

    pdf.output('pdf_2.pdf')

    print("*****************************************************************************")
    mail_content = '''Bizzi tercih etdiğiniz için teşşekür ederiz
    '''
    sender_address = 'cs308shopping@gmail.com'
    sender_pass = 'oeiuyzfbjqvzvimc'
    receiver_address = email

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'test'
    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'pdf_2.pdf'
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    payload.add_header('Content-Disposition', "attachment; filename= %s" % attach_file_name)
    message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security

    session.login(sender_address, sender_pass)  # login with mail_id and password


    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

lst = ["telefon","2","45USD pound"]
create_pdf("mehmet", lst,"cs308shopping@gmail.com")