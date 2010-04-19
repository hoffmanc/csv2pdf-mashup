from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util
from dbimport import *

#for charts
#from pygooglechart import GroupedVerticalBarChart, Axis

#for doc
#import time
#from reportlab.lib.enums import TA_JUSTIFY
#from reportlab.lib.pagesizes import letter
#from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
#from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#from reportlab.lib.units import inch

class MainHandler(webapp.RequestHandler):

  def get(self):
    load_data()
    prec = {}
    site = {}
    all = {}
    cnt = 0
    lastp = None
    for p in SurveyResponse.all().order("preceptor_name"):
      try: 
        elem = prec[(p.preceptor_name, p.site_name, p.question_name)]
        elem[0] += p.choice_id 
        elem[1] += p.choice_id 
      except:
        prec[(p.preceptor_name, p.site_name, p.question_name)] = (p.choice_id, 1)
      try:
        elem = site[(p.site_name, p.question_name)]
        elem[0] += p.choice_id 
        elem[1] += p.choice_id 
      except:
        site[(p.site_name, p.question_name)] = (p.choice_id, 1)
      try:
        elem = all[p.question_name]
        elem[p.question_name] += p.choice_id
      except:
        all[p.question_name] = p.choice_id

    for p in prec:
      print ",".join(p)
      for q in all:
        elem = prec[(p[0], p[1], q)]
        avg = elem[0] / elem[1]
        self.response.out.write("%s: %s" % (q, avg))

def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()


"""
preceptors = conn.execute(select([stats.c.preceptor_name, stats.c.site_name
  ]).group_by(stats.c.preceptor_name, stats.c.site_name))

for p in preceptors:
  chart = GroupedVerticalBarChart(350, 200,
    y_range=(0,5))
  chart.set_bar_width(5)
  chart.set_bar_spacing(0)
  chart.set_group_spacing(4)
  chart.set_colours(['0772A1', 'FFB700', 'FF3100'])
  chart.set_grid(0, 20, 5, 5)
  
  left_axis = range(0, 6, 1)
  left_axis[0] = '' #interfers with first x label
  chart.set_axis_labels(Axis.LEFT, left_axis)

  prec = p[0]
  site = p[1]
  questions = conn.execute(select([stats.c.question_name, stats.c.order, func.avg(stats.c.choice_id)],
      stats.c.preceptor_name == prec
    ).group_by(stats.c.order, stats.c.question_name, 
    ).order_by(stats.c.order
    )).fetchall()
  ques_avgs = map(lambda q: q[2], questions)
  chart.add_data(ques_avgs)
  chart.set_axis_labels(Axis.BOTTOM, range(1,len(ques_avgs)+1))

  sites = conn.execute(select([stats.c.order, func.avg(stats.c.choice_id)],
      stats.c.site_name == site
    ).group_by(stats.c.order
    ).order_by(stats.c.order
    )).fetchall()
  sites = map(lambda s: s[1], sites)
  chart.add_data(sites)

  all = conn.execute(select([stats.c.order, func.avg(stats.c.choice_id)],
    ).group_by(stats.c.order
    ).order_by(stats.c.order
    )).fetchall()
  all = map(lambda a: a[1], all)
  chart.add_data(all)

  chart.download('preceptorReport.png')

  doc = SimpleDocTemplate(
    "preceptor-report-%s.pdf" % prec,pagesize=letter,
    rightMargin=72,leftMargin=72,
    topMargin=72,bottomMargin=18
  )
  
  styles=getSampleStyleSheet()
  styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

  Story=[]
  logo = "preceptorReport.png"
 
  ptext = '<font size=12>%s</font>' % "Preceptor Report"
  Story.append(Paragraph(ptext, styles["Normal"]))
  ptext = '<font size=12>%s</font>' % prec
  Story.append(Paragraph(ptext, styles["Normal"]))
  ptext = '<font size=12>%s</font>' % time.strftime('%m-%d-%y')
  Story.append(Paragraph(ptext, styles["Normal"]))
  Story.append(Spacer(1, 12))

  Story.append(Image(logo))

  qcnt = 1
  for q in questions:
    Story.append(Paragraph(
      "%d. %s" % (qcnt, q[0]),
      styles["Normal"]
    ))
    qcnt+= 1

  Story.append(Spacer(1, 12))
  Story.append(Paragraph(""
    Hello.  Here is your report.  Please contact us for more information.
    Thank you.
The result is three paragraphs, each half an inch apart and in a different color.

Platypus provides a huge benefit over the pdfgen module when it comes to quickly and efficiently generating dynamic documents. Consider this script, which takes the contents of a simple text file and generates a PDF document:
"",
    styles["Normal"]
  ))
 
  doc.build(Story)
"""
