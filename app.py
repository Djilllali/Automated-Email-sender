from fileinput import filename
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pandas as pd
import smtplib
from email.utils import formataddr
from email.message import EmailMessage
import ssl
from email.utils import make_msgid 
def generatePDF(text): 
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(380, 560, text)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("relax.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(f"{text}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

df = pd.read_csv('registrations_relax.csv', sep=',', header=None)

print(df.values[0])


context=ssl._create_unverified_context()

for ite in df.values : 
    name_full = ite[1]+" "+ite[2]
    generatePDF( text=name_full)
    with smtplib.SMTP_SSL(host="smtp.123-reg.co.uk" , port="465" ,context=context  )as server:
        server.login("noreply@turingjobsdz.com", "xLYpXuKG_Bwj27n")
        # server.verify('khalfounmohamedelmehdi@gmail.com')
        msg = EmailMessage()
        msg.set_content('''
            On vous envoie un autre RIP CCP pour que vous finalisez votre inscription.
            Veuillez nous excuser pour ce blocage , merci pour votre compréhension .
            Remarque : Après l'envoi des frais de l'inscription veuillez nous envoyer 
            le reçu ccp à notre boite mail : ccp@turingjobsdz.com
            et de nous fournir les documents suivants par mail : 
            - CV 
            - Diplome / Certeficat de scolarité 
            - Photo copie de la pièce d'identité
        ''')
        msg['Subject'] = "Confirmation de l'inscription à Turing Jobs"
        msg['From'] = formataddr(('Turing Jobs' , "noreply@turingjobsdz.com")) 
        msg['To'] = ite[0]
        msg['message-id'] = make_msgid()
        with open(f"{name_full}.pdf", 'rb') as fp:
            file_data = fp.read()
            msg.add_attachment(file_data , maintype="application" , subtype="pdf"  , filename="proforma.pdf" )
        try :
            server.send_message(msg)
        except Exception as e :
            print('--------------error sending email')
            print('--------------name' , name_full)
            print('--------------error message ', e)
            print('***************************************************' )

        server.quit()






