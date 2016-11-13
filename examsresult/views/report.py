from PyQt5.QtWidgets import QWidget, QLabel

from examsresult import current_config
from examsresult.views import CoreView

DIVISOR_PRECISION = 2


class ViewReport(CoreView):

    table_left = 100
    table_top = 130
    table_height = 350
    table_width = 500

    y_pos = 10

    show_schoolyear = True
    show_schoolclass = True
    show_subject = True
    show_student = False

    def __init__(self, dbhandler, root_tab, lng, data):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng
        self.config = current_config

        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())

        mytab = QWidget()

        if self.show_schoolyear:
            self.schoolyear = data['schoolyear']
            label_schoolyear_description = QLabel(mytab)
            label_schoolyear_description.setText(self.lng['schoolyear'])
            label_schoolyear_description.move(10, self.y_pos)
            label_schoolyear_description = QLabel(mytab)
            label_schoolyear_description.setText(self.schoolyear)
            label_schoolyear_description.move(100, self.y_pos)
            self.y_pos += 20

        if self.show_schoolclass:
            self.schoolclass = data['schoolclass']
            label_schoolclass_description = QLabel(mytab)
            label_schoolclass_description.setText(self.lng['schoolclass'])
            label_schoolclass_description.move(10, self.y_pos)
            label_schoolclass_description = QLabel(mytab)
            label_schoolclass_description.setText(self.schoolclass)
            label_schoolclass_description.move(100, self.y_pos)
            self.y_pos += 20

        if self.show_subject:
            self.subject = data['subject']
            label_subject_description = QLabel(mytab)
            label_subject_description.setText(self.lng['subject'])
            label_subject_description.move(10, self.y_pos)
            label_subject_description = QLabel(mytab)
            label_subject_description.setText(self.subject)
            label_subject_description.move(100, self.y_pos)
            self.y_pos += 20

        if self.show_student:
            self.student_id = data['student_id']
            s = self.dbh.get_student_data(self.student_id)
            student = "%s, %s" % (s.lastname, s.firstname)

            label_student_description = QLabel(mytab)
            label_student_description.setText(self.lng['student'])
            label_student_description.move(10, self.y_pos)
            label_student_description = QLabel(mytab)
            label_student_description.setText(student)
            label_student_description.move(100, self.y_pos)
            self.y_pos += 20

        self.y_pos = self.show_results(root=mytab, y_pos=self.y_pos + 10)

        self.tab_window.addTab(mytab, self.lng['title'])

    def show_results(self, root, y_pos=100):
        return y_pos

    def print_content(self, root, y, data):

        def print_label(root, x, y, text):
            label_date = QLabel(root)
            label_date.setText(text)
            label_date.move(x, y)

        x_coord = 70
        for text, x in data:
            x_coord += x
            print_label(root, x_coord, y, str(text))


class ViewReportStudent(ViewReport):

    show_student = True

    def show_results(self, root, y_pos=100):

        timeperiod_list = self.dbh.get_timeperiod()
        complete_t_p_result_sum = 0
        complete_t_p_result_count = 0
        complete_t_p_result_average = 0
        for period in timeperiod_list:
            t_p_result_sum = 0
            t_p_result_count = 0
            t_p_result_average = 0
            self.print_content(root, y_pos, [(period[1], 0)])
            y_pos += 20

            data_list = [("Date", 0), ("Examtype", 110), ("Result", 100), ("Comment", 40)]
            self.print_content(root, y_pos, data_list)
            y_pos += 20
            results = self.dbh.get_exam_result(student_id=self.student_id, subject=self.subject,
                                               timeperiod_id=period[0])
            for r in results:
                x_t = self.dbh.get_examtype_by_id(r.exam.exam_type)
                if r.result:
                    t_p_result_sum += r.result * x_t.weight
                    t_p_result_count += x_t.weight
                data_list = [(r.exam.date, 0), (x_t.name, 110), (r.result, 100), (r.comment, 40)]
                self.print_content(root, y_pos, data_list)
                y_pos += 20

            if t_p_result_count:
                t_p_result_average = round(float(t_p_result_sum) / t_p_result_count, DIVISOR_PRECISION)

            if t_p_result_sum:
                if self.config['schoolyear_result_calculation_method'] == 'complete':
                    complete_t_p_result_sum += t_p_result_sum * period[2]
                    complete_t_p_result_count += t_p_result_count * period[2]
                elif self.config['schoolyear_result_calculation_method'] == 'timeperiod':
                    complete_t_p_result_sum += t_p_result_average * period[2]
                    complete_t_p_result_count += period[2]
                else:
                    print("unknown calculation method")

            data_list = [("", 0), ("", 110), (t_p_result_average, 100), ("", 40)]
            self.print_content(root, y_pos, data_list)
            y_pos += 20

        if complete_t_p_result_count:
            complete_t_p_result_average = round(float(complete_t_p_result_sum)/complete_t_p_result_count, DIVISOR_PRECISION)

        data_list = [(self.lng['schoolyear'], 0), ("", 110), (complete_t_p_result_average, 100), ("", 40)]

        self.print_content(root, y_pos, data_list)
        y_pos += 20

        return y_pos


class ViewReportSchoolclass(ViewReport):

    def show_results(self, root, y_pos=100):

        timeperiod_list = self.dbh.get_timeperiod()
        data_list = [(self.lng['student'], 0)]
        for period in timeperiod_list:
            data_list.append((period[1], 100))
        data_list.append((self.lng['schoolyear'], 100))

        self.print_content(root, y_pos, data_list)
        y_pos += 20

        for student in self.dbh.get_students(self.schoolyear, self.schoolclass):
            name = "%s, %s" % (student[1], student[2])
            data_list = [(name, 0)]
            complete_t_p_result_sum = 0
            complete_t_p_result_count = 0
            complete_t_p_result_average = 0
            for period in timeperiod_list:
                t_p_result_list = []
                exams = self.dbh.get_exams(self.schoolyear, self.schoolclass, self.subject, period[0])
                for x in exams:
                    t_p_result_list.extend(self.dbh.get_exam_result(exam_id=x[0], student_id=student[0], subject=self.subject, timeperiod_id=period[0]))
                t_p_result_sum = 0
                t_p_result_count = 0
                t_p_result_average = 0
                for tp in t_p_result_list:
                    if tp.result:
                        exam_type = self.dbh.get_examtype_by_id(tp.exam.exam_type)
                        if tp.result:
                            t_p_result_sum += tp.result * exam_type.weight
                            t_p_result_count += exam_type.weight

                if t_p_result_count:
                    t_p_result_average = round(float(t_p_result_sum)/t_p_result_count, DIVISOR_PRECISION)

                if t_p_result_sum:
                    if self.config['schoolyear_result_calculation_method'] == 'complete':
                        complete_t_p_result_sum += t_p_result_sum * period[2]
                        complete_t_p_result_count += t_p_result_count * period[2]
                    elif self.config['schoolyear_result_calculation_method'] == 'timeperiod':
                        complete_t_p_result_sum += t_p_result_average * period[2]
                        complete_t_p_result_count += period[2]
                    else:
                        print("unknown calculation method")

                data_list.append((t_p_result_average, 100))

            if complete_t_p_result_count:
                complete_t_p_result_average = round(float(complete_t_p_result_sum)/complete_t_p_result_count, DIVISOR_PRECISION)
            data_list.append((complete_t_p_result_average, 100))

            self.print_content(root, y_pos, data_list)
            y_pos += 20

        return y_pos
