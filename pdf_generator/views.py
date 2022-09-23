from django.shortcuts import render
from django.http import Http404
from rest_framework.decorators import api_view
from django.http import JsonResponse,FileResponse
import json

from fpdf import FPDF

@api_view(["POST"])
def pdf(argument):
    try:
        data = json.loads(argument.body)

        #Header and Footer
        class PDF(FPDF):
            def header(self):
                # Header Image
                self.image('pdf_generator/static/images/letter_header.png', 0, 0, pdf.w)
                # self.set_line_width(0.5)
                # self.set_draw_color(237, 100, 43)
                # self.line(12, 40, pdf.w-12, 40)
                # self.set_draw_color(44, 40, 112)
                # self.set_line_width(1.2)
                # self.line(80, 40, pdf.w-80, 40)
                # Line break
                self.ln(40)

            def footer(self):  
                #Gray Line
                self.set_draw_color(214,216,220)
                self.set_line_width(0.5)
                self.line(12, pdf.h-22, pdf.w-12, pdf.h-22)
                #Blue Box
                pdf.set_fill_color(44, 40, 112)
                pdf.rect(0, pdf.h-12, pdf.w, 12, 'F')
                #Page Number
                # self.set_font('Helvetica', 'I', 7)
                # self.set_text_color(166, 166, 166)
                # self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', align='C')

        pdf = PDF('P', 'mm', 'A4')

        #Add font
        pdf.add_font('Montserrat', '', 'pdf_generator/static/fonts/Montserrat/Montserrat-Regular.ttf', uni=True)
        pdf.add_font('Montserrat', 'B', 'pdf_generator/static/fonts/Montserrat/Montserrat-Medium.ttf', uni=True)

        pdf.set_margin(15)
        pdf.add_page()

        #Watermark
        pdf.image('pdf_generator/static/images/letter_watermark.png', 0, (pdf.h/2)-30, pdf.w)

        pdf.set_font('Montserrat', '', 16)

        #To address
        pdf.cell(0, 8, 'To,', new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, 'The Principal', new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, 'EMEA College of Arts and Science', new_x="LMARGIN", new_y="NEXT")

        pdf.ln()

        #Date
        pdf.cell(0, 8, data["date"], new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, data["day"], new_x="LMARGIN", new_y="NEXT")
        pdf.ln()

        #Subject
        pdf.multi_cell(0, 8, f'Subject: {data["subject"]}', new_x="LMARGIN", new_y="NEXT")
        pdf.ln()

        #Body
        pdf.cell(0, 8, "Sir,", new_x="LMARGIN", new_y="NEXT")
        pdf.multi_cell(0, 8, f'     {data["body"]}', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(20)
        pdf.cell(0, 8, "Yours sincerely,", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('Montserrat', 'B', 16)
        pdf.cell(0, 8, "CONNECT", new_x="LMARGIN", new_y="NEXT")


        #Print pdf
        pdf.output('letter.pdf', 'F')
        return FileResponse(open('letter.pdf', 'rb'), as_attachment=True, content_type='application/pdf')

    except ValueError:
        return JsonResponse({"error": "wrong data"})