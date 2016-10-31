from sqlalchemy import Column, Integer, Float, ForeignKey, Unicode, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# https://sqlalchemy-migrate.readthedocs.io/en/latest/

db_version = 1


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
    comment = Column(Unicode(1024), nullable=True)

    __table_args__ = (
        UniqueConstraint('schoolyear', 'schoolclass', name='school_class-unique-constraint'),
    )


class Exam(Base):
    __tablename__ = 'exam'
    date = Column(Integer, nullable=False)

    subject = Column(Unicode(256), ForeignKey('subject.name'))
    exam_type = Column(Integer, ForeignKey('exam_type.id'))
    time_period = Column(Integer, ForeignKey('time_period.id'))
    school_class_id = Column(Integer, ForeignKey('school_class.id'))

    single_test = Column(Boolean, default=False, nullable=False)
    comment = Column(Unicode(1024), nullable=True)


class ExamResult(Base):
    __tablename__ = 'exam_result'
    result = Column(Float(precision=1), default=0)

    exam_id = Column(Integer, ForeignKey('exam.id'))
    exam = relationship("Exam", backref="exam_results")

    student = Column(Integer, ForeignKey('student.id'))
    comment = Column(Unicode(1024), nullable=True)


class Student(Base):
    __tablename__ = 'student'
    firstname = Column(Unicode(256))
    lastname = Column(Unicode(256))
    comment = Column(Unicode(1024), nullable=True)

    school_class_id = Column(Integer, ForeignKey('school_class.id'))
    school_class = relationship("SchoolClass", backref="students")

    __table_args__ = (
        UniqueConstraint('firstname', 'lastname', 'school_class_id', name='student-unique-constraint'),
    )
