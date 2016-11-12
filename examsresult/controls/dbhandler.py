from os.path import isfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from examsresult.controls.dbupdater import DBUpdater
from examsresult.models import Exam, ExamResult, SchoolClassName, Student, Schoolyear, \
    SchoolClass, ExamType, TimePeriod, Subject, Parameter, Base


class DatabaseConnector(object):

    engine = None
    session = None
    database = None
    databasefile = None

    def __init__(self, databasefile, dbtype='sqlite'):
        if dbtype == 'sqlite':
            db_type = "sqlite:///"
        else:
            print("unknown Database Type")
            pass

        self.databasefile = databasefile
        self.database = "%s%s"  % (db_type, databasefile)
        self.engine = self._create_db_engine()
        self._create_session()

    def _create_db_engine(self):
        if not isfile(self.databasefile):
            self._create_database()

        self.engine = create_engine(self.database)
        return self.engine

    def _create_session(self):
        self.session = sessionmaker(bind=self.engine)()
        return self.session

    def _create_database(self):
        Base.metadata.bind = self.database
        Base.metadata.create_all(self.engine)

    def db_updater(self):
        dbu = DBUpdater(self.session)
        return dbu.dbupdater()


class DBHandler(object):

    def __init__(self, database_filename):
        self.dbc = DatabaseConnector(database_filename)
        self.session = self.dbc.session

    def _list(self, model, filter={}):
        if filter:
            return self.session.query(model).filter_by(filter)
        else:
            return self.session.query(model)

    def get_schoolclassstudents(self, schoolyear=None, schoolclass=None):
        student_list = []
        class_data = self.session.query(SchoolClass)
        if schoolyear:
            class_data = class_data.filter(SchoolClass.schoolyear==schoolyear)
        if schoolclass:
            class_data = class_data.filter(SchoolClass.schoolclass==schoolclass)

        class_data = class_data.all()
        for c in class_data:
            students = self.session.query(Student).filter(Student.school_class_id == c.id).all()
            for s in students:
                student_list.append((s.id, s.lastname, s.firstname, s.comment))
        return student_list

    def get_schoolyear(self):
        ret = self._list(Schoolyear)
        data = []
        for d in ret.all():
            data.append((d.id, d.name))
        return data

    def set_schoolyear(self, data):
        for d in data:
            if d[0] != '':
                s = self.session.query(Schoolyear).filter(Schoolyear.id==int(d[0])).first()
            else:
                s = None
            if not s:
                s = Schoolyear(name=d[1])
            else:
                s.name = d[1]
            self.session.add(s)

        self.session.commit()
        return 0

    def get_schoolclassname(self, schoolyear=None):
        data = []
        ret = self._list(SchoolClass)
        if schoolyear:
            ret = ret.filter(SchoolClass.schoolyear==schoolyear)
        for d in ret.all():
            data.append((d.id, d.schoolclass))
        return data

    def set_schoolclassname(self, data):
        for d in data:
            if d[0] != '':
                s = self.session.query(SchoolClassName).filter(SchoolClassName.id==int(d[0])).first()
            else:
                s = None
            if not s:
                s = SchoolClassName(name=d[1])
            else:
                s.name = d[1]
            self.session.add(s)

        self.session.commit()
        return 0

    def get_schoolclass_id(self, schoolyear, schoolclassname):
        school_class_row = self.session.query(SchoolClass).filter(SchoolClass.schoolyear==schoolyear). \
            filter(SchoolClass.schoolclass==schoolclassname).first()
        if school_class_row:
            return school_class_row.id
        return None

    def get_schoolclass_data(self, id):
        school_class_row = self.session.query(SchoolClass).filter(SchoolClass.id==id).first()
        if school_class_row:
            return school_class_row
        return None

    def get_examtype_id(self, examtype):
        ret = self.session.query(ExamType).filter(ExamType.name == examtype).first()
        if ret:
            return ret.id
        return None

    def get_timeperiod_id(self, timeperiod):
        ret = self.session.query(TimePeriod).filter(TimePeriod.name == timeperiod).first()
        if ret:
            return ret.id
        return None

    def get_subject(self):
        ret = self._list(Subject)
        data = []
        for d in ret.all():
            data.append((d.id, d.name))
        return data

    def set_subject(self, data):
        for d in data:
            if d[0] != '':
                s = self.session.query(Subject).filter(Subject.id==int(d[0])).first()
            else:
                s = None
            if not s:
                s = Subject(name=d[1])
            else:
                s.name = d[1]
            self.session.add(s)

        self.session.commit()
        return 0

    def get_examtype(self):
        ret = self._list(ExamType)
        data = []
        for d in ret.all():
            data.append((d.id, d.name, d.weight))
        return data

    def get_examtype_by_id(self, id):
        ret = self.session.query(ExamType).filter(ExamType.id == id).first()
        if ret:
            return ret
        return None

    def set_examtype(self, data):
        for d in data:
            if d[0] != '':
                s = self.session.query(ExamType).filter(ExamType.id==int(d[0])).first()
            else:
                s = None
            if not s:
                s = ExamType(name=d[1], weight=d[2])
            else:
                s.name = d[1]
            self.session.add(s)

        self.session.commit()
        return 0

    def get_timeperiod(self):
        ret = self._list(TimePeriod)
        data = []
        for d in ret.all():
            data.append((d.id, d.name, d.weight))
        return data

    def get_timeperiod_by_id(self, id):
        ret = self.session.query(TimePeriod).filter(TimePeriod.id==id).first()
        if ret:
            return ret
        return None

    def set_timeperiod(self, data):
        for d in data:
            if d[0] != '':
                s = self.session.query(TimePeriod).filter(TimePeriod.id==int(d[0])).first()
            else:
                s = None
            if not s:
                s = TimePeriod(name=d[1], weight=d[2])
            else:
                s.name = d[1]
                s.weight = d[2]

            self.session.add(s)

        self.session.commit()
        return 0

    def get_student_data(self, id):
        return self.session.query(Student).filter(Student.id==id).first()

    def get_students(self, schoolyear, schoolclass):
        ret = self._list(SchoolClass)
        ret = ret.filter(SchoolClass.schoolyear==schoolyear)
        ret = ret.filter(SchoolClass.schoolclass==schoolclass)
        school_class = ret.first()

        data = []
        if school_class:
            for d in school_class.students:
                data.append((d.id, d.lastname, d.firstname, d.comment))
        return data

    def set_students(self, schoolyear, schoolclass, students=[]):
        s = self.session.query(SchoolClass).filter(SchoolClass.schoolyear==schoolyear)
        s.filter(SchoolClass.schoolclass==schoolclass)
        school_class = s.first()

        if not school_class:
            # create new school class
            school_class = SchoolClass(schoolyear=schoolyear,
                                schoolclass=schoolclass,
                               )
            self.session.add(school_class)
            self.session.commit()
            # get the row back in secure way:
            s = self.session.query(SchoolClass).filter(SchoolClass.schoolyear == schoolyear)
            s.filter(SchoolClass.schoolclass == schoolclass)
            school_class = s.first()

        # collect all students found for class
        id_list = []
        for student in school_class.students:
            id_list.append(str(student.id))

        # now refresh student assignment -------------------------
        for d in students:
            if d[0] != '':
                s = self.session.query(Student).filter(Student.id == int(d[0])).first()
            else:
                s = None
            if not s:
                s = Student(lastname=d[1], firstname=d[2], comment=d[3])
            else:
                id_list.remove(str(d[0]))
                s.lastname = d[1]
                s.firstname = d[2]
                s.comment = d[3]
            s.school_class = school_class
            self.session.add(s),

        self.session.commit()
        return 0

    def get_exams(self, schoolyear, schoolclassname, subject):
        exam_list = []

        school_class_id = self.get_schoolclass_id(schoolyear, schoolclassname)
        if school_class_id:
            x_list = self.session.query(Exam).filter(Exam.school_class_id == school_class_id).filter(
                Exam.subject == subject).all()
        else:
            x_list = []

        for x in x_list:
            count = 0
            sum = 0
            average = 0
            for r in x.exam_results:
                if r.result:
                    count += 1
                    sum += r.result
            if count:
                average = round(sum/count, 2)

            written_count = "%d/%d" % (count, len(x.exam_results))
            x_type = self.session.query(ExamType).filter(ExamType.id == x.exam_type).first()
            x_timeperiod = self.session.query(TimePeriod).filter(TimePeriod.id == x.time_period).first()
            exam_list.append((x.id, x.date, x_type.name, x_timeperiod.name, written_count, average, x.comment))

        return exam_list

    def exam_is_unique(self, exam_date, schoolyear, schoolclass, subject, examtype, timeperiod):
        school_class_id = self.get_schoolclass_id(schoolyear, schoolclass)
        ret = self.get_exam(exam_date, school_class_id, subject, examtype, timeperiod)
        if ret:
            return False
        return True

    def get_exam(self, exam_date, school_class_id, subject, examtype, timeperiod):
        examtype_id = self.get_examtype_id(examtype)
        timeperiod_id = self.get_timeperiod_id(timeperiod)

        ret = self.session.query(Exam). \
            filter(Exam.date==exam_date). \
            filter(Exam.school_class_id==school_class_id). \
            filter(Exam.subject==subject). \
            filter(Exam.exam_type==examtype_id). \
            filter(Exam.time_period==timeperiod_id).first()
        return ret

    def get_exam_by_id(self, exam_id):
        ret = self.session.query(Exam).filter(Exam.id == exam_id).first()
        return ret

    def set_exam(self, exam_date, schoolyear, schoolclassname, subject, examtype, timeperiod, results, comment, id=None):

        school_class_id = self.get_schoolclass_id(schoolyear, schoolclassname)
        examtype_id = self.get_examtype_id(examtype)
        timeperiod_id = self.get_timeperiod_id(timeperiod)
        subject_row = self.session.query(Subject).filter(Subject.name==subject).first()

        if id:
            x = self.get_exam_by_id(id)
        else:
            x = self.get_exam(exam_date, school_class_id, subject_row.name, examtype, timeperiod)
        if not x:
            x = Exam(date=exam_date,
                     school_class_id=school_class_id,
                     subject=subject_row.name,
                     exam_type=examtype_id,
                     time_period=timeperiod_id,
                     comment=comment
                     )
            self.session.add(x)
            self.session.commit()
            x = self.get_exam(exam_date, school_class_id, subject_row.name, examtype, timeperiod)
        else:
            x.date = exam_date
            x.subject = subject_row.name
            x.exam_type = examtype_id
            x.time_period = timeperiod_id
            x.comment = comment
            self.session.add(x)
            self.session.commit()

        for result in results:
            student_id = result[0]
            student_result = result[3]
            student_comment = result[4]
            self.set_exam_result(exam_id=x.id, student_id=student_id, result=student_result, comment=student_comment)

        return 0

    def remove_exam(self, exam_id):
        results = self.session.query(ExamResult).filter(ExamResult.exam_id==exam_id).all()
        for r in results:
            self.session.delete(r)

        x = self.session.query(Exam).filter(Exam.id == exam_id).first()
        self.session.delete(x)
        self.session.commit()
        return 0

    def get_exam_result(self, exam_id=None, student_id=None, subject=None, timeperiod_id=None):
        ret = self.session.query(ExamResult)
        if exam_id:
            ret = ret.filter(ExamResult.exam_id == exam_id)
        if student_id:
            ret = ret.filter(ExamResult.student == student_id)

        ret = ret.all()

        result = []
        if subject:
            for r in ret:
                if r.exam.subject != subject:
                    continue
                result.append(r)
        else:
            result = ret

        ret = result
        result = []
        if timeperiod_id:
            for t in ret:
                if t.exam.time_period != timeperiod_id:
                    continue
                result.append(t)
        else:
            result = ret

        return result

    def set_exam_result(self, exam_id, student_id, result, comment):
        r = self.get_exam_result(exam_id, student_id)
        if not r:
            r = ExamResult(result=result,
                           exam_id=exam_id,
                           student=student_id,
                           comment=comment)
        else:
            r = r[0]
            r.result = result
            r.comment = comment

        self.session.add(r)
        self.session.commit()

    def get_parameter(self, key):
        return self.session.query(Parameter).filter(Parameter.key==key).first()

    def set_parameter(self, key, value):
        p = self.get_parameter(key=key)
        if not p:
            p = Parameter(key=key,
                          value=value)
        else:
            p.value = value

        self.session.add(p)
        self.session.commit()
        return 0
