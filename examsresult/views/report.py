from PyQt5.QtWidgets import QWidget, QLabel
from examsresult.views import CoreView

DIVISOR_PRECISION = 2


class ViewReport(CoreView):

    table_left = 100
    table_top = 130
    table_height = 350
    table_width = 500

    def print_exam_result(self, root, y, date, type, result, comment):
        x = 70
        label_date = QLabel(root)
        label_date.setText(date)
        label_date.move(x, y)

        label_type = QLabel(root)
        label_type.setText(str(type))
        label_type.move(x + 110, y)

        label_result = QLabel(root)
        label_result.setText(str(result))
        label_result.move(x + 210, y)

        label_comment = QLabel(root)
        label_comment.setText(comment)
        label_comment.move(x + 260, y)


class ViewReportStudent(ViewReport):

    def __init__(self, dbhandler, root_tab, lng, data):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng

        self.schoolyear = data['schoolyear']
        self.schoolclass = data['schoolclass']
        self.subject = data['subject']
        self.student_id = data['student_id']

        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())

        mytab = QWidget()

        s = self.dbh.get_student_data(self.student_id)
        student = "%s, %s" % (s.lastname, s.firstname)

        label_schoolyear_description = QLabel(mytab)
        label_schoolyear_description.setText(self.lng['schoolyear'])
        label_schoolyear_description.move(10, 10)
        label_schoolyear_description = QLabel(mytab)
        label_schoolyear_description.setText(self.schoolyear)
        label_schoolyear_description.move(100, 10)

        label_schoolclass_description = QLabel(mytab)
        label_schoolclass_description.setText(self.lng['schoolclass'])
        label_schoolclass_description.move(10, 30)
        label_schoolclass_description = QLabel(mytab)
        label_schoolclass_description.setText(self.schoolclass)
        label_schoolclass_description.move(100, 30)

        label_subject_description = QLabel(mytab)
        label_subject_description.setText(self.lng['subject'])
        label_subject_description.move(10, 50)
        label_subject_description = QLabel(mytab)
        label_subject_description.setText(self.subject)
        label_subject_description.move(100, 50)

        label_student_description = QLabel(mytab)
        label_student_description.setText(self.lng['student'])
        label_student_description.move(10, 70)
        label_student_description = QLabel(mytab)
        label_student_description.setText(student)
        label_student_description.move(100, 70)

        y_pos = 100
        time_period_data_list = self.dbh.get_timeperiod()
        complete_sum = 0
        complete_divisor = 0
        for period in time_period_data_list:
            sum = 0
            divisor = 0
            self.print_exam_result(mytab, y_pos, period[1], "", "", "")
            y_pos += 20
            self.print_exam_result(mytab, y_pos, "Date", "Examtype", "Result", "Comment")
            y_pos += 20
            results = self.dbh.get_exam_result(student_id=self.student_id, subject=self.subject, timeperiod_id=period[0])
            for r in results:
                x_t = self.dbh.get_examtype_by_id(r.exam.exam_type)
                if r.result:
                    sum += r.result * x_t.weight
                    divisor += 1 * x_t.weight
                self.print_exam_result(mytab, y_pos, r.exam.date, x_t.name, r.result, r.comment)
                y_pos += 20
            average = 0
            if divisor:
                average = round(float(sum)/divisor, DIVISOR_PRECISION)
                complete_sum += sum * period[2]
                complete_divisor += divisor * period[2]
            self.print_exam_result(mytab, y_pos, "", "", average, "")
            y_pos += 20

        complete_average = 0
        if complete_divisor:
            complete_average = round(float(complete_sum) / complete_divisor, DIVISOR_PRECISION)

        y_pos += 20
        self.print_exam_result(mytab, y_pos, self.lng['schoolyear'], "", complete_average, "")

        self.tab_window.addTab(mytab, self.lng['title'])


class ViewReportSchoolclass(ViewReport):

    def __init__(self, dbhandler, root_tab, lng, data):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng

        self.schoolyear = data['schoolyear']
        self.schoolclass = data['schoolclass']
        self.subject = data['subject']

        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())

        mytab = QWidget()

        label_schoolyear_description = QLabel(mytab)
        label_schoolyear_description.setText(self.lng['schoolyear'])
        label_schoolyear_description.move(10, 10)
        label_schoolyear_description = QLabel(mytab)
        label_schoolyear_description.setText(self.schoolyear)
        label_schoolyear_description.move(100, 10)

        label_schoolclass_description = QLabel(mytab)
        label_schoolclass_description.setText(self.lng['schoolclass'])
        label_schoolclass_description.move(10, 30)
        label_schoolclass_description = QLabel(mytab)
        label_schoolclass_description.setText(self.schoolclass)
        label_schoolclass_description.move(100, 30)

        label_subject_description = QLabel(mytab)
        label_subject_description.setText(self.lng['subject'])
        label_subject_description.move(10, 50)
        label_subject_description = QLabel(mytab)
        label_subject_description.setText(self.subject)
        label_subject_description.move(100, 50)

        self.tab_window.addTab(mytab, self.lng['title'])
