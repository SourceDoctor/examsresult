from os.path import isfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from examsresult.controls.dbupdater import DBUpdater
from examsresult.models import Exam, ExamResult, SchoolClassName, Student, Schoolyear, \
    ExamType, TimePeriod, Subject, Parameter, Base


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

    def get_schoolyear(self):
        ret = self._list(Schoolyear)
        data = []
        for d in ret.all():
            data.append((d.id, d.name))
        return data

    def set_schoolyear(self, data):
        for d in data:
            if d[0] != '':
                id = int(d[0])
                s = self.session.query(Schoolyear).filter(id == id).first()
            else:
                s = None
            if not s:
                s = Schoolyear(name=d[1])
            else:
                s.name = d[1]
            self.session.add(s)

        self.session.commit()
        return 0

    def get_schoolclassname(self, filter={}):
        ret = self._list(SchoolClassName)
        data = []
        for d in ret.all():
            data.append((d.id, d.name))
        return data

    def set_schoolclassname(self, data):
        for d in data:
            if d[0] != '':
                id = int(d[0])
                s = self.session.query(SchoolClassName).filter(id == id).first()
            else:
                s = None
            if not s:
                s = SchoolClassName(name=d[1])
            else:
                s.name = d[1]
            self.session.add(s)

        self.session.commit()
        return 0

    def get_subject(self):
        ret = self._list(Subject)
        data = []
        for d in ret.all():
            data.append((d.id, d.name))
        return data


    def set_subject(self, data):
        for d in data:
            print(str(d))
            if d[0] != '':
                id = int(d[0])
                s = self.session.query(Subject).filter(id == id).first()
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

    def set_examtype(self, data):
        for d in data:
            if d[0] != '':
                id = int(d[0])
                s = self.session.query(ExamType).filter(id == id).first()
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

    def set_timeperiod(self, data):
        for d in data:
            if d[0] != '':
                id = int(d[0])
                s = self.session.query(TimePeriod).filter(id == id).first()
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

    # ----------- still not used functions -----------------------------------------

    def get_exams(self, filter={}):
        ret = self._list(Exam)

        if 'schoolclass' in filter.keys():
            ret = ret.filter(Exam.school_class_id.name == filter['schoolclass'])
        if 'student' in filter.keys():
            ret = ret.filter(Exam.student.name == filter['student'])
        return ret.all()

    def get_exam_result(self, filter={}):
        ret = self._list(ExamResult)

        if 'schoolclass' in filter.keys():
            ret = ret.filter(ExamResult.student.school_class.name == filter['schoolchlass'])
        if 'student' in filter.keys():
            ret = ret.filter(ExamResult.student.name == filter['student'])
        return ret.all()

    def get_students(self, filter={}):
        ret = self._list(Student)

        if 'schoolclass' in filter.keys():
            ret = ret.filter(Student.school_class.name == filter['schoolclass'])
        return ret.all()

    def get_parameter(self, filter_key):
        ret = self._list(Parameter, {'key': filter_key})
        return ret.all()