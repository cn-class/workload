#!/usr/bin/python
# -*- coding: utf-8 -*-
import StringIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min

from .models import Teaching


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
        'valign': 'vcenter',
        'border': 1,
        'text_wrap': True,
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1,

    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1,
        'text_wrap': True
    })
    cell_cen = workbook.add_format({
        'align': 'center',
        'valign': 'top',
    })

    # write title
    
    title_text = u"{0} {1}".format(ugettext(u"ชื่อ"), current_user)
    # text = u"{0} {1}".format(ugettext("ปีการศึกษา"), u"2560")

    # sheet1 -----------------------------------------------------------------------------

    # merge cells
    if staff and score:
        worksheet_s.merge_range('A1:M1', ugettext(u"แบบฟอร์มรายงานผลการปฏิบัติงานของอาจารย์  คณะวิศวกรรมศาสตร์ มหาวิทยาลัยธรรมศาสตร์"),cell_cen)
        worksheet_s.merge_range('A2:M2', title_text,cell_cen)
        worksheet_s.merge_range('A3:M3', ugettext(u"ปีการศึกษา 2560"),cell_cen)
    elif score:
        worksheet_s.merge_range('A1:L1', ugettext(u"แบบฟอร์มรายงานผลการปฏิบัติงานของอาจารย์  คณะวิศวกรรมศาสตร์ มหาวิทยาลัยธรรมศาสตร์"),cell_cen)
        worksheet_s.merge_range('A2:L2', title_text,cell_cen)
        worksheet_s.merge_range('A3:L3', ugettext(u"ปีการศึกษา 2560"),cell_cen)
    elif staff:
        worksheet_s.merge_range('A1:L1', ugettext(u"แบบฟอร์มรายงานผลการปฏิบัติงานของอาจารย์  คณะวิศวกรรมศาสตร์ มหาวิทยาลัยธรรมศาสตร์"),cell_cen)
        worksheet_s.merge_range('A2:L2', title_text,cell_cen)
        worksheet_s.merge_range('A3:L3', ugettext(u"ปีการศึกษา 2560"),cell_cen)
    else:
        worksheet_s.merge_range('A1:K1', ugettext(u"แบบฟอร์มรายงานผลการปฏิบัติงานของอาจารย์  คณะวิศวกรรมศาสตร์ มหาวิทยาลัยธรรมศาสตร์"),cell_cen)
        worksheet_s.merge_range('A2:K2', title_text,cell_cen)
        worksheet_s.merge_range('A3:K3', ugettext(u"ปีการศึกษา 2560"),cell_cen)

    # write header
    worksheet_s.merge_range('A5:I5',ugettext(u"งานสอน"))
    worksheet_s.merge_range('A6:A9',ugettext(u"รหัสวิชา"),header)
    worksheet_s.merge_range('B6:B9',ugettext(u"ชื่อวิชา"),header)
    worksheet_s.merge_range('C6:C9',ugettext(u"สัดส่วน\nการสอน"),header)
    worksheet_s.merge_range('D6:E7',ugettext(u"จำนวนหนว่ยกิตการ"),header)
    worksheet_s.merge_range('D8:D9',ugettext(u"บรรยาย"),header)
    worksheet_s.merge_range('E8:E9',ugettext(u"ปฏิบัติการ"),header)
    worksheet_s.merge_range('F6:I6',ugettext(u"ประเภทโครงการ"),header)
    worksheet_s.merge_range('F7:F9',ugettext(u"ปกติ"),header)
    worksheet_s.merge_range('G7:H7',ugettext(u"พิเศษ"),header)
    worksheet_s.merge_range('G8:G9',ugettext(u"ได้ค่าตอบแทน"),header)
    worksheet_s.merge_range('H8:H9',ugettext(u"ไม่ได้ค่าตอบแทน"),header)
    worksheet_s.merge_range('I7:I9',ugettext(u"งานสอนคณะอื่น\nใน มธ. ที่ไม่ได้\nค่าตอบแทน"),header)
    worksheet_s.merge_range('J6:J9',ugettext(u"จำนวนนักศึกษา"),header)
    worksheet_s.merge_range('K6:K9',ugettext(u"หมายเหตุ"),header)
    if staff and score:
        worksheet_s.merge_range('L6:L9',ugettext(u"user"),header)
        worksheet_s.merge_range('M6:M9',ugettext(u"คะแนน"),header)
    elif score:
        worksheet_s.merge_range('L6:L9',ugettext(u"คะแนน"),header)
    elif staff:
        worksheet_s.merge_range('L6:L9',ugettext(u"user"),header)
    
    # column widths
    subject_col_width = 15
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data):
        row = 9 + idx
        worksheet_s.write_string(row, 0, data.subject_ID, cell_center)

        subject = data.subject.replace('\r','')
        worksheet_s.write_string(row, 1, subject, cell_center)
        subject_rows = compute_row(subject,subject_col_width)
        worksheet_s.set_row(row,15 * subject_rows)

        worksheet_s.write_number(row, 2, data.ratio, cell_center)
        worksheet_s.write_number(row, 3, data.num_of_lecture, cell_center)

        worksheet_s.write_number(row, 4, data.num_of_lab, cell_center)
        if data.program_ID == u'โครงการปกติ':
            worksheet_s.write_string(row, 5, 'x', cell_center)
            worksheet_s.write_string(row, 6, ' ', cell_center)
            worksheet_s.write_string(row, 7, ' ', cell_center)
            worksheet_s.write_string(row, 8, ' ', cell_center)
        elif data.program_ID == u'โครงการพิเศษได้ค่าตอบแทน':
            worksheet_s.write_string(row, 5, ' ', cell_center)
            worksheet_s.write_string(row, 6, 'x', cell_center)
            worksheet_s.write_string(row, 7, ' ', cell_center)
            worksheet_s.write_string(row, 8, ' ', cell_center)
        elif data.program_ID == u'โครงการพิเศษไม่ได้ค่าตอบแทน':
            worksheet_s.write_string(row, 5, ' ', cell_center)
            worksheet_s.write_string(row, 6, ' ', cell_center)
            worksheet_s.write_string(row, 7, 'x', cell_center)
            worksheet_s.write_string(row, 8, ' ', cell_center)
        elif data.program_ID == u'งานสอนคณะอื่นภายใน มธ. ที่ไม่ได้ค่าตอบแทน':
            worksheet_s.write_string(row, 5, ' ', cell_center)
            worksheet_s.write_string(row, 6, ' ', cell_center)
            worksheet_s.write_string(row, 7, ' ', cell_center)
            worksheet_s.write_string(row, 8, 'x', cell_center)

        worksheet_s.write_number(row, 9, data.num_of_student, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_s.write_string(row, 10, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_s.set_row(row,15 * comment_rows)

        if staff and score:
            worksheet_s.write_string(row, 11,data.user.username, cell_center)
            worksheet_s.write_string(row, 12, " ", cell_center)
        elif score:
            worksheet_s.write_string(row, 11, " ", cell_center)
        elif staff:
            worksheet_s.write_string(row, 11,data.user.username, cell_center)


    # change column widths
    worksheet_s.set_column('B:B', subject_col_width+7)  # subject column
    worksheet_s.set_column('C:C', 1+7)  # ratio column
    worksheet_s.set_column('D:D', 1+7)  # num_of_lecture column
    worksheet_s.set_column('E:E', 1+7)  # num_of_lab column
    worksheet_s.set_column('F:F', 1+7)  # program column
    worksheet_s.set_column('G:G', 1+7)  # num_of_student column
    worksheet_s.set_column('H:H', 1+7)  # comment column
    worksheet_s.set_column('I:I', 3+7)  # comment column
    worksheet_s.set_column('J:J', 1+7)  # program column
    worksheet_s.set_column('K:K', 15+7)  # num_of_student column
    worksheet_s.set_column('L:L', comment_col_width+7)  # comment column
    if staff and score:
        worksheet_s.set_column('M:M',10+7) #user column
        worksheet_s.set_column('N:M', 10+7)  # comment column
    elif score:
        worksheet_s.set_column('M:M', 10+7)  # comment column
    elif staff:
        worksheet_s.set_column('M:M',10+7) #user column

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


    # write header
    worksheet_t.merge_range('A1:K1',ugettext(u"การคุมโครงงาน/วิทยานิพนธ์"))

    worksheet_t.merge_range('A2:A5',ugettext(u"ชื่อโครงงาน/วิทยานิพนธ์"),header)
    worksheet_t.merge_range('B2:B5',ugettext(u"ชื่อนักศึกษา"),header)
    worksheet_t.merge_range('C2:C5',ugettext(u"สัดส่วน\nการสอน"),header)
    worksheet_t.merge_range('D2:G2',ugettext(u"ระดับ"),header)
    worksheet_t.merge_range('D3:D5',ugettext(u"โครงงาน"),header)
    worksheet_t.merge_range('E3:E5',ugettext(u"สาระนิพนธ์"),header)
    worksheet_t.merge_range('F3:G3',ugettext(u"วิทยานิพนธ์ "),header)
    worksheet_t.merge_range('F4:F5',ugettext(u"ป. โทร"),header)
    worksheet_t.merge_range('G4:G5',ugettext(u"ป. เอก"),header)
    worksheet_t.merge_range('H2:K2',ugettext(u"ประเภทโครงการ"),header)
    worksheet_t.merge_range('H3:H5',ugettext(u"ปกติ"),header)
    worksheet_t.merge_range('I3:J3',ugettext(u"พิเศษ"),header)
    worksheet_t.merge_range('I4:I5',ugettext(u"ได้ค่าตอบแทน"),header)
    worksheet_t.merge_range('J4:J5',ugettext(u"ไม่ได้ค่าตอบแทน"),header)
    worksheet_t.merge_range('K3:K5',ugettext(u"งานสอนคณะอื่น\nใน มธ. ที่ไม่ได้\nค่าตอบแทน"),header)
    worksheet_t.merge_range('L2:L5',ugettext(u"หมายเหตุ"),header)
    if staff and score:
        worksheet_t.merge_range('M2:M5',ugettext(u"user"),header)
        worksheet_t.merge_range('N2:N5',ugettext(u"คะแนน"),header)
    elif score:
        worksheet_t.merge_range('M2:M5',ugettext(u"คะแนน"),header)
    elif staff:
        worksheet_t.merge_range('M2:M5',ugettext(u"user"),header)

    
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
        worksheet_t.write_string(row, 4, data.degree, cell_center)
        worksheet_t.write_string(row, 5, data.degree, cell_center)
        worksheet_t.write_string(row, 6, data.degree, cell_center)
        worksheet_t.write_string(row, 7, data.program_ID, cell_center)
        worksheet_t.write_string(row, 8, data.program_ID, cell_center)
        worksheet_t.write_string(row, 9, data.program_ID, cell_center)
        worksheet_t.write_string(row, 10, data.program_ID, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_t.write_string(row, 11, comment, cell_center)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_t.set_row(row,15 * comment_rows)
        if staff and score:
            worksheet_t.write_string(row, 12, data.user.username, cell_center)
            worksheet_t.write_string(row, 13, " ", cell_center)
        elif score:
            worksheet_t.write_string(row, 12, " ", cell_center)
        elif staff:
            worksheet_t.write_string(row, 12, data.user.username, cell_center)

    # change column widths
    worksheet_t.set_column('A:A', 20+7)  # thesis_name column
    worksheet_t.set_column('B:B', 20+7)  # student_name column
    worksheet_t.set_column('C:C', 2+7)  # ratio column
    worksheet_t.set_column('D:D', 2+7)  # degree column
    worksheet_t.set_column('E:E', 2+7)  # degree column
    worksheet_t.set_column('F:F', 2+7)  # degree column
    worksheet_t.set_column('G:G', 2+7)  # degree column
    worksheet_t.set_column('H:H', 2+7)  # program_ID column
    worksheet_t.set_column('I:I', 2+7)  # program_ID column
    worksheet_t.set_column('J:J', 2+7)  # program_ID column
    worksheet_t.set_column('K:K', 2+7)  # program_ID column
    worksheet_t.set_column('L:L', comment_col_width+7)  # comment column
    if staff and score:
        worksheet_t.set_column('M:M',10+7) #user column
        worksheet_t.set_column('N:N', 10+7)  # comment column
    elif score:
        worksheet_t.set_column('M:M', 10+7)  # comment column
    elif staff:
        worksheet_t.set_column('M:M',10+7) #user column


    # sheet3 -----------------------------------------------------------------------------

    # write header
    worksheet_u.merge_range('A1:L1',ugettext(u"งานวิจัยและงานสร้างสรรค์"))

    worksheet_u.merge_range('A2:A8',ugettext(u"ชื่อผลงาน"),header)
    worksheet_u.merge_range('B2:B8',ugettext(u"ชื่อผู้แต่งร่วม"),header)
    worksheet_u.merge_range('C2:C8',ugettext(u"ชื่อวารสารที่ตีพิมพ์"),header)
    worksheet_u.merge_range('D2:D8',ugettext(u"ปี พ.ศ. ที่ตีพิมพ์"),header)
    worksheet_u.merge_range('E2:E8',ugettext(u"สัดส่วนผลงาน"),header)

    worksheet_u.merge_range('F2:J2',ugettext(u"ระดับของผลงานวิชาการ"),header)
    worksheet_u.merge_range('F3:H4',ugettext(u"วารสารที่ สกว. ยอมรับ"),header)
    worksheet_u.merge_range('F5:F8',ugettext(u"นานาชาติ\nมี impact\nfactor"),header)
    worksheet_u.merge_range('G5:G8',ugettext(u"นานาชาติ\nไม่มี impact\nfactor"),header)
    worksheet_u.merge_range('H5:H8',ugettext(u"ระดับชาติ\nหรือ มธ."),header)
    worksheet_u.merge_range('I3:I8',ugettext(u"วารสาร\nนานาชาติ\nที่อยู่\nในฐานข้อมูล\nสากล"),header)
    worksheet_u.merge_range('J3:J8',ugettext(u"ผลงาน\nวิชาการอื่น\nตามข้อ ๖.๓.๕"),header)
    worksheet_u.merge_range('K2:L2',ugettext(u"สิ่งประดิษฐ์"),header)
    worksheet_u.merge_range('K3:K8',ugettext(u"ได้รับการจด\nทะเบียน\nสิทธิบัตร/\nอนุสิทธิบัตร"),header)
    worksheet_u.merge_range('L3:L8',ugettext(u"สิทธิบัตร/อนุ\nสิทธิบัตร ที่ถูก\nนำไปใช้เชิงพาณิชย์\nหรือ\nสาธารณประโยชน์"),header)
    worksheet_u.merge_range('M2:M8',ugettext(u"หมายเหตุ"),header)
    if staff and score:
        worksheet_u.merge_range('N2:N8',ugettext(u"user"),header)
        worksheet_u.merge_range('O2:O8',ugettext(u"คะแนน"),header)
    elif score:
        worksheet_u.merge_range('N2:N8',ugettext(u"คะแนน"),header)
    elif staff:
        worksheet_u.merge_range('N2:N8',ugettext(u"user"),header)


    # column widths
    research_col_width = 20
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data3):

        row = 8 + idx

        research_name = data.research_name.replace('\r','')
        worksheet_u.write_string(row, 0, research_name, cell_center)
        research_rows = compute_row(research_name,research_col_width)
        worksheet_u.set_row(row, 15 * research_rows)

        worksheet_u.write_string(row, 1, data.assist_name, cell_center)
        worksheet_u.write_string(row, 2, data.journal_name, cell_center)
        worksheet_u.write_number(row, 3, data.year, cell_center)
        worksheet_u.write_number(row, 4, data.ratio, cell_center)
        worksheet_u.write_string(row, 5, data.degree, cell_center)
        worksheet_u.write_string(row, 6, data.degree, cell_center)
        worksheet_u.write_string(row, 7, data.degree, cell_center)
        worksheet_u.write_string(row, 8, data.degree, cell_center)
        worksheet_u.write_string(row, 9, data.degree, cell_center)
        worksheet_u.write_string(row, 10, data.degree, cell_center)
        worksheet_u.write_string(row, 11, data.degree, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_u.write_string(row, 12, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_u.set_row(row,15 * comment_rows)

        if staff and score:
            worksheet_u.write_string(row, 13, data.user.username, cell_center)
            worksheet_u.write_string(row, 14, " ", cell_center)
        elif score:
            worksheet_u.write_string(row, 13, " ", cell_center)
        elif staff:
            worksheet_u.write_string(row, 13, data.user.username, cell_center)

        

    # change column widths
    worksheet_u.set_column('A:A', research_col_width+7)  # thesis_name column
    worksheet_u.set_column('B:B', 10+7)  # assist column
    worksheet_u.set_column('C:C', 12+7)  # journal column
    worksheet_u.set_column('D:D', 12+7)  # year column
    worksheet_u.set_column('E:E', 8+7)  # ratio column
    worksheet_u.set_column('F:F', 2+7)  # degree column
    worksheet_u.set_column('G:G', 2+7)  # degree column
    worksheet_u.set_column('H:H', 2+7)  # degree column
    worksheet_u.set_column('I:I', 2+7)  # degree column
    worksheet_u.set_column('J:J', 2+7)  # degree column
    worksheet_u.set_column('K:K', 2+7)  # degree column
    worksheet_u.set_column('L:L', 2+7)  # degree column
    worksheet_u.set_column('M:M', comment_col_width+7)  # comment column
    if staff and score:
        worksheet_u.set_column('N:N',10+7) #user column
        worksheet_u.set_column('O:O', 10+7)  # comment column
    elif score:
        worksheet_u.set_column('N:N', 10+7)  # comment column
    elif staff:
        worksheet_u.set_column('N:N',10+7) #user column


    # sheet4 -----------------------------------------------------------------------------

    # write header
    worksheet_v.merge_range('A1:K1',ugettext(u"งานเขียนเอกสารประกอบการสอน เอกสารคำสอน หนังสือ ตำรา หรือบทความวิชาการ"))

    worksheet_v.merge_range('A2:A5',ugettext(u"รหัสวิชา"),header)
    worksheet_v.merge_range('B2:B5',ugettext(u"ชื่อวิชา"),header)
    worksheet_v.merge_range('C2:C5',ugettext(u"ชื่อผู้แต่งร่วม"),header)
    worksheet_v.merge_range('D2:D5',ugettext(u"จำนวนหน้า"),header)
    worksheet_v.merge_range('E2:E5',ugettext(u"สัดส่วนผลงาน"),header)

    worksheet_v.merge_range('F2:J2',ugettext(u"ประเภทผลงาน"),header)
    worksheet_v.merge_range('F3:F5',ugettext(u"บทความ\nวิชาการ"),header)
    worksheet_v.merge_range('G3:G5',ugettext(u"คู่มือ\nปฏิบัติการ"),header)
    worksheet_v.merge_range('H3:H5',ugettext(u"เอกสาร\nประกอบการสอน"),header)
    worksheet_v.merge_range('I3:I5',ugettext(u"เอกสารคำ\nสอน"),header)
    worksheet_v.merge_range('J3:J5',ugettext(u"ตำราหรือ\nหนังสือ"),header)
    worksheet_v.merge_range('K2:K5',ugettext(u"หมายเหตุ"),header)
    if staff and score:
        worksheet_v.merge_range('L2:L5',ugettext(u"user"),header)
        worksheet_v.merge_range('M2:M5',ugettext(u"คะแนน"),header)
    elif score:
        worksheet_v.merge_range('L2:L5',ugettext(u"คะแนน"),header)
    elif staff:
        worksheet_v.merge_range('L2:L5',ugettext(u"user"),header)


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
        worksheet_v.write_string(row, 6, data.degree, cell_center)
        worksheet_v.write_string(row, 7, data.degree, cell_center)
        worksheet_v.write_string(row, 8, data.degree, cell_center)
        worksheet_v.write_string(row, 9, data.degree, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_v.write_string(row, 10, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_v.set_row(row,15 * comment_rows)

        if score and staff:
            worksheet_v.write_string(row, 11, data.user.username, cell_center)
            worksheet_v.write_string(row, 12, " ", cell_center)
        elif score:
            worksheet_v.write_string(row, 11, " ", cell_center)
        elif staff:
            worksheet_v.write_string(row, 11, data.user.username, cell_center)
        

    # change column widths
    worksheet_v.set_column('A:A', 10+7)  #subject_id
    worksheet_v.set_column('B:B', subject_col_width+7)  # subject column
    worksheet_v.set_column('C:C', 11+7)  # assist_name column
    worksheet_v.set_column('D:D', 9+7)  # page column
    worksheet_v.set_column('E:E', 9+7)  # ratio column
    worksheet_v.set_column('F:F', 2+7)  # degree column
    worksheet_v.set_column('G:G', 2+7)  # degree column
    worksheet_v.set_column('H:H', 2+7)  # degree column
    worksheet_v.set_column('I:I', 2+7)  # degree column
    worksheet_v.set_column('J:J', 2+7)  # degree column
    worksheet_v.set_column('K:K', comment_col_width+7)  # comment column
    if score and staff:
        worksheet_v.set_column('L:L',10+7) #user column
        worksheet_v.set_column('L:M',10+7) #user column
    elif score:
        worksheet_v.set_column('L:L', 10+7)  # comment column
    elif staff:
        worksheet_v.set_column('L:L', 10+7)  # comment column

    # sheet5 -----------------------------------------------------------------------------

    # write header
    worksheet_w.merge_range('A1:H1',ugettext(u"งานสนับสนุนการจัดการศึกษา"))


    worksheet_w.merge_range('A2:A3',ugettext(u"รายการ"),header)
    worksheet_w.merge_range('B2:C2',ugettext(u"ระดับ"),header)
    worksheet_w.write('B3', ugettext(u"ประธาน"),header)
    worksheet_w.write('C3', ugettext(u"กรรมการ"),header)
    worksheet_w.merge_range('D2:E2',ugettext(u"ประเภท"),header)
    worksheet_w.write('D3', ugettext(u"ในคณะ"),header)
    worksheet_w.write('E3', ugettext(u"นอกคณะ"),header)
    worksheet_w.merge_range('F2:G2',ugettext(u"กรรมการครูภัณฑ์"),header)
    worksheet_w.write('F3', ugettext(u"เปิดซอง"),header)
    worksheet_w.write('G3', ugettext(u"ตรวจรับ"),header)
    worksheet_w.merge_range('H2:H3',ugettext(u"หมายเหตุ"),header)
    if staff and score:
        worksheet_w.merge_range('I2:I3',ugettext(u"user"),header)
        worksheet_w.merge_range('J2:J3',ugettext(u"คะแนน"),header)
    elif score:
        worksheet_w.merge_range('I2:I3',ugettext(u"คะแนน"),header)
    elif staff:
        worksheet_w.merge_range('I2:I3',ugettext(u"user"),header)


    # column widths
    support_list_col_width = 40
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data5):
        row = 3 + idx

        support_list = data.support_list.replace('\r','')
        worksheet_w.write_string(row, 0, support_list, cell_center)
        support_list_rows = compute_row(support_list,support_list_col_width)
        worksheet_w.set_row(row,15 * support_list_rows)

        worksheet_w.write_string(row, 1, data.degree, cell_center)
        worksheet_w.write_string(row, 2, data.degree, cell_center)
        worksheet_w.write_string(row, 3, data.kind, cell_center)
        worksheet_w.write_string(row, 4, data.kind, cell_center)
        worksheet_w.write_string(row, 5, data.degree, cell_center)
        worksheet_w.write_string(row, 6, data.degree, cell_center)

        comment = data.comment.replace('\r','')
        worksheet_w.write_string(row, 7, comment, cell)
        comment_rows = compute_row(comment,comment_col_width)
        worksheet_w.set_row(row,15 * comment_rows)

        if staff and score:
            worksheet_w.write_string(row, 8, data.user.username, cell_center)
            worksheet_w.write_string(row, 9, " ", cell_center)
        elif score:
            worksheet_w.write_string(row, 8, " ", cell_center)
        elif staff:
            worksheet_w.write_string(row, 8, data.user.username, cell_center)

    # change column widths
    worksheet_w.set_column('A:A', support_list_col_width+7)  # subject column
    worksheet_w.set_column('B:B', 1+7)  # subject column
    worksheet_w.set_column('C:C', 1+7)  # ratio column
    worksheet_w.set_column('D:D', 1+7)  # ratio column
    worksheet_w.set_column('E:E', 1+7)  # ratio column
    worksheet_w.set_column('F:F', 1+7)  # ratio column
    worksheet_w.set_column('G:G', 1+7)  # ratio column
    worksheet_w.set_column('H:H', comment_col_width+7)  # comment column
    if staff and score:
        worksheet_w.set_column('I:I',10+7) #user column
        worksheet_w.set_column('J:J',10+7) #user column
    elif score:
        worksheet_w.set_column('I:I', 10+7)  # comment column
    elif staff:
        worksheet_w.set_column('I:I', 10+7)  # comment column


    # sheet6 -----------------------------------------------------------------------------


    # write header
    worksheet_x.merge_range('A1:E1',ugettext(u"งานบริหาร"))
    worksheet_x.write(2, 0, ugettext(u"รายการ"), header)
    worksheet_x.write(2, 1, ugettext(u"วันเวลาเริ่มดำรงตำแหน่ง"), header)
    worksheet_x.write(2, 2, ugettext(u"วันเวลาที่สิ้นสุดการดำรงตำแหน่ง"), header)
    worksheet_x.write(2, 3, ugettext(u"ระยะเวลาที่ดำรงตำแหน่ง"), header)
    worksheet_x.write(2, 4, ugettext(u"หมายเหตุ"), header)
    if staff and score:
        worksheet_x.write(2, 5, ugettext(u"user"),header)
        worksheet_x.write(2, 6, ugettext(u"คะแนน"), header)
    elif score:
        worksheet_x.write(2, 5, ugettext(u"คะแนน"), header)
    elif staff:
        worksheet_x.write(2, 5, ugettext(u"user"),header)
    

    # column widths
    position_name_col_width = 40
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data6):
        row = 2 + idx

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

    # write header
    worksheet_y.merge_range('A1:C1',ugettext(u"รางวัลต่างๆ"))
    worksheet_y.write(2, 0, ugettext(u"รายการ"), header)
    worksheet_y.write(3, 0, ugettext(u"อาจารย์ได้รับรางวัลทางวิชาการ หรือวิชาชีพระดับหน่วยงานภายนอกมหาวิทยาลัย"), cell_center)
    worksheet_y.write(4, 0, ugettext(u"อาจารย์ได้รับรางวัลทางวิชาการ หรือวิชาชีพระดับชาติ/นานาชาติ"), cell_center)
    worksheet_y.write(5, 0, ugettext(u"อาจารย์ที่ปรึกษากิจกรรมการแข่งขันทางวิชาการของนักศึกษาที่ได้รับรางวัลระดับหน่วยงาน"), cell_center)
    worksheet_y.write(6, 0, ugettext(u"อาจารย์ที่ปรึกษากิจกรรมการแข่งขันทางวิชาการของนักศึกษาที่ได้รับรางวัลระดับชาติ/นานาชาติ"), cell_center)
    worksheet_y.write(7, 0, ugettext(u"อาจารย์ที่ให้ความร่วมมือในการจัดประชุมวิชาการของคณะฯ"), cell_center)
    worksheet_y.write(2, 1, ugettext(u"ชื่อผลงาน"), header)
    worksheet_y.write(2, 2, ugettext(u"ชื่อผู้เข้าร่วมแข่งขัน"), header)
    worksheet_y.write(2, 3, ugettext(u"หมายเหตุ"), header)
    if staff and score:
        worksheet_y.write(2, 4, ugettext(u"user"),header)
        worksheet_y.write(2, 5, ugettext(u"คะแนน"), header)
    elif score:
        worksheet_y.write(2, 4, ugettext(u"คะแนน"), header)
    elif staff:
        worksheet_y.write(2, 4, ugettext(u"user"),header)
    

    # column widths
    benefit_name_col_width = 40
    description_col_width = 10
    comment_col_width = 25

    # add data to the table
    for idx, data in enumerate(query_data7):
        row = 3 + idx
        # worksheet_y.write_string(row, 0, data.benefit_list, cell_center)

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


    worksheet_y.write(13, 1, ugettext(u"ลงนาม"), header)
    worksheet_y.write(13, 2, ugettext(u" "), header)
    worksheet_y.write(13, 3, ugettext(u"ประธานกรรมการระดับภาค"), header)
    worksheet_y.write(14, 1, ugettext(u"ลงนาม"), header)
    worksheet_y.write(14, 2, ugettext(u" "), header)
    worksheet_y.write(14, 3, ugettext(u"กรรมการระดับภาค"), header)
    worksheet_y.write(15, 1, ugettext(u"ลงนาม"), header)
    worksheet_y.write(15, 2, ugettext(u" "), header)
    worksheet_y.write(15, 3, ugettext(u"กรรมการระดับภาค"), header)
        
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


