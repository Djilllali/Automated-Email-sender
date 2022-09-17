from fileinput import filename
from unicodedata import name
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pandas as pd
import smtplib
from email.message import EmailMessage
import ssl
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


generatePDF( text="JOHN DOE")
df = pd.read_csv('registrations_relax.csv', sep=',', header=None)



context=ssl._create_unverified_context()



with smtplib.SMTP_SSL(host="smtp.123-reg.co.uk" , port="465" ,context=context  )as server:
    server.login("contact@turingjobsdz.com", "xLYpXuKG_Y6DdRL")
    for ite in df.values : 
        name_full = ite[1]+" "+ite[2]
        generatePDF( text=name_full)
        msg = EmailMessage()
        msg.set_content('envoyez au ccp ')
        msg['Subject'] = "inscriptions"
        msg['From'] = "contact@turingjobsdz.com"
        print('-------mail address',ite[0])
        msg['To'] = ite[0]

        with open(f"{name_full}.pdf", 'rb') as fp:
            file_data = fp.read()
            msg.add_attachment(file_data , maintype="application" , subtype="pdf"  , filename="facture proforma.pdf" )
        server.send_message(msg)





