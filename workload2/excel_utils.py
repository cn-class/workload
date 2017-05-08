#!/usr/bin/python
# -*- coding: utf-8 -*-
import StringIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min

from .models import Thesis


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
    worksheet_s.merge_range('A2:E2', title_text, title)

    # write header
    worksheet_s.merge_range('A4:E4',ugettext(u"การคุมโครงงาน/วิทยานิพนธ์"))
    worksheet_s.write(4, 0, ugettext(u"ชื่อโครงงาน/วิทยานิพนธ์"), header)
    worksheet_s.write(4, 1, ugettext(u"ชื่อนักศึกษา"), header)
    worksheet_s.write(4, 2, ugettext(u"สัดส่วนการสอน"), header)
    worksheet_s.write(4, 3, ugettext(u"ระดับ"), header)
    worksheet_s.write(4, 4, ugettext(u"ประเภทโครงการ"), header)
    worksheet_s.write(4, 5, ugettext(u"หมายเหตุ"), header)
    

    # column widths
    thesis_col_width = 35
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):
        row = 5 + idx

        thesis_name = data.thesis_name.replace('\r','')
        worksheet_s.write_string(row, 0, thesis_name, cell_center)
        thesis_rows = compute_row(thesis_name,thesis_col_width)
        worksheet_s.set_row(row,15 * thesis_rows)

        student_name = data.student_name.replace('\r','')
        worksheet_s.write_string(row, 1, student_name, cell_center)
        student_rows = compute_row(student_name,thesis_col_width)
        worksheet_s.set_row(row,15 * student_rows)

        worksheet_s.write_number(row, 2, data.ratio, cell_center)
        worksheet_s.write_string(row, 3, data.degree, cell_center)
        worksheet_s.write_string(row, 4, data.program_ID, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_s.write_string(row, 5, comment, cell_center)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_s.set_row(row,15 * comment_rows)

        

    # change column widths
    worksheet_s.set_column('A:A', thesis_col_width)  # thesis_name column
    worksheet_s.set_column('B:B', thesis_col_width)  # thesis_name column
    worksheet_s.set_column('C:C', 11)  # ratio column
    worksheet_s.set_column('D:D', 15)  # degree column
    worksheet_s.set_column('E:E', 30)  # program_ID column
    worksheet_s.set_column('F:F', comment_col_width)  # comment column

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
    worksheet_s.merge_range('A2:E2', title_text, title)

    # write header
    worksheet_s.merge_range('A4:E4',ugettext(u"การคุมโครงงาน/วิทยานิพนธ์"))
    worksheet_s.write(4, 0, ugettext(u"ชื่อโครงงาน/วิทยานิพนธ์"), header)
    worksheet_s.write(4, 1, ugettext(u"ชื่อนักศึกษา"), header)
    worksheet_s.write(4, 2, ugettext(u"สัดส่วนการสอน"), header)
    worksheet_s.write(4, 3, ugettext(u"ระดับ"), header)
    worksheet_s.write(4, 4, ugettext(u"ประเภทโครงการ"), header)
    worksheet_s.write(4, 5, ugettext(u"หมายเหตุ"), header)
    worksheet_s.write(4, 6, ugettext(u"user"), header)
    

    # column widths
    thesis_col_width = 35
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):
        row = 5 + idx

        thesis_name = data.thesis_name.replace('\r','')
        worksheet_s.write_string(row, 0, thesis_name, cell_center)
        thesis_rows = compute_row(thesis_name,thesis_col_width)
        worksheet_s.set_row(row,15 * thesis_rows)

        student_name = data.student_name.replace('\r','')
        worksheet_s.write_string(row, 1, student_name, cell_center)
        student_rows = compute_row(student_name,thesis_col_width)
        worksheet_s.set_row(row,15 * student_rows)

        worksheet_s.write_number(row, 2, data.ratio, cell_center)
        worksheet_s.write_string(row, 3, data.degree, cell_center)
        worksheet_s.write_string(row, 4, data.program_ID, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_s.write_string(row, 5, comment, cell_center)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_s.set_row(row,15 * comment_rows)

        worksheet_s.write_string(row, 6, data.user.username, cell_center)
        

    # change column widths
    worksheet_s.set_column('A:A', thesis_col_width+5)  # thesis_name column
    worksheet_s.set_column('B:B', thesis_col_width+5)  # thesis_name column
    worksheet_s.set_column('C:C', 11+5)  # ratio column
    worksheet_s.set_column('D:D', 15+5)  # degree column
    worksheet_s.set_column('E:E', 30+5)  # program_ID column
    worksheet_s.set_column('F:F', comment_col_width+5)  # comment column
    worksheet_s.set_column('G:G', 15+5)

    row = row + 1

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data




def compute_row(text,width):
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