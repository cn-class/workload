#!/usr/bin/python
# -*- coding: utf-8 -*-
import StringIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min

from .models import Support


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
    worksheet_s.merge_range('A4:E4',ugettext(u"งานสนับสนุนการจัดการศึกษา"))
    worksheet_s.write(4, 0, ugettext(u"รายการ"), header)
    worksheet_s.write(4, 1, ugettext(u"ระดับ"), header)
    worksheet_s.write(4, 2, ugettext(u"ประเภท"), header)
    worksheet_s.write(4, 3, ugettext(u"หมายเหตุ"), header)

    # column widths
    support_list_col_width = 40
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):
        row = 5 + idx

        support_list = data.support_list.replace('\r','')
        worksheet_s.write_string(row, 0, support_list, cell_center)
        support_list_rows = compute_row(support_list,support_list_col_width)
        worksheet_s.set_row(row,15 * support_list_rows)

        worksheet_s.write_string(row, 1, data.degree, cell_center)
        worksheet_s.write_string(row, 2, data.kind, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_s.write_string(row, 3, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_s.set_row(row,15 * comment_rows)

    # change column widths
    worksheet_s.set_column('A:A', support_list_col_width+5)  # subject column
    worksheet_s.set_column('B:B', 15+5)  # subject column
    worksheet_s.set_column('C:C', 15+5)  # ratio column
    worksheet_s.set_column('D:D', comment_col_width+5)  # comment column

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
    worksheet_s.merge_range('A4:E4',ugettext(u"งานสนับสนุนการจัดการศึกษา"))
    worksheet_s.write(4, 0, ugettext(u"รายการ"), header)
    worksheet_s.write(4, 1, ugettext(u"ระดับ"), header)
    worksheet_s.write(4, 2, ugettext(u"ประเภท"), header)
    worksheet_s.write(4, 3, ugettext(u"หมายเหตุ"), header)
    worksheet_s.write(4, 4, ugettext(u"user"), header)

    # column widths
    support_list_col_width = 40
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):
        row = 5 + idx

        support_list = data.support_list.replace('\r','')
        worksheet_s.write_string(row, 0, support_list, cell_center)
        support_list_rows = compute_row(support_list,support_list_col_width)
        worksheet_s.set_row(row,15 * support_list_rows)

        worksheet_s.write_string(row, 1, data.degree, cell_center)
        worksheet_s.write_string(row, 2, data.kind, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_s.write_string(row, 3, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_s.set_row(row,15 * comment_rows)

        worksheet_s.write_string(row, 4, data.user.username, cell_center)

        
    # change column widths
    worksheet_s.set_column('A:A', support_list_col_width+5)  # subject column
    worksheet_s.set_column('B:B', 15+5)  # subject column
    worksheet_s.set_column('C:C', 15+5)  # ratio column
    worksheet_s.set_column('D:D', comment_col_width+5)  # comment column
    worksheet_s.set_column('E:E', 15+5)

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