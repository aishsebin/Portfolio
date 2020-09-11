from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.validators import Auto
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String, Rect
from datetime import date


from reportlab.platypus import Paragraph, SimpleDocTemplate,Image, PageTemplate, Frame, PageBreak, FrameBreak, Spacer, NextPageTemplate, HRFlowable
import random


cash=[209804, 210353, 548.48, 0.26, 281.49, 0.13, 1.98]
FI=[4531082, 4892169, 206462, 4.56, 217467, 4.45, 45.94]
Equity=[5218922,5362021.34,-62131.35,-1.19,117832,2.2,50.36]
Commodities=[0]*7
NonTrad=[0]*7
Investment=225323
Valuation=865489


def add_legend(draw_obj, chart, data,doc):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = doc.width/2+100
    legend.y = doc.height/2
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)

def pie_chart_with_legend(doc):
    data=['Cash ('+str(cash[6])+'%)','Fixed Income ('+str(FI[6])+'%)','Equity ('+str(Equity[6])+'%)','Commodities ('+str(Commodities[6])+'%)','Non-Traditional ('+str(NonTrad[6])+'%)']
    drawing = Drawing(width=doc.width/2, height=250)
    my_title = String(100, 25, 'Asset-wise Allocation', fontSize=14)
    pie = Pie()
    pie.sideLabels = False
    pie.slices.label_visible = False
    pie.x = 100
    pie.y = 40
    pie.width=200
    pie.height=200
    pie.data = [cash[6],FI[6],Equity[6],Commodities[6],NonTrad[6]]
    pie.labels = data
    pie.slices.strokeWidth = 0.5
    drawing.add(my_title)
    drawing.add(pie)
    add_legend(drawing, pie, data,doc)
    return drawing


styles = getSampleStyleSheet()
styleN = styles['Normal']
styleContent= ParagraphStyle(name='content', parent=styles['Normal'], fontSize=18, leading=35)
styleH = styles['Heading1']
style_right = ParagraphStyle(name='right', parent=styles['Heading1'], alignment=TA_RIGHT, fontSize=24)


story = []
doc = SimpleDocTemplate('hello.pdf',pagesize = landscape(A4),rightMargin=30,leftMargin=30,topMargin=30, bottomMargin=30)
words = "lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore et".split()
logo= 'AIM_logo.jpg'
portfolioDate= date.today()




#add some flowables
myFrame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='myFrame')
frame1=Frame(doc.leftMargin, doc.bottomMargin,doc.width/2-6, doc.height, id='col1')
frame2=Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin,doc.width/2-6, doc.height, id='col2')

coverPage=PageTemplate(id='Cover', frames=[myFrame])
columnTemplate=PageTemplate(id='TwoCol',frames=[frame1,frame2])

story.append(Image(logo, 2*inch, 2*inch, hAlign='RIGHT'))
story.append(Spacer(0,10))
story.append(Paragraph("CLIENT  PORTFOLIO",style_right))
story.append(HRFlowable(width='100%', thickness=5, color=colors.navy))
story.append(Spacer(0,15))

story.append(Paragraph("TABLE OF CONTENTS",ParagraphStyle(name='content', parent=styles['Normal'], fontSize=18, leading=35)))

story.append(Paragraph("Portfolio Holdings"+"."*100+"1",styleN))

story.append(NextPageTemplate('TwoCol'))
story.append(PageBreak())
story.append(Paragraph("Portfolio Holdings",styleH))
story.append(Paragraph("As of "+str(portfolioDate),styleContent))

draw = Drawing(200, 150)
rect=Rect(doc.width/4, 100, 120, 50)
rect.fillColor=colors.lightcoral
draw.add(rect)
my_title = String(doc.width/4+6, 135, 'Total Investment', fontSize=16)
my_title.fillColor=colors.white
draw.add(my_title)
my_title = String(doc.width/4+15, 110, '$'+str(Investment), fontSize=20)
my_title.fillColor=colors.white
draw.add(my_title)
story.append(draw)
#chart = pie_chart_with_legend(doc)
#story.append(chart)

story.append(FrameBreak())
story.append(Spacer(0,75))


draw = Drawing(200, 150)
rect=Rect(40, 112, 120, 50)
rect.fillColor=colors.orange
draw.add(rect)

my_title = String(41, 145, 'Current Valuation', fontSize=16)
my_title.fillColor=colors.white
draw.add(my_title)
my_title = String(55, 122, '$'+str(Valuation), fontSize=20)
my_title.fillColor=colors.white
draw.add(my_title)
story.append(draw)


story.append(Paragraph("This is a paragrfjvhhhhhhnjhhhhhhhhhhhhhhhhhhhhhhhhhhhkhvdsssssssssssssssssstrdktcjhvjhvgtfycgkvjhbhbhguvgvjbhjbhbkkjnkjnjigvhjbiugvjhhgyujbuyugfghvbjuytfgcvbjkiuytfgcnvbjkoiuytdfxvcbhbjyfdfxcgvhiu8y7ityhgaphgcjjjjjhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhjjjjjjjjjjjjjjjjjjjjjjjjfxhcjgkhbjbjhfvkfhvkbjvjcjjvgvjvh in <i>Normal</i> style. gik",styleN))

story.append(Paragraph("This is a paragrfjvhhhhhhnjhhhhhhhhhhhhhhhhhhhhhhhhhhhkhvdsssssssssssssssssstrdktcjhvjhvgtfycgkvjhbhbhguvgvjbhjbhbkkjnkjnjigvhjbiugvjhhgyujbuyugfghvbjuytfgcvbjkiuytfgcnvbjkoiuytdfxvcbhbjyfdfxcgvhiu8y7ityhgaphgcjjjjjhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhjjjjjjjjjjjjjjjjjjjjjjjjfxhcjgkhbjbjhfvkfhvkbjvjcjjvgvjvh in <i>Normal</i> style. gik",styleN))
story.append(Paragraph("This is a paragrfjvhhhhhhnjhhhhhhhhhhhhhhhhhhhhhhhhhhhkhvdsssssssssssssssssstrdktcjhvjhvgtfycgkvjhbhbhguvgvjbhjbhbkkjnkjnjigvhjbiugvjhhgyujbuyugfghvbjuytfgcvbjkiuytfgcnvbjkoiuytdfxvcbhbjyfdfxcgvhiu8y7ityhgaphgcjjjjjhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhjjjjjjjjjjjjjjjjjjjjjjjjfxhcjgkhbjbjhfvkfhvkbjvjcjjvgvjvh in <i>Normal</i> style. gik",styleN))


doc.addPageTemplates([coverPage,columnTemplate,])
doc.build(story)

