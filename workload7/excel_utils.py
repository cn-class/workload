#!/usr/bin/python
# -*- coding: utf-8 -*-
import StringIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min

from .models import Benefit


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
    worksheet_s.merge_range('A2:C2', title_text, title)

    # write header
    worksheet_s.merge_range('A4:C4',ugettext(u"รางวัลต่างๆ"))
    worksheet_s.write(4, 0, ugettext(u"รายการ"), header)
    worksheet_s.write(4, 1, ugettext(u"ชื่อผลงาน"), header)
    worksheet_s.write(4, 2, ugettext(u"หมายเหตุ"), header)
    

    # column widths
    benefit_name_col_width = 50
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):
        row = 5 + idx
        worksheet_s.write_string(row, 0, data.benefit_list, cell_center)

        benefit_name = data.benefit_name.replace('\r','')
        worksheet_s.write_string(row, 1, benefit_name, cell_center)
        benefit_name_rows = compute_row(benefit_name,benefit_name_col_width)
        worksheet_s.set_row(row,15 * benefit_name_rows)

        comment = data.comment.replace('\r','')
        worksheet_s.write_string(row, 2, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        print(comment_rows)
        worksheet_s.set_row(row,15 * comment_rows)

        
    # change column widths
    worksheet_s.set_column('A:A', benefit_name_col_width)  # benefit_name column
    worksheet_s.set_column('B:B', benefit_name_col_width)  # benefit_name column
    worksheet_s.set_column('C:C', comment_col_width)  # ratio column


    row = row + 1
    #Adding some function

    # lecture_sum = Teaching.objects.filter(user=current_user).aggregate(Sum('num_of_lecture'))
    # worksheet_s.write_formula(row, 3,
    #                           '=sum({0}{1}:{0}{2})'.format('D', 6, row),
    #                           cell_center,
    #                           lecture_sum['num_of_lecture__sum'])

    # lab_sum = Teaching.objects.filter(user=current_user).aggregate(Sum('num_of_lab'))
    # worksheet_s.write_formula(row, 4,
    #                           '=sum({0}{1}:{0}{2})'.format('E', 6, row),
    #                           cell_center,
    #                           lab_sum['num_of_lab__sum'])

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