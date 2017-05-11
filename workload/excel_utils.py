#!/usr/bin/python
# -*- coding: utf-8 -*-
import StringIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min

from .models import Teaching


def WriteToExcel(query_data,current_user,score):
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
    worksheet_s.merge_range('A2:I2', title_text, title)

    # write header
    worksheet_s.merge_range('A3:I3',ugettext(u"งานสอน"))
    worksheet_s.merge_range('D4:E4',ugettext(u"จำนวนหนว่ยกิตการ"),header)
    worksheet_s.write(4, 0, ugettext(u"รหัสวิชา"), header)
    worksheet_s.write(4, 1, ugettext(u"ชื่อวิชา"), header)
    worksheet_s.write(4, 2, ugettext(u"สัดส่วนการสอน"), header)
    worksheet_s.write(4, 3, ugettext(u"บรรยาย"), header)
    worksheet_s.write(4, 4, ugettext(u"ปฏิบัติการ"), header)
    worksheet_s.write(4, 5, ugettext(u"ภาค"), header)
    worksheet_s.write(4, 6, ugettext(u"จำนวนนักศึกษา"), header)
    worksheet_s.write(4, 7, ugettext(u"หมายเหตุ"), header)
    if score:
        worksheet_s.write(4, 8, ugettext(u"คะแนน"), header)

    
    # column widths
    subject_col_width = 15
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):
        row = 5 + idx
        worksheet_s.write_string(row, 0, data.subject_ID, cell_center)

        subject = data.subject.replace('\r','')
        worksheet_s.write_string(row, 1, subject, cell_center)
        subject_rows = compute_row(subject,subject_col_width)
        worksheet_s.set_row(row,15 * subject_rows)

        worksheet_s.write_number(row, 2, data.ratio, cell_center)
        worksheet_s.write_number(row, 3, data.num_of_lecture, cell_center)

        worksheet_s.write_number(row, 4, data.num_of_lab, cell_center)
        worksheet_s.write_string(row, 5, data.program_ID, cell_center)
        worksheet_s.write_number(row, 6, data.num_of_student, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_s.write_string(row, 7, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_s.set_row(row,15 * comment_rows)

        if score:
            worksheet_s.write_string(row, 8, " ", cell_center)


    # change column widths
    worksheet_s.set_column('B:B', subject_col_width)  # subject column
    worksheet_s.set_column('C:C', 11)  # ratio column
    worksheet_s.set_column('D:D', 9)  # num_of_lecture column
    worksheet_s.set_column('E:E', 9)  # num_of_lab column
    worksheet_s.set_column('F:F', 20)  # program column
    worksheet_s.set_column('G:G', 15)  # num_of_student column
    worksheet_s.set_column('H:H', comment_col_width)  # comment column
    if score:
         worksheet_s.set_column('I:I', 10)  # comment column


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




def WriteToExcelAll(query_data,query_data2,query_data3,query_data4,query_data5,query_data6,query_data7,current_user,score,staff):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet(u"งานสอน")
    worksheet_t = workbook.add_worksheet(u"การคุมโครงงาน")
    worksheet_u = workbook.add_worksheet(u"งานวิจัย")
    worksheet_v = workbook.add_worksheet(u"งานเขียนเอกสาร")
    worksheet_w = workbook.add_worksheet(u"งานสนับสนุนการจัดการศึกษา")
    worksheet_x = workbook.add_worksheet(u"งานบริหาร")
    worksheet_y = workbook.add_worksheet(u"รางวัลต่างๆ")

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

    # sheet1 -----------------------------------------------------------------------------

    # merge cells
    worksheet_s.merge_range('A2:I2', title_text, title)

    # write header
    worksheet_s.merge_range('A3:I3',ugettext(u"งานสอน"))
    worksheet_s.merge_range('D4:E4',ugettext(u"จำนวนหนว่ยกิตการ"),header)
    worksheet_s.write(4, 0, ugettext(u"รหัสวิชา"), header)
    worksheet_s.write(4, 1, ugettext(u"ชื่อวิชา"), header)
    worksheet_s.write(4, 2, ugettext(u"สัดส่วนการสอน"), header)
    worksheet_s.write(4, 3, ugettext(u"บรรยาย"), header)
    worksheet_s.write(4, 4, ugettext(u"ปฏิบัติการ"), header)
    worksheet_s.write(4, 5, ugettext(u"ภาค"), header)
    worksheet_s.write(4, 6, ugettext(u"จำนวนนักศึกษา"), header)
    worksheet_s.write(4, 7, ugettext(u"หมายเหตุ"), header)
    if staff and score:
        worksheet_s.write(4, 8, ugettext(u"user"),header)
        worksheet_s.write(4, 9, ugettext(u"คะแนน"), header)
    elif score:
        worksheet_s.write(4, 8, ugettext(u"คะแนน"), header)
    elif staff:
        worksheet_s.write(4, 8, ugettext(u"user"),header)
    
    # column widths
    subject_col_width = 15
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):
        row = 5 + idx
        worksheet_s.write_string(row, 0, data.subject_ID, cell_center)

        subject = data.subject.replace('\r','')
        worksheet_s.write_string(row, 1, subject, cell_center)
        subject_rows = compute_row(subject,subject_col_width)
        worksheet_s.set_row(row,15 * subject_rows)

        worksheet_s.write_number(row, 2, data.ratio, cell_center)
        worksheet_s.write_number(row, 3, data.num_of_lecture, cell_center)

        worksheet_s.write_number(row, 4, data.num_of_lab, cell_center)
        worksheet_s.write_string(row, 5, data.program_ID, cell_center)
        worksheet_s.write_number(row, 6, data.num_of_student, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_s.write_string(row, 7, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_s.set_row(row,15 * comment_rows)

        if staff and score:
            worksheet_s.write_string(row, 8,data.user.username, cell_center)
            worksheet_s.write_string(row, 9, " ", cell_center)
        elif score:
            worksheet_s.write_string(row, 8, " ", cell_center)
        elif staff:
            worksheet_s.write_string(row, 8,data.user.username, cell_center)


    # change column widths
    worksheet_s.set_column('B:B', subject_col_width+7)  # subject column
    worksheet_s.set_column('C:C', 11+7)  # ratio column
    worksheet_s.set_column('D:D', 9+7)  # num_of_lecture column
    worksheet_s.set_column('E:E', 9+7)  # num_of_lab column
    worksheet_s.set_column('F:F', 20+7)  # program column
    worksheet_s.set_column('G:G', 15+7)  # num_of_student column
    worksheet_s.set_column('H:H', comment_col_width+7)  # comment column
    if staff and score:
        worksheet_s.set_column('I:I',10+7) #user column
        worksheet_s.set_column('J:J', 10+7)  # comment column
    elif score:
        worksheet_s.set_column('I:I', 10+7)  # comment column
    elif staff:
        worksheet_s.set_column('I:I',10+7) #user column

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



    # sheet2 -----------------------------------------------------------------------------

    # merge cells
    worksheet_t.merge_range('A2:E2', title_text, title)

    # write header
    worksheet_t.merge_range('A4:E4',ugettext(u"การคุมโครงงาน/วิทยานิพนธ์"))
    worksheet_t.write(4, 0, ugettext(u"ชื่อโครงงาน/วิทยานิพนธ์"), header)
    worksheet_t.write(4, 1, ugettext(u"ชื่อนักศึกษา"), header)
    worksheet_t.write(4, 2, ugettext(u"สัดส่วนการสอน"), header)
    worksheet_t.write(4, 3, ugettext(u"ระดับ"), header)
    worksheet_t.write(4, 4, ugettext(u"ประเภทโครงการ"), header)
    worksheet_t.write(4, 5, ugettext(u"หมายเหตุ"), header)
    if staff and score:
        worksheet_t.write(4, 6, ugettext(u"user"),header)
        worksheet_t.write(4, 7, ugettext(u"คะแนน"), header)
    elif score:
        worksheet_t.write(4, 6, ugettext(u"คะแนน"), header)
    elif staff:
        worksheet_t.write(4, 6, ugettext(u"user"),header)
    

    # column widths
    thesis_col_width = 35
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data2):
        row = 5 + idx

        thesis_name = data.thesis_name.replace('\r','')
        worksheet_t.write_string(row, 0, thesis_name, cell_center)
        thesis_rows = compute_row(thesis_name,thesis_col_width)
        worksheet_t.set_row(row,15 * thesis_rows)

        student_name = data.student_name.replace('\r','')
        worksheet_t.write_string(row, 1, student_name, cell_center)
        student_rows = compute_row(student_name,thesis_col_width)
        worksheet_t.set_row(row,15 * student_rows)

        worksheet_t.write_number(row, 2, data.ratio, cell_center)
        worksheet_t.write_string(row, 3, data.degree, cell_center)
        worksheet_t.write_string(row, 4, data.program_ID, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_t.write_string(row, 5, comment, cell_center)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_t.set_row(row,15 * comment_rows)
        if staff and score:
            worksheet_t.write_string(row, 6, data.user.username, cell_center)
            worksheet_t.write_string(row, 7, " ", cell_center)
        elif score:
            worksheet_t.write_string(row, 6, " ", cell_center)
        elif staff:
            worksheet_t.write_string(row, 6, data.user.username, cell_center)

    # change column widths
    worksheet_t.set_column('A:A', thesis_col_width+7)  # thesis_name column
    worksheet_t.set_column('B:B', thesis_col_width+7)  # thesis_name column
    worksheet_t.set_column('C:C', 11+7)  # ratio column
    worksheet_t.set_column('D:D', 15+7)  # degree column
    worksheet_t.set_column('E:E', 25+7)  # program_ID column
    worksheet_t.set_column('F:F', comment_col_width+7)  # comment column
    if staff and score:
        worksheet_t.set_column('G:G',10+7) #user column
        worksheet_t.set_column('H:H', 10+7)  # comment column
    elif score:
        worksheet_t.set_column('G:G', 10+7)  # comment column
    elif staff:
        worksheet_t.set_column('G:G',10+7) #user column


    # sheet3 -----------------------------------------------------------------------------

    # merge cells
    worksheet_u.merge_range('A2:G2', title_text, title)

    # write header
    worksheet_u.merge_range('A4:H4',ugettext(u"งานวิจัยและงานสร้างสรรค์"))
    worksheet_u.write(4, 0, ugettext(u"ชื่อผลงาน"), header)
    worksheet_u.write(4, 1, ugettext(u"ชื่อผู้แต่งร่วม"), header)
    worksheet_u.write(4, 2, ugettext(u"ชื่อวารสารที่ตีพิมพ์"), header)
    worksheet_u.write(4, 3, ugettext(u"ปี พ.ศ. ที่ตีพิมพ์"), header)
    worksheet_u.write(4, 4, ugettext(u"สัดส่วน"), header)
    worksheet_u.write(4, 5, ugettext(u"ประเภท"), header)
    worksheet_u.write(4, 6, ugettext(u"หมายเหตุ"), header)
    if staff and score:
        worksheet_u.write(4, 7, ugettext(u"user"),header)
        worksheet_u.write(4, 8, ugettext(u"คะแนน"), header)
    elif score:
        worksheet_u.write(4, 7, ugettext(u"คะแนน"), header)
    elif staff:
        worksheet_u.write(4, 7, ugettext(u"user"),header)

    # column widths
    research_col_width = 20
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data3):

        row = 5 + idx

        research_name = data.research_name.replace('\r','')
        worksheet_u.write_string(row, 0, research_name, cell_center)
        research_rows = compute_row(research_name,research_col_width)
        worksheet_u.set_row(row, 15 * research_rows)

        worksheet_u.write_string(row, 1, data.assist_name, cell_center)
        worksheet_u.write_string(row, 2, data.journal_name, cell_center)
        worksheet_u.write_number(row, 3, data.year, cell_center)
        worksheet_u.write_number(row, 4, data.ratio, cell_center)
        worksheet_u.write_string(row, 5, data.degree, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_u.write_string(row, 6, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_u.set_row(row,15 * comment_rows)

        if staff and score:
            worksheet_u.write_string(row, 7, data.user.username, cell_center)
            worksheet_u.write_string(row, 8, " ", cell_center)
        elif score:
            worksheet_u.write_string(row, 7, " ", cell_center)
        elif staff:
            worksheet_u.write_string(row, 7, data.user.username, cell_center)

        

    # change column widths
    worksheet_u.set_column('A:A', research_col_width+7)  # thesis_name column
    worksheet_u.set_column('B:B', 10+7)  # assist column
    worksheet_u.set_column('C:C', 12+7)  # journal column
    worksheet_u.set_column('D:D', 12+7)  # year column
    worksheet_u.set_column('E:E', 8+7)  # ratio column
    worksheet_u.set_column('F:F', 20+7)  # degree column
    worksheet_u.set_column('G:G', comment_col_width+7)  # comment column
    if staff and score:
        worksheet_u.set_column('H:H',10+7) #user column
        worksheet_u.set_column('I:I', 10+7)  # comment column
    elif score:
        worksheet_u.set_column('H:H', 10+7)  # comment column
    elif staff:
        worksheet_u.set_column('H:H',10+7) #user column


    # sheet4 -----------------------------------------------------------------------------

    # merge cells
    worksheet_v.merge_range('A2:H2', title_text, title)

    # write header
    worksheet_v.merge_range('A4:H4',ugettext(u"งานเขียนเอกสารประกอบการสอน เอกสารคำสอน หนังสือ ตำรา หรือบทความวิชาการ"))
    worksheet_v.write(4, 0, ugettext(u"รหัสวิชา"), header)
    worksheet_v.write(4, 1, ugettext(u"ชื่อวิชา"), header)
    worksheet_v.write(4, 2, ugettext(u"ชื่อผู้แต่งร่วม"), header)
    worksheet_v.write(4, 3, ugettext(u"จำนวนหน้า"), header)
    worksheet_v.write(4, 4, ugettext(u"สัดส่วผลงาน"), header)
    worksheet_v.write(4, 5, ugettext(u"ประเภทผลงาน"), header)
    worksheet_v.write(4, 6, ugettext(u"หมายเหตุ"), header)
    if staff and score:
        worksheet_v.write(4, 7, ugettext(u"user"),header)
        worksheet_v.write(4, 8, ugettext(u"คะแนน"), header)
    elif score:
        worksheet_v.write(4, 7, ugettext(u"คะแนน"), header)
    elif staff:
        worksheet_v.write(4, 7, ugettext(u"user"),header)

    # column widths
    subject_col_width = 25
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data4):
        row = 5 + idx
        worksheet_v.write_string(row, 0, data.subject_ID, cell_center)

        subject = data.subject_name.replace('\r','')
        worksheet_v.write_string(row, 1, data.subject_name, cell_center)
        subject_rows = compute_row(subject,subject_col_width)
        worksheet_v.set_row(row,15 * subject_rows)

        worksheet_v.write_string(row, 2, data.assist_name, cell_center)
        worksheet_v.write_number(row, 3, data.page, cell_center)

        worksheet_v.write_number(row, 4, data.ratio, cell_center)
        worksheet_v.write_string(row, 5, data.degree, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_v.write_string(row, 6, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_v.set_row(row,15 * comment_rows)

        if score and staff:
            worksheet_v.write_string(row, 7, data.user.username, cell_center)
            worksheet_v.write_string(row, 8, " ", cell_center)
        elif score:
            worksheet_v.write_string(row, 7, " ", cell_center)
        elif staff:
            worksheet_v.write_string(row, 7, data.user.username, cell_center)
        

    # change column widths
    worksheet_v.set_column('A:A', 10+7)  #subject_id
    worksheet_v.set_column('B:B', subject_col_width+7)  # subject column
    worksheet_v.set_column('C:C', 11+7)  # assist_name column
    worksheet_v.set_column('D:D', 9+7)  # page column
    worksheet_v.set_column('E:E', 9+7)  # ratio column
    worksheet_v.set_column('F:F', 20+7)  # degree column
    worksheet_v.set_column('G:G', comment_col_width+7)  # comment column
    if score and staff:
        worksheet_v.set_column('H:H',10+7) #user column
        worksheet_v.set_column('I:I',10+7) #user column
    elif score:
        worksheet_v.set_column('H:H', 10+7)  # comment column
    elif staff:
        worksheet_v.set_column('H:H', 10+7)  # comment column

    # sheet5 -----------------------------------------------------------------------------

    # merge cells
    worksheet_w.merge_range('A2:E2', title_text, title)

    # write header
    worksheet_w.merge_range('A4:E4',ugettext(u"งานสนับสนุนการจัดการศึกษา"))
    worksheet_w.write(4, 0, ugettext(u"รายการ"), header)
    worksheet_w.write(4, 1, ugettext(u"ระดับ"), header)
    worksheet_w.write(4, 2, ugettext(u"ประเภท"), header)
    worksheet_w.write(4, 3, ugettext(u"หมายเหตุ"), header)
    if score and staff:
        worksheet_w.write(4, 4, ugettext(u"user"),header)
        worksheet_w.write(4, 5, ugettext(u"คะแนน"), header)
    elif score:
        worksheet_w.write(4, 4, ugettext(u"คะแนน"), header)
    elif staff:
        worksheet_w.write(4, 4, ugettext(u"user"),header)

    # column widths
    support_list_col_width = 40
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data5):
        row = 5 + idx

        support_list = data.support_list.replace('\r','')
        worksheet_w.write_string(row, 0, support_list, cell_center)
        support_list_rows = compute_row(support_list,support_list_col_width)
        worksheet_w.set_row(row,15 * support_list_rows)

        worksheet_w.write_string(row, 1, data.degree, cell_center)
        worksheet_w.write_string(row, 2, data.kind, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_w.write_string(row, 3, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_w.set_row(row,15 * comment_rows)

        if staff and score:
            worksheet_w.write_string(row, 4, data.user.username, cell_center)
            worksheet_w.write_string(row, 5, " ", cell_center)
        elif score:
            worksheet_w.write_string(row, 4, " ", cell_center)
        elif staff:
            worksheet_w.write_string(row, 4, data.user.username, cell_center)

    # change column widths
    worksheet_w.set_column('A:A', support_list_col_width+7)  # subject column
    worksheet_w.set_column('B:B', 15+7)  # subject column
    worksheet_w.set_column('C:C', 15+7)  # ratio column
    worksheet_w.set_column('D:D', comment_col_width+7)  # comment column
    if staff and score:
        worksheet_w.set_column('E:E',10+7) #user column
        worksheet_w.set_column('F:F',10+7) #user column
    elif score:
        worksheet_w.set_column('E:E', 10+7)  # comment column
    elif staff:
        worksheet_w.set_column('E:E', 10+7)  # comment column


    # sheet6 -----------------------------------------------------------------------------

    # merge cells
    worksheet_x.merge_range('A2:E2', title_text, title)

    # write header
    worksheet_x.merge_range('A4:E4',ugettext(u"งานบริหาร"))
    worksheet_x.write(4, 0, ugettext(u"รายการ"), header)
    worksheet_x.write(4, 1, ugettext(u"วันเวลาเริ่มดำรงตำแหน่ง"), header)
    worksheet_x.write(4, 2, ugettext(u"วันเวลาที่สิ้นสุดการดำรงตำแหน่ง"), header)
    worksheet_x.write(4, 3, ugettext(u"ระยะเวลาที่ดำรงตำแหน่ง"), header)
    worksheet_x.write(4, 4, ugettext(u"หมายเหตุ"), header)
    if staff and score:
        worksheet_x.write(4, 5, ugettext(u"user"),header)
        worksheet_x.write(4, 6, ugettext(u"คะแนน"), header)
    elif score:
        worksheet_x.write(4, 5, ugettext(u"คะแนน"), header)
    elif staff:
        worksheet_x.write(4, 5, ugettext(u"user"),header)
    

    # column widths
    position_name_col_width = 40
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data6):
        row = 5 + idx

        position_name = data.position_name.replace('\r','')
        worksheet_x.write_string(row, 0, position_name, cell_center)
        position_name_rows = compute_row(position_name,position_name_col_width)
        worksheet_x.set_row(row,15 * position_name_rows)

        worksheet_x.write_string(row, 1, data.time_start, cell_center)
        worksheet_x.write_string(row, 2, data.time_end, cell_center)

        worksheet_x.write_number(row, 3, row, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_x.write_string(row, 4, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_x.set_row(row,15 * comment_rows)

        if staff and score:
            worksheet_x.write_string(row, 5, data.user.username, cell_center)
            worksheet_x.write_string(row, 6, " ", cell_center)
        elif score:
            worksheet_x.write_string(row, 5, " ", cell_center)
        elif staff:
            worksheet_x.write_string(row, 5, data.user.username, cell_center)


    # change column widths
    worksheet_x.set_column('A:A', position_name_col_width+7)  # subject column
    worksheet_x.set_column('B:B', 18+7) 
    worksheet_x.set_column('C:C', 20+7)  # ratio column
    worksheet_x.set_column('D:D', 18+7)  # num_of_lecture column
    worksheet_x.set_column('E:E', comment_col_width+10)  # comment column
    if staff and score:
        worksheet_x.set_column('F:F',10+7) #user column
        worksheet_x.set_column('G:G', 10+7)  # comment column
    elif score:
        worksheet_x.set_column('F:F', 10+7)  # comment column
    elif staff:
        worksheet_x.set_column('F:F', 10+7)  # comment column

    # sheet7 -----------------------------------------------------------------------------

    # merge cells
    worksheet_y.merge_range('A2:C2', title_text, title)

    # write header
    worksheet_y.merge_range('A4:C4',ugettext(u"รางวัลต่างๆ"))
    worksheet_y.write(4, 0, ugettext(u"รายการ"), header)
    worksheet_y.write(4, 1, ugettext(u"ชื่อผลงาน"), header)
    worksheet_y.write(4, 2, ugettext(u"ชื่อผู้เข้าร่วมแข่งขัน"), header)
    worksheet_y.write(4, 3, ugettext(u"หมายเหตุ"), header)
    if staff and score:
        worksheet_y.write(4, 4, ugettext(u"user"),header)
        worksheet_y.write(4, 5, ugettext(u"คะแนน"), header)
    elif score:
        worksheet_y.write(4, 4, ugettext(u"คะแนน"), header)
    elif staff:
        worksheet_y.write(4, 4, ugettext(u"user"),header)
    

    # column widths
    benefit_name_col_width = 50
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data7):
        row = 5 + idx
        worksheet_y.write_string(row, 0, data.benefit_list, cell_center)

        benefit_name = data.benefit_name.replace('\r','')
        worksheet_y.write_string(row, 1, benefit_name, cell_center)
        benefit_name_rows = compute_row(benefit_name,benefit_name_col_width)
        worksheet_y.set_row(row,15 * benefit_name_rows)

        person_name = data.person_name.replace('\r','')
        worksheet_y.write_string(row, 2, person_name, cell_center)
        person_name_rows = compute_row(person_name,benefit_name_col_width)
        worksheet_y.set_row(row,15 * person_name_rows)

        comment = data.comment.replace('\r','')
        worksheet_y.write_string(row, 3, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_y.set_row(row,15 * comment_rows)

        if staff and score:
            worksheet_y.write_string(row, 4, data.user.username, cell_center)
            worksheet_y.write_string(row, 5, " ", cell_center)
        elif score:
            worksheet_y.write_string(row, 4, " ", cell_center)
        elif staff:
            worksheet_y.write_string(row, 4, data.user.username, cell_center)

        
    # change column widths
    worksheet_y.set_column('A:A', benefit_name_col_width+7)  # benefit_name column
    worksheet_y.set_column('B:B', benefit_name_col_width+7)  # benefit_name column
    worksheet_y.set_column('C:C', benefit_name_col_width+7)  # benefit_name column
    worksheet_y.set_column('D:D', comment_col_width+7)  # ratio column
    if staff and score:
        worksheet_y.set_column('E:E',10+7) #user column
        worksheet_y.set_column('F:F', 10+7)  # comment column
    elif score:
        worksheet_y.set_column('E:E', 10+7)  # comment column
    elif staff:
        worksheet_y.set_column('E:E', 10+7)  # comment column

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


