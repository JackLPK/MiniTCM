import tempfile
from copy import deepcopy
from pathlib import Path
from pprint import pprint

import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import (TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY)

from minitcm import FONTS_DIR, PDFS_DIR, TEMPLATES_DIR

# asian fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('han', (FONTS_DIR / 'SourceHanSerif' / 'SourceHanSerif-Regular.ttc').as_posix()))


P = Paragraph
PS = ParagraphStyle


class MyPDF:
    def __init__(self, fp, data, debug=False):
        self.data = data
        self.debug = debug
        self.width, self.height = A4
        self.doc = self._get_doc(fp)
        self.BFS = 14    # base fontsize
        self.font_name = 'han'
        self.margin = 1 * cm
        self.inner_w = self.width - self.margin*2
        self.inner_h = self.height - self.margin * 2
        self.base_ps = self._get_base_ps()
        self.story = []

    def run(self):
        self.story.extend(self._section_1())
        self.story.extend(self._section_2())
        self.story.extend(self._section_3())

        self.doc.build(self.story, self._first_page)


    def _get_doc(self, fp):
        cfg = {
            'pagesize': A4,
            'leftMargin': cm, 'rightMargin': cm, 'topMargin': cm, 'bottomMargin': cm,
            'showBoundary': 1 if self.debug else 0,
        }
        return SimpleDocTemplate(fp.as_posix(), **cfg)

    def _get_base_ps(self):
        cfg = {'fontName': self.font_name, **self._fsl(self.BFS), 'alignment': TA_CENTER }
        return ParagraphStyle('base', getSampleStyleSheet()['Normal'], **cfg)

    def _fsl(self, size):
        """ fontsize and leading """
        return {'fontSize': size, 'leading': size*1.5}

    def _section_1(self):
        ps1 = ParagraphStyle('title', self.base_ps, **self._fsl(self.BFS * 2))
        p1 = Paragraph(self.data['doctor']['organisation'], ps1)

        ps2 = ParagraphStyle('title', self.base_ps, **self._fsl(self.BFS * 1.5))
        p2 = Paragraph(self.data['script']['subtitle'], ps2)

        return [p1, p2, ]
        return [p1, Spacer(1, 0.4*cm), p2, ]

    def _section_2(self):

        def section_2a():
            pd = self.data['patient']

            t_style = TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'han'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('LINEBELOW', (1, 0), (1, 0), 1, colors.black),    # border-bottom
                ('LINEBELOW', (3, 0), (3, 0), 1, colors.black),    # border-bottom
            ])
            t_style.add('GRID', (0, 0), (-1, -1), 0.1, colors.gray) if self.debug else None

            # row 1
            ts_1 = TableStyle([
                ('LINEBELOW', (5, 0), (5, 0), 1, colors.black),    # border-bottom
                ], t_style)

            data = self._row_p(
                ['姓名：', pd['name'], '性別：', pd['gender'], '年龄：', pd['age']],
                self.base_ps
            )

            cw = [self.inner_w/9, self.inner_w/9*2] * 3
            t1 = Table(data, colWidths=cw, style=ts_1, hAlign='CENTER')

            # row 2
            ts_2 = TableStyle([], t_style)

            data = self._row_p(
                ['聯絡：', pd['contact'],
                '日期：', self.data['script']['date'].replace('T', ' ')
                ], self.base_ps)

            cw = [self.inner_w/6, self.inner_w/6*2] * 2
            t2 = Table(data, colWidths=cw, style=ts_2, hAlign='CENTER')

            return [t1, t2, ]

        def section_2b():
            nd = self.data['notes']
            name_ps = PS('label', self.base_ps, alignment=TA_RIGHT)
            content_ps = PS('content', self.base_ps, alignment=TA_LEFT)
            data = [[P(note['name'], name_ps), P(note['content'], content_ps)] for note in nd]

            t_style = TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'han'),
                ('LINEBELOW', (1, 0), (-1, -1), 2, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])
            if self.debug :
                t_style.add('GRID', (0, 0), (-1, -1), 0.1, colors.gray)

            # pprint(data)
            cw = [self.inner_w*0.2, self.inner_w*0.8]
            table = Table(data, colWidths=cw, style=t_style, hAlign='CENTER')
            return [table, ]

        return [*section_2a(), *section_2b()]

    def _row_p(self, data, ps):
        return [[P(str(t), ps) for t in data]]

    def _section_3(self):
        def to_2d(data, N=3, f_deco=None):
            retval = []
            data_c = deepcopy(data)
            while len(data_c) > 0:
                tli = []
                for _i in range(N):
                    val = data_c.pop(0) if len(data_c) > 0 else None
                    val = val if (None in (val, f_deco)) else f_deco(val)
                    tli.append(val) if val is not None else None
                retval.append(tli)
            return retval

        def deco(unit, ps):
            def inner(obj):
                text = '{} {} {}'.format(obj['name'], obj['mass'], unit)
                return Paragraph(text, ps)
            return inner

        t_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'han'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        t_style.add('GRID', (0, 0), (-1, -1), 0.1, colors.gray) if self.debug else None
        t3_cw = [self.inner_w/3 for i in range(3)]

        t3 = Table(to_2d(self.data['meds'], 3, deco('g', self.base_ps)), colWidths=t3_cw, style=t_style, hAlign='CENTER')
        img = Image((TEMPLATES_DIR / 'Rp.png').as_posix(), width=1.2*cm, height=1.2*cm, hAlign='LEFT')
        return (img, t3, )

    def _first_page(self, canvas:Canvas, document):

        PORTION = 10
        h_delta = self.height / (PORTION)
        w_delta = self.width / (PORTION)

        h_lines = [i * h_delta for i in range(PORTION+1)]
        w_lines = [i * w_delta for i in range(PORTION+1)]

        def footer():
            ps = PS('footer1', self.base_ps, alignment=TA_LEFT)
            text_1 = '{}: {}<br/>{}<br/>{}: {}'.format(
                '貼數', self.data['script']['dosage'],
                self.data['script']['footer'],
                '医生', self.data['doctor']['name'],
            )

            p = P(text_1, ps)
            p.wrapOn(canvas, self.inner_w, self.inner_h)
            p.drawOn(canvas, 1.5*cm, 1.5*cm)

        def category():
            ps = PS('category', self.base_ps, borderWidth=0.02*cm, borderColor=colors.black)
            text = self.data['script']['category']
            p = P(text, ps)
            p.wrapOn(canvas, 4*cm, 4*cm)
            p.drawOn(canvas, w_lines[7], h_lines[9])

        def script_id():
            ps = PS('id', self.base_ps, borderWidth=0.02*cm, borderColor=colors.black)
            text = f"{self.data['script']['id']:09}"
            p = P(text, ps)
            p.wrapOn(category, 4*cm, 4*cm)
            p.drawOn(canvas, w_lines[1], h_lines[9])

        def grids():
            canvas.saveState()

            canvas.setStrokeColor(colors.green)
            [canvas.line(0, h, self.width, h) for h in h_lines]
            [canvas.drawString(0, h, f'{i}') for i, h in enumerate(h_lines)]

            canvas.setStrokeColor(colors.red)
            [canvas.line(w, 0, w, self.height) for w in w_lines]
            [canvas.drawString(w, 0, f'{i}') for i, w in enumerate(w_lines)]

            canvas.restoreState()

        #
        if self.debug:
            grids()
        footer()
        category()
        script_id()

def create_pdf(fp=None, obj=None, temp=False):
    """ expect python dictionary """
    if not obj:
        from sample_data import sample_export_data as obj

    if fp is not None:
        MyPDF(fp, obj['data'], False).run()
        return fp

    elif fp is None and temp is False:
        fp = PDFS_DIR / 'testoop.pdf'
        MyPDF(fp, obj['data'], False).run()

    elif fp is None and temp is True:
        _handl, fp_str = tempfile.mkstemp(suffix='.pdf')
        MyPDF(Path(fp_str), obj['data'], False).run()
        return Path(fp_str).resolve()

    else:
        raise Exception('error at tempfiles')
