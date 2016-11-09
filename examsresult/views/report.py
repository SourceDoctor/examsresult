from PyQt5.QtWidgets import QWidget, QTableWidget, QLabel

from examsresult.views import CoreView


class ViewReport(CoreView):

    table_left = 100
    table_top = 130
    table_height = 350
    table_width = 500


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
