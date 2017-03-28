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
    worksheet_s.merge_range('B2:I2', title_text, title)

    # write header
    worksheet_s.write(4, 0, ugettext("No"), header)
    worksheet_s.write(4, 1, ugettext(u"ชื่อวิชา"), header)
    worksheet_s.write(4, 2, ugettext(u"สัดส่วนการสอน"), header)
    worksheet_s.write(4, 3, ugettext(u"จำนวนหน่วยกิตการบรรยาย"), header)
    worksheet_s.write(4, 4, ugettext(u"จำนวนหน่วยกิตการปฏิบัติการ"), header)
    worksheet_s.write(4, 5, ugettext(u"ภาค"), header)
    worksheet_s.write(4, 6, ugettext(u"จำนวนนักศึกษา"), header)
    worksheet_s.write(4, 7, ugettext(u"สัดส่วนคะแนน"), header)
    worksheet_s.write(4, 8, ugettext(u"หมายเหตุ"), header)
    

    # column widths
    town_col_width = 10
    description_col_width = 10
    observations_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):
        row = 5 + idx
        worksheet_s.write_number(row, 0, idx + 1, cell_center)

        worksheet_s.write_string(row, 1, data.subject, cell)
        # if len(data.town.name) > town_col_width:
        #     town_col_width = len(data.town.name)

        worksheet_s.write_number(row, 2, data.ratio, cell_center)
        worksheet_s.write_number(row, 3, data.num_of_lecture, cell_center)
        # if len(data.description) > description_col_width:
        #     description_col_width = len(data.description)

        worksheet_s.write_number(row, 4, data.num_of_lab, cell_center)
        worksheet_s.write_string(row, 5, data.program_ID, cell_center)
        worksheet_s.write_number(row, 6, data.num_of_student, cell_center)
        worksheet_s.write_number(row, 7, data.ratio_of_score, cell_center)
        worksheet_s.write_string(row, 8, data.comment, cell_center)

        

    # change column widths
    worksheet_s.set_column('B:B', town_col_width)  # subject column
    worksheet_s.set_column('C:C', 11)  # ratio column
    worksheet_s.set_column('D:D', 17)  # num_of_lecture column
    worksheet_s.set_column('E:E', 18)  # num_of_lab column
    worksheet_s.set_column('F:F', 10)  # program column
    worksheet_s.set_column('G:G', 15)  # num_of_student column
    worksheet_s.set_column('H:H', 10)  # comment column
    worksheet_s.set_column('I:I', observations_col_width)  # comment column


    row = row + 1
    #Adding some function

    lecture_sum = Teaching.objects.filter(user=current_user).aggregate(Sum('num_of_lecture'))
    worksheet_s.write_formula(row, 3,
                              '=sum({0}{1}:{0}{2})'.format('D', 6, row),
                              cell_center,
                              lecture_sum['num_of_lecture__sum'])

    lab_sum = Teaching.objects.filter(user=current_user).aggregate(Sum('num_of_lab'))
    worksheet_s.write_formula(row, 4,
                              '=sum({0}{1}:{0}{2})'.format('E', 6, row),
                              cell_center,
                              lab_sum['num_of_lab__sum'])

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data