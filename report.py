from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.validators import Auto
from reportlab.graphics.charts.legends import Legend, LineLegend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String, Rect
from datetime import date

from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.axes import XValueAxis, YValueAxis, AdjYValueAxis, NormalDateXValueAxis
from reportlab.platypus import Paragraph, SimpleDocTemplate,Image, PageTemplate, Frame, PageBreak, FrameBreak, Spacer, NextPageTemplate, HRFlowable, Table, TableStyle
import random





def generatePDF(FI,Equity,Investment,Valuation,monthlyInv,monthlyVal,portfolioHoldings,tab_data,tab_data1):
    
    logo= 'AIM_logo.jpg'
    portfolioDate= date.today()
    months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleContent= ParagraphStyle(name='content', parent=styles['Normal'], fontSize=18, leading=35)
    styleH = styles['Heading1']
    style_right = ParagraphStyle(name='right', parent=styles['Heading1'], alignment=TA_RIGHT, fontSize=24)
    style_center= ParagraphStyle(name='center', parent=styles['Normal'], alignment=TA_CENTER, fontSize=16, leading=35)

    story = []
    doc = SimpleDocTemplate('portfolio.pdf',pagesize = landscape(A4),rightMargin=30,leftMargin=30,topMargin=30, bottomMargin=30)

    myFrame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='myFrame')
    frame1=Frame(doc.leftMargin, doc.bottomMargin,doc.width/2-6, doc.height, id='col1')
    frame2=Frame(doc.leftMargin+doc.width/2+6,doc.bottomMargin,doc.width/2-6, doc.height, id='col2')
    frame3=Frame(doc.leftMargin, doc.bottomMargin,doc.width, doc.height/2, id='col3')
    coverPage=PageTemplate(id='Cover', frames=[myFrame])
    threeTemplate=PageTemplate(id='ThreeSec',frames=[frame1,frame2,frame3])
    columnTemplate=PageTemplate(id='TwoCol',frames=[frame1,frame2])


    #Page 1
    story.append(Image(logo, 2*inch, 2*inch, hAlign='RIGHT'))
    story.append(Spacer(0,10))
    story.append(Paragraph("CLIENT  PORTFOLIO",style_right))
    story.append(HRFlowable(width='100%', thickness=5, color=colors.navy))
    story.append(Spacer(0,15))

    story.append(Paragraph("TABLE OF CONTENTS",ParagraphStyle(name='content', parent=styles['Normal'], fontSize=18, leading=35)))

    story.append(Paragraph("Investment Value"+"."*104+"1",styleN))
    story.append(Spacer(0,15))
    story.append(Paragraph("Portfolio Holdings"+"."*103+"2",styleN))
    story.append(Spacer(0,15))
    story.append(Paragraph("Net Position"+"."*112+"4",styleN))
    story.append(Spacer(0,15))

    story.append(NextPageTemplate('ThreeSec'))
    story.append(PageBreak())

    #Page 2
    story.append(Paragraph("Investment Value",styleH))
    story.append(Paragraph("As of "+str(portfolioDate),styleContent))

    #Frame1
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

    story.append(FrameBreak())

    #Frame 2
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

    story.append(FrameBreak())

    #Frame 3
    lineChart = line_chart(doc,months,portfolioDate,monthlyInv,monthlyVal,Valuation,Investment)
    story.append(lineChart)

    story.append(NextPageTemplate('TwoCol'))
    story.append(PageBreak())


    # Page 3

    story.append(Paragraph("Portfolio Holdings",styleH))
    story.append(Paragraph("As of "+str(portfolioDate),styleContent))

    story.append(Spacer(0,70))
    story.append(Paragraph("Summary of Portfolio Holdings",style_center))


    style=TableStyle([('BACKGROUND',(0,-1),(-1,-1),colors.whitesmoke),('ALIGN',(1,0),(-1,-1),'CENTER'),('FONTSIZE',(0,0),(-1,-1),8),('BODYTEXT',(0,0),(-1,-1),'TEXTWRAP'),('LINEABOVE',(0,0),(-1,1),1,colors.black)])

    table1=Table(portfolioHoldings)
    table1.setStyle(style)
    story.append(table1)

    story.append(FrameBreak())

    #Frame2
    chart = pie_chart_with_legend(doc,FI,Equity)
    story.append(chart)


    #Page 4
    story.append(PageBreak())
    story.append(Paragraph("Details of portfolio holdings",styleH))
    story.append(Paragraph("As of "+str(portfolioDate),styleContent))
    story.append(Spacer(0,20))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.black))

    style=TableStyle([('BACKGROUND',(0,1),(-1,1),colors.whitesmoke),('ALIGN',(1,0),(-1,-1),'CENTER'),('FONTSIZE',(0,0),(-1,-1),8),('BODYTEXT',(0,0),(-1,-1),'TEXTWRAP')])

    table=Table(tab_data)
    table.setStyle(style)
    story.append(table)

    #page 5
    story.append(PageBreak())
    story.append(Paragraph("Net Position",styleH))
    story.append(Paragraph("As of "+str(portfolioDate),styleContent))
    story.append(Spacer(0,20))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.black))

    table1=Table(tab_data1)
    table1.setStyle(style)
    story.append(table1)


    doc.addPageTemplates([coverPage,threeTemplate, columnTemplate,])
    doc.build(story)




def add_legend(draw_obj, chart, data,doc):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 100
    legend.y = -110
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)

def pie_chart_with_legend(doc,FI,Equity):
    data=['Fixed Income ('+str(FI[6])+'%)','Equity ('+str(Equity[6])+'%)']
    drawing = Drawing(width=doc.width/2, height=250)
    my_title = String(140, -70, 'Asset-wise Allocation', fontSize=14)
    pie = Pie()
    pie.sideLabels = False
    pie.slices.label_visible = False
    pie.x = 100
    pie.y = -40
    pie.width=200
    pie.height=200
    pie.data = [FI[6],Equity[6]]
    pie.labels = data
    pie.slices.strokeWidth = 0.5
    drawing.add(my_title)
    drawing.add(pie)
    add_legend(drawing, pie, data,doc)
    return drawing

def add_legend1(draw_obj, chart, data, doc):
    legend = LineLegend()
    legend.alignment = 'right'
    legend.x = doc.leftMargin
    legend.y = doc.bottomMargin-30
   
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)

def line_chart(doc,months,portfolioDate,monthlyInv,monthlyVal,Valuation,Investment):
    drawing = Drawing(doc.width/2, doc.height/2-80)
    data = [
     monthlyInv,
     monthlyVal
    ]
    my_title = String(doc.width/2-90, doc.height/2, 'Performance Chart', fontSize=20)

    lc = HorizontalLineChart()
    lc.x = doc.leftMargin+35
    lc.y = doc.bottomMargin
    lc.height = doc.height/2-60
    lc.width = doc.width-100
    
    lc.data = data
    lc.joinedLines = 1
    catNames=months[portfolioDate.month:]
    
    if portfolioDate.month>1:
        catNames+=months[:portfolioDate.month]

    lc.categoryAxis.categoryNames = catNames
    #lc.categoryAxis.labels.boxAnchor = 'autox'
    lc.valueAxis.valueMin = 0
    roundedVal= Valuation if Valuation%10==0 else Valuation+Valuation%10
    lc.valueAxis.valueMax = roundedVal
    lc.valueAxis.valueStep=int((roundedVal/10)/10)*10
    lc.lines[0].strokeWidth = 2
    lc.lines[1].strokeWidth = 1.5
    lc.lines[0].strokeColor= colors.blue
    lc.lines[1].strokeColor= colors.green if Valuation>Investment else colors.red
    lc.valueAxis.visibleGrid=1
    lc.valueAxis.gridStrokeColor=colors.lightgrey

    lc.lines[0].name = 'Investment Value'
    lc.lines[1].name = 'Closing Valuation'
    #lc.lineLabelFormat = '%2.0f'
    labels=['Investment Value','Closing Valuation']
    lc._seriesCount = len(labels)

    drawing.add(my_title)
    drawing.add(lc)
    add_legend1(drawing, lc, labels,doc)
    
    return drawing



FI=[4531082, 4892169, 206462, 4.56, 217467, 4.45, 45.94]
Equity=[5218922,5362021.34,-62131.35,-1.19,117832,2.2,50.36]

Investment=225323
Valuation=865489
monthlyInv=[23564,5782,84,79765,3243,65799,43344,5668,43,78900,3456,7543]
monthlyVal=[85265,578954,8656,87533,29754,264256,23244,23435,243234,5767,576854,574321]
portfolioHoldings=[
    ['','Cost basis($)','Value on\n'+str(date.today()), 'Unrealized\ngain/loss($)', 'Unrealized\ngain/loss(%)','Est. annual\nincome($)','Current\nyield(%)','% of\nPortfolio'],
    ['Fixed Income']+FI,
    ['Equity']+Equity,
    ['Total Portfolio']+[ round(a+b,2) for (a,b) in zip(FI,Equity) ]
]


#Page 4 data
tab_data=[
      ['','','','','Cost basis($)','Market Value($)','Unrealized \n gain/loss($)','Unrealized \n gain/loss(%)','Est. annual \n income($)','Current yield(%)','% of asset\n class','% of portfolio']
      ,['Total Portfolio','','','','$9,967,814.44','$10,648,193.73','$145,102.43','1.46%','$336,076.01','3.16%','100%',]
      ,['Cash','Quantity','Purchase price($) \n /Avg price','Price on \n'+str(date.today()),'Cost basis($)','Market Value($)','Unrealized\n gain/loss ($)','Unrealized \ngain/loss(%)','Est. annual \nincome($)','Current yield(%)','% of cash','% of portfolio']
      ,['UBS BANK USA \n DEPOSIT ACCOUNT','179,478.88','1.00','1.00','179,478.88','179,478.88','0.00','0.00%','85.32%','1.69%']
      ,['*FIRST EAGLE\n GLOBAL FUND CLASS C','','','1.00','5,867.17','6,681.39','814.22','13.88%','35.61%','','3.18%','0.06%']
      ,['*GOLDMAN SACHS ASSET\n ALLOCATION GROWTH\n STRATEGY FUND CL A','','','1.00','18,770.90','17,544.77','-1,226.13','-6.53%','244.21','','8.34%','0.16%']
      ,['TOTAL CASH','','','','$209,804.94','$210,353.44','$548.48','0.26%','$281.49','0.13%','100.00%','1.98%']
]
#Page 5 data
tab_data1=[
      ['','','','','Cost basis($)','Market Value($)','Unrealized gain/loss ($)','Unrealized gain/loss(%)','Est. annual income($)','Current yield(%)','% of asset class','% of portfolio']
      ,['Total Portfolio','','','','$9,967,814.44','$10,648,193.73','$145,102.43','1.46%','$336,076.01','3.16%','100%','100%']
    ]

generatePDF(FI,Equity,Investment,Valuation,monthlyInv,monthlyVal,portfolioHoldings,tab_data,tab_data1)