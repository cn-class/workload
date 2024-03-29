#!/usr/bin/python
# -*- coding: utf-8 -*-
import StringIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min

from .models import Research


def WriteToExcel(query_data,current_user):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Summary")

    # excel styles
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })


    # write title
    
    title_text = u"{0} {1}".format(ugettext("Report"), current_user)
    # merge cells
    worksheet_s.merge_range('A2:G2', title_text, title)

    # write header
    worksheet_s.merge_range('A4:H4',ugettext(u"งานวิจัยและงานสร้างสรรค์"))
    worksheet_s.write(4, 0, ugettext(u"ชื่อผลงาน"), header)
    worksheet_s.write(4, 1, ugettext(u"ชื่อผู้แต่งร่วม"), header)
    worksheet_s.write(4, 2, ugettext(u"ชื่อวารสารที่ตีพิมพ์"), header)
    worksheet_s.write(4, 3, ugettext(u"ปี พ.ศ. ที่ตีพิมพ์"), header)
    worksheet_s.write(4, 4, ugettext(u"สัดส่วน"), header)
    worksheet_s.write(4, 5, ugettext(u"ประเภท"), header)
    worksheet_s.write(4, 6, ugettext(u"หมายเหตุ"), header)
    

    # column widths
    research_col_width = 20
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):

        row = 5 + idx

        research_name = data.research_name.replace('\r','')
        worksheet_s.write_string(row, 0, research_name, cell_center)
        research_rows = compute_rows(research_name,research_col_width)
        worksheet_s.set_row(row, 15 * research_rows)

        worksheet_s.write_string(row, 1, data.assist_name, cell_center)
        worksheet_s.write_string(row, 2, data.journal_name, cell_center)
        worksheet_s.write_number(row, 3, data.year, cell_center)
        worksheet_s.write_number(row, 4, data.ratio, cell_center)
        worksheet_s.write_string(row, 5, data.degree, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_s.write_string(row, 6, comment, cell)
        comment_rows = compute_rows(comment,comment_col_width)
        worksheet_s.set_row(row,15 * comment_rows)

        

    # change column widths
    worksheet_s.set_column('A:A', research_col_width)  # thesis_name column
    worksheet_s.set_column('B:B', 10+5)  # assist column
    worksheet_s.set_column('C:C', 12+5)  # journal column
    worksheet_s.set_column('D:D', 12+5)  # year column
    worksheet_s.set_column('E:E', 8+5)  # ratio column
    worksheet_s.set_column('F:F', 20+5)  # degree column
    worksheet_s.set_column('G:G', comment_col_width+5)  # comment column

    row = row + 1

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data

def WriteToExcelManager(query_data,current_user):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Summary")

    # excel styles
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })


    # write title
    
    title_text = u"{0} {1}".format(ugettext("Report"), current_user)
    # merge cells
    worksheet_s.merge_range('A2:G2', title_text, title)

    # write header
    worksheet_s.merge_range('A4:H4',ugettext(u"งานวิจัยและงานสร้างสรรค์"))
    worksheet_s.write(4, 0, ugettext(u"ชื่อผลงาน"), header)
    worksheet_s.write(4, 1, ugettext(u"ชื่อผู้แต่งร่วม"), header)
    worksheet_s.write(4, 2, ugettext(u"ชื่อวารสารที่ตีพิมพ์"), header)
    worksheet_s.write(4, 3, ugettext(u"ปี พ.ศ. ที่ตีพิมพ์"), header)
    worksheet_s.write(4, 4, ugettext(u"สัดส่วน"), header)
    worksheet_s.write(4, 5, ugettext(u"ประเภท"), header)
    worksheet_s.write(4, 6, ugettext(u"หมายเหตุ"), header)
    worksheet_s.write(4, 7, ugettext(u"user"), header)
    

    # column widths
    research_col_width = 20
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):

        row = 5 + idx

        research_name = data.research_name.replace('\r','')
        worksheet_s.write_string(row, 0, research_name, cell_center)
        research_rows = compute_rows(research_name,research_col_width)
        worksheet_s.set_row(row, 15 * research_rows)

        worksheet_s.write_string(row, 1, data.assist_name, cell_center)
        worksheet_s.write_string(row, 2, data.journal_name, cell_center)
        worksheet_s.write_number(row, 3, data.year, cell_center)
        worksheet_s.write_number(row, 4, data.ratio, cell_center)
        worksheet_s.write_string(row, 5, data.degree, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_s.write_string(row, 6, comment, cell)
        comment_rows = compute_rows(comment,comment_col_width)
        worksheet_s.set_row(row,15 * comment_rows)

        worksheet_s.write_string(row, 7, data.user.username, cell_center)

        

    # change column widths
    worksheet_s.set_column('A:A', research_col_width)  # thesis_name column
    worksheet_s.set_column('B:B', 10+5)  # assist column
    worksheet_s.set_column('C:C', 12+5)  # journal column
    worksheet_s.set_column('D:D', 12+5)  # year column
    worksheet_s.set_column('E:E', 8+5)  # ratio column
    worksheet_s.set_column('F:F', 20+5)  # degree column
    worksheet_s.set_column('G:G', comment_col_width+5)  # comment column
    worksheet_s.set_column('H:H', 15+5)

    row = row + 1

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


def compute_rows(text,width):
    if len(text) < width:
        return 1

    pharses = text.replace('\r','').split('\n')

    rows = 0
    for pharse in pharses:
        if len(pharse) < width:
            rows = rows + 1
        else:
            words = pharse.split(' ')
            temp = ''
            for idx,word in enumerate(words):
                temp = temp + word + ' '
                # check if column width exceeded
                if len(temp) > width:
                    rows = rows + 1
                    temp = '' + word + ' '
                # check if it is not the lastword
                if idx == len(words) - 1 and len(temp) > 0:
                    rows = rows + 1

    return rows