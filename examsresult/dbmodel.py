from sqlalchemy import Column, Integer, Float, ForeignKey, Unicode, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# https://sqlalchemy-migrate.readthedocs.io/en/latest/

db_version = 1

class Base(object):
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)


class Parameter(Base):
    __tablename__ = 'parameter'
    key = Column(Unicode(256), unique=True, nullable=False)
    value = Column(Unicode(256), nullable=True)


class Schoolyear(Base):
    __tablename__ = 'school_year'
    name = Column(Unicode(256), nullable=False)


class SchoolClass(Base):
    __tablename__ = 'school_class'
    name = Column(Unicode(256), nullable=False)
    schoolyear = Column(Unicode(256), ForeignKey('school_year.name'))

    exams = relationship("Exam")


class Subject(Base):
    __tablename__ = 'subject'
    name = Column(Unicode(256), nullable=False)


class ExamType(Base):
    __tablename__ = 'exam_type'
    name = Column(Unicode(256), nullable=False)
    weight = Column(Float(precision=2), nullable=False)


class Exam(Base):
    __tablename__ = 'exam'
    date = Column(Integer, nullable=False)

    subject = Column(Unicode(256), ForeignKey('subject.name'))
    exam_type = Column(Integer, ForeignKey('exam_type.id'))
    school_class_id = Column(Integer, ForeignKey('school_class.id'))

    single_test = Column(Boolean, default=False, nullable=False)
    comment = Column(Unicode(1024), nullable=True)


class ExamResult(Base):
    __tablename__ = 'exam_result'
    result = Column(Integer, default=0)

    exam_id = Column(Integer, ForeignKey('exam.id'))
    exam = relationship("Exam", backref="exam_results")

    student = Column(Integer, ForeignKey('student.id'))
    comment = Column(Unicode(1024), nullable=True)


class Student(Base):
    __tablename__ = 'student'
    name = Column(Unicode(256))

    school_class_id = Column(Integer, ForeignKey('school_class.id'))
    school_class = relationship("SchoolClass", backref="students")
