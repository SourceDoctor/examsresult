from os.path import isfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from examsresult.controls.dbupdater import DBUpdater
from examsresult.models import Exam, ExamResult, SchoolClassName, Student, Schoolyear, \
    ExamType, Subject, Parameter, Base


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

    def _delete(self, model, id):
        db_data = self.session.query(model).filter(model.id==id)
        self.session.delete(db_data)
        self.session.commit()
        return 0

    def _add(self, model, *data):
        db_data = model(data)
        self.session.add(db_data)
        self.session.commit()
        return 0

    def _update(self, model, id, *data):
        ret = 0
        db_data = self.session.query(model).filter(model.id==id)
        if not db_data:
            ret = self._add(model,*data)
        else:
            for k, v in db_data.keys():
                db_data.k = v
            self.session.update(data)
        self.session.commit()
        return ret

    def _list(self, model, filter={}):
        return self.session.query(model).filter_by(filter)

    def get_schoolyears(self):
        ret = self._list(Schoolyear)
        return ret.all()

    def get_schoolclassname(self, filter={}):
        ret = self._list(SchoolClassName)
        return ret.all()

    def set_schoolclassname(self, data):
        for d in data:
            s = self.session.query(SchoolClassName).filter(id==d[0]).first()
            if not s:
                s = SchoolClassName(name=d[1])
            else:
                s.name = d[1]
            self.session.add(s)

        self.session.commit()

        return 0

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

    def get_exam_types(self):
        ret = self._list(ExamType)
        return ret.all()

    def get_subject(self):
        ret = self._list(Subject)
        return ret.all()

    def get_parameter(self, filter_key):
        ret = self._list(Parameter, {'key': filter_key})
        return ret.all()