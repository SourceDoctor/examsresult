from sqlalchemy import Column, Integer, Float, ForeignKey, Unicode, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

db_version = 3

# all table column id
DB_ID_INDEX = 0
# table schoolclass - column schoolclass
DB_SCHOOLCLASS_SCHOOLCLASS_INDEX = 2

SYSTEM_VERSION_KEY = 'system_version'
DB_VERSION_KEY = 'db_version'


class Base(object):
    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(cls=Base)


class Version(Base):
    __tablename__ = 'version'
    key = Column(Unicode(256), unique=True, nullable=False)
    value = Column(Unicode(256), nullable=True)


class Parameter(Base):
    __tablename__ = 'parameter'
    key = Column(Unicode(256), unique=True, nullable=False)
    value = Column(Unicode(256), nullable=True)


class Schoolyear(Base):
    __tablename__ = 'school_year'
    name = Column(Unicode(256), unique=True, nullable=False)


class SchoolClassName(Base):
    __tablename__ = 'school_class_name'
    name = Column(Unicode(256), unique=True, nullable=False)


class Subject(Base):
    __tablename__ = 'subject'
    name = Column(Unicode(256), unique=True, nullable=False)


class ExamType(Base):
    __tablename__ = 'exam_type'
    name = Column(Unicode(256), unique=True, nullable=False)
    weight = Column(Float(precision=2), default=1, nullable=False)


class TimePeriod(Base):
    # weigth of first and second half of schoolyear, ...
    __tablename__ = 'time_period'
    name = Column(Unicode(256), unique=True, nullable=False)
    weight = Column(Float(precision=2), default=1, nullable=False)


class SchoolClass(Base):
    __tablename__ = 'school_class'
    schoolyear = Column(Unicode(256), ForeignKey('school_year.name'))
    schoolclass = Column(Unicode(256), ForeignKey('school_class_name.name'))
    # if school class is combined with students from several school classes
    # for a subject in example, specific sports, or religious seperations
    # then combined_schoolclass is set to True
    combined_schoolclass = Column(Boolean, default=False)
    comment = Column(Unicode(1024), nullable=True)

    __table_args__ = (
        UniqueConstraint('schoolyear', 'schoolclass', name='school_class-unique-constraint'),
    )


class Exam(Base):
    __tablename__ = 'exam'
    date = Column(Unicode(32), nullable=False)

    subject = Column(Unicode(256), ForeignKey('subject.name'))
    exam_type = Column(Integer, ForeignKey('exam_type.id'))
    time_period = Column(Integer, ForeignKey('time_period.id'))
    school_class_id = Column(Integer, ForeignKey('school_class.id'))
    exam_results = relationship("ExamResult", back_populates="exam")

    comment = Column(Unicode(1024), nullable=True)


class ExamResult(Base):
    __tablename__ = 'exam_result'
    result = Column(Float(precision=1), default=0)

    exam_id = Column(Integer, ForeignKey('exam.id'))
    exam = relationship("Exam", back_populates="exam_results")

    student = Column(Integer, ForeignKey('student.id'))
    comment = Column(Unicode(1024), nullable=True)


class Student(Base):
    __tablename__ = 'student'
    firstname = Column(Unicode(256))
    lastname = Column(Unicode(256))
    comment = Column(Unicode(1024), nullable=True)

    school_class_id = Column(Integer, ForeignKey('school_class.id'))
    school_class = relationship("SchoolClass", backref="students")
    # real school_class_name per default equal with school_class (value = 0),
    # if school class is mixed it shows the ID to school class, student is assigned to in school
    real_school_class_name_id = Column(Integer, default=0)
    image = Column(Unicode(64), nullable=True)

    __table_args__ = (
        UniqueConstraint('firstname', 'lastname', 'school_class_id', name='student-unique-constraint'),
    )
