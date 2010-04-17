#for data
import csv,sys
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, MetaData, select, func, and_

#for charts
from pygooglechart import GroupedVerticalBarChart, Axis

#for doc
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

engine = create_engine('sqlite:///:memory:')
metadata = MetaData()
stats = Table('stats', metadata,
	Column('survey_id', Integer),
	Column('choice_id', Integer),
	Column('question_name', String),
	Column('order', Integer),
	Column('preceptor_id', Integer),
	Column('site_name', String),
)
metadata.create_all(engine)

reader = csv.reader(open( sys.argv[1], 'rb'), delimiter='\t')
headerrow = reader.next()
conn = engine.connect()

for row in reader:
	ins = stats.insert().values(
		survey_id = row[0],
		choice_id = row[1],
		question_name = row[2],
		order = row[3],
		preceptor_id = row[4],
		site_name = row[5],
	)
	conn.execute(ins)


preceptors = conn.execute(select([stats.c.preceptor_id, stats.c.site_name
	]).group_by(stats.c.preceptor_id, stats.c.site_name))

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
			stats.c.preceptor_id == prec
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
	Story.append(Paragraph("""
		Hello.  Here is your report.  Please contact us for more information.
		Thank you.
The result is three paragraphs, each half an inch apart and in a different color.

Platypus provides a huge benefit over the pdfgen module when it comes to quickly and efficiently generating dynamic documents. Consider this script, which takes the contents of a simple text file and generates a PDF document:
""",
		styles["Normal"]
	))
 
	doc.build(Story)
