from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QAbstractItemView, QMenu, QToolButton

from examsresult import current_config
from examsresult.tools import HIDE_ID_COLUMN
from examsresult.views import CoreView

DIVISOR_PRECISION = 2


class ViewReport(CoreView):

    table_left = 30
    table_top = 130
    table_height = 350
    table_width = 600

    y_pos = 10

    show_schoolyear = True
    show_schoolclass = True
    show_subject = True
    show_student = False

    sorting = False

    def __init__(self, dbhandler, root_tab, lng, data):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng
        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())
        self.config = current_config

        mytab = QWidget()

        self.my_table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, self.lng['title'])

        if self.show_schoolyear:
            self.schoolyear = data['schoolyear']
            label_schoolyear_description = QLabel(self.lng['schoolyear'], mytab)
            label_schoolyear_description.move(10, self.y_pos)
            label_schoolyear_description = QLabel(self.schoolyear, mytab)
            label_schoolyear_description.move(100, self.y_pos)
            self.y_pos += 20

        if self.show_schoolclass:
            self.schoolclass = data['schoolclass']
            label_schoolclass_description = QLabel(self.lng['schoolclass'], mytab)
            label_schoolclass_description.move(10, self.y_pos)
            label_schoolclass_description = QLabel(self.schoolclass, mytab)
            label_schoolclass_description.move(100, self.y_pos)
            self.y_pos += 20

        if self.show_subject:
            self.subject = data['subject']
            label_subject_description = QLabel(self.lng['subject'], mytab)
            label_subject_description.move(10, self.y_pos)
            label_subject_description = QLabel(self.subject, mytab)
            label_subject_description.move(100, self.y_pos)
            self.y_pos += 20

        if self.show_student:
            self.student_id = data['student_id']
            s = self.dbh.get_student_data(self.student_id)
            self.student = "%s, %s" % (s.lastname, s.firstname)

            label_student_description = QLabel(self.lng['student'], mytab)
            label_student_description.move(10, self.y_pos)
            label_student_description = QLabel(self.student, mytab)
            label_student_description.move(100, self.y_pos)
            self.y_pos += 20

        self.y_pos += 20
        label_results = QLabel(self.lng['results'], mytab)
        label_results.move(self.table_left, self.y_pos)

        self.y_pos += 20
        self.table_top = self.y_pos
        self.my_table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

        self.my_table.setColumnCount(len(self.column_title))

        self.my_table.verticalHeader().setVisible(self.header_vertical)
        self.my_table.horizontalHeader().setVisible(self.header_horizontal)

        column_tuple = ()
        for col in self.column_title:
            column_tuple += (col['name'],)
        self.my_table.setHorizontalHeaderLabels(column_tuple)

        self.button_export = QToolButton(mytab)
        self.button_export.move(self.table_left + self.table_width + 10, self.table_top)
        self.button_export.setText(self.lng['export'])
        self.button_export.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        menu.addAction(self.lng['csv_export'], lambda: self.do_csv_export())
        menu.addAction(self.lng['pdf_export'], lambda: self.do_pdf_export(self.export_file_title))
        self.button_export.setMenu(menu)

        # hide Column 'id'
        self.my_table.setColumnHidden(0, HIDE_ID_COLUMN)

        if self.row_title:
            self.my_table.setVerticalHeaderLabels(self.row_title)

        if self.full_row_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        if self.full_column_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectColumns)

        if self.cell_editable:
            self.my_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Fixme: on doubleclick-Edit Cell has blinking Cursor focus

        self.load_data()

        self.my_table.resizeColumnsToContents()
        self.my_table.setSortingEnabled(self.sorting)

    def do_csv_export(self):
        self.configure_export_csv(parent=self.tab_window, default_filename=self.export_file_title)

    @property
    def export_file_title(self):
        return ""


class ViewReportSchoolclass(ViewReport):

    def _define_column_title(self):
        timeperiod_list = self.dbh.get_timeperiod()
        column_title = []

        column_title.append({'name': self.lng['student'], 'type': 'string', 'unique': False})
        for period in timeperiod_list:
            column_title.append({'name': period[1], 'type': 'string', 'unique': False})
        column_title.append({'name': self.lng['schoolyear'], 'type': 'string', 'unique': False})

        return column_title

    @property
    def export_file_title(self):
        return "%s_%s" % (self.schoolyear, self.schoolclass)

    def _action_load_content(self):
        return self.show_results()

    def show_results(self):

        result_list = []
        result_count = 1

        timeperiod_list = self.dbh.get_timeperiod()

        for student in self.dbh.get_students(self.schoolyear, self.schoolclass):
            name = "%s, %s" % (student[1], student[2])
            data_list = (result_count, name)
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
                data_list += (t_p_result_average,)

            if complete_t_p_result_count:
                complete_t_p_result_average = round(float(complete_t_p_result_sum)/complete_t_p_result_count, DIVISOR_PRECISION)
            data_list += (complete_t_p_result_average,)

            # print student result
            result_list.append(data_list)
            result_count += 1

        return result_list

    def pdf_template(self, obj, data):
        # Todo: Feed me
        obj.drawString(100, 750, "empty Report Schoolclass Template")


class ViewReportStudent(ViewReport):

    show_student = True

    def _define_column_title(self):
        return [{'name': self.lng['date'], 'type': 'string', 'unique': False},
                {'name': self.lng['timeperiod'], 'type': 'string', 'unique': False},
                {'name': self.lng['examtype'], 'type': 'string', 'unique': False},
                {'name': self.lng['result'], 'type': 'string', 'unique': False},
                {'name': self.lng['periodresult'], 'type': 'string', 'unique': False},
                {'name': self.lng['comment'], 'type': 'string', 'unique': False},
                ]

    def _action_load_content(self):
        return self.show_results()

    @property
    def export_file_title(self):
        return "%s_%s_%s" % (self.schoolclass, self.subject, self.student)

    def show_results(self):

        timeperiod_list = self.dbh.get_timeperiod()
        complete_t_p_result_sum = 0
        complete_t_p_result_count = 0
        complete_t_p_result_average = 0

        result_list = []
        result_count = 1

        for period in timeperiod_list:
            t_p_result_sum = 0
            t_p_result_count = 0
            t_p_result_average = 0

            results = self.dbh.get_exam_result(student_id=self.student_id, subject=self.subject,
                                               timeperiod_id=period[0])
            for r in results:
                x_t = self.dbh.get_examtype_by_id(r.exam.exam_type)
                if r.result:
                    t_p_result_sum += r.result * x_t.weight
                    t_p_result_count += x_t.weight
                # print result
                result_list.append((result_count, r.exam.date, period[1], x_t.name, r.result, "", r.comment))
                result_count += 1

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
            # print Average
            result_list.append((result_count, "", period[1], "", "", t_p_result_average, ""))
            result_count += 1

        if complete_t_p_result_count:
            complete_t_p_result_average = round(float(complete_t_p_result_sum)/complete_t_p_result_count, DIVISOR_PRECISION)

        # print schoolyear
        result_list.append((result_count, "", self.lng['schoolyear'], "", "", complete_t_p_result_average, ""))
        result_count += 1

        return result_list

    def pdf_template(self, obj, data):
        # Todo: Feed me
        obj.drawString(100, 750, "empty Report Student Template")
