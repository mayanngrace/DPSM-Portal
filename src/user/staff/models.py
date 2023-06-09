from stat import FILE_ATTRIBUTE_SPARSE_FILE
from src import db
from flask_login import UserMixin
from flask import current_app as app
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy import *
from sqlalchemy.schema import FetchedValue

schema = 'public'

class FacultyPersonalInformation(UserMixin, db.Model):
    __table_args__ = {
        'schema' : schema, 
        'extend_existing': True
    }
    __tablename__ = 'faculty_personal_information'
    user_id 					= db.Column(db.String(180), primary_key=True, nullable=True)
    rank                        = db.Column(db.String(180), nullable=True)
    classification              = db.Column(db.String(180), nullable=True)
    status                      = db.Column(db.String(180), nullable=True)
    tenure                      = db.Column(db.String(180), nullable=True)
    first_name                  = db.Column(db.String(180), nullable=True)
    middle_name                 = db.Column(db.String(180), nullable=True)
    last_name                   = db.Column(db.String(180), nullable=True)
    suffix                      = db.Column(db.String(180), nullable=True)
    date_of_birth               = db.Column(DATE, nullable=True)
    place_of_birth              = db.Column(db.String(180), nullable=True)
    present_address             = db.Column(db.String(180), nullable=True)
    permanent_address           = db.Column(db.String(180), nullable=True)
    civil_status                = db.Column(db.String(180), nullable=True)
    religion                    = db.Column(db.String(180), nullable=True)
    landline                    = db.Column(db.String(180), nullable=True)
    mobile_number               = db.Column(db.String(180), nullable=True)
    primary_email               = db.Column(db.String(180), nullable=True)
    alternate_email             = db.Column(db.String(180), nullable=True)
    emergency_contact_person    = db.Column(db.String(180), nullable=True)
    emergency_contact_number    = db.Column(db.String(180), nullable=True)
    dependent_name              = db.Column(db.String(180), nullable=True)
    dependent_birthdate         = db.Column(db.String(180), nullable=True)
    dependent_relationship      = db.Column(db.String(180), nullable=True)
    info_status                 = db.Column(db.Boolean, nullable=True)
    last_modified               = db.Column(TIMESTAMP, nullable=True)
    date_created                = db.Column(DATE, nullable=True)
    created_by                  = db.Column(db.String(180), nullable=True)
    unit 					    = db.Column(db.String(180), nullable=True)

class EducationalAttainment(UserMixin, db.Model):
    __table_args__ = {
        'schema' : schema, 
        'extend_existing': True
    }
    __tablename__ = 'educational_attainment'
    user_id = db.Column(db.String(180), nullable=True)
    school = db.Column(db.String(180), nullable=True)
    degree = db.Column(db.String(180), nullable=True)
    specialization = db.Column(db.String(180), nullable=True)
    degree_type = db.Column(db.String(180), nullable=True)
    start_date = db.Column(DATE, nullable=True)
    end_date = db.Column(DATE, nullable=True)
    proof_ext = db.Column(db.String(180), nullable=True)
    info_status = db.Column(db.Boolean, nullable=True)
    last_modified = db.Column(TIMESTAMP, nullable=True)
    id = db.Column(db.String(180), primary_key=True, nullable=True) 

class WorkExperience(UserMixin, db.Model):
    __table_args__ = {
        'schema' : schema, 
        'extend_existing': True
    }
    __tablename__   = 'work_experience'
    user_id         = db.Column(db.String(180), nullable=True)
    location        = db.Column(db.String(180), nullable=True)
    name_employer   = db.Column(db.String(180), nullable=True)
    title           = db.Column(db.String(180), nullable=True)
    description     = db.Column(db.String(180), nullable=True)
    start_date      = db.Column(DATE, nullable=True)
    end_date        = db.Column(DATE, nullable=True)
    proof_ext = db.Column(db.String(180), nullable=True)
    info_status = db.Column(db.Boolean, nullable=True)
    last_modified   = db.Column(TIMESTAMP, nullable=True)
    id              = db.Column(db.String(180), primary_key=True, nullable=True) 

class Accomplishment(UserMixin, db.Model):
    __table_args__ = {
        'schema' : schema, 
        'extend_existing': True
    }
    __tablename__       = 'accomplishments'
    user_id             = db.Column(db.String(180), nullable=True)
    position            = db.Column(db.String(180), nullable=True)
    organization        = db.Column(db.String(180), nullable=True)
    type_contribution   = db.Column(db.String(180), nullable=True)
    description         = db.Column(db.String(180), nullable=True)
    proof_ext = db.Column(db.String(180), nullable=True)
    info_status = db.Column(db.Boolean, nullable=True)
    start_date          = db.Column(DATE, nullable=True)
    end_date            = db.Column(DATE, nullable=True)
    last_modified       = db.Column(TIMESTAMP, nullable=True)
    id                  = db.Column(db.String(180), primary_key=True, nullable=True) 

    def __repr__(self):
        return f'<Position {self.position}, Organization {self.organization}, Type {self.type_contribution},\
            Description {self.description}, Proof {self.proof_ext}, Start Date {self.start_date}, End Date {self.end_date}, Last Modified {self.last_modified}>'

class Publication(UserMixin, db.Model):
    __table_args__ = {
        'schema' : schema, 
        'extend_existing': True
    }
    __tablename__       = 'publications'
    user_id             = db.Column(db.String(180), nullable=True)
    publication         = db.Column(db.String(180), nullable=True)
    citation            = db.Column(db.String(180), nullable=True)
    url                 = db.Column(db.String(180), nullable=True)
    coauthors_dpsm      = db.Column(db.String(180), nullable=True)
    coauthors_nondpsm   = db.Column(db.String(180), nullable=True)
    proof_ext           = db.Column(db.String(180), nullable=True)
    info_status         = db.Column(db.Boolean, nullable=True)
    date_published      = db.Column(DATE, nullable=True)
    last_modified       = db.Column(TIMESTAMP, nullable=True)
    id                  = db.Column(db.String(180), primary_key=True, nullable=True) 

class ResearchGrant(UserMixin, db.Model):
    __table_args__ = {
        'schema' : schema, 
        'extend_existing': True
    }
    __tablename__       = 'research_grants'
    user_id             = db.Column(db.String(180), nullable=True)
    name_research       = db.Column(db.String(180), nullable=True)
    sponsor             = db.Column(db.String(180), nullable=True)
    amount_granted      = db.Column(db.String(180), nullable=True)
    progress   = db.Column(db.String(180), nullable=True)
    coresearchers_dpsm      = db.Column(db.String(180), nullable=True)
    coresearchers_nondpsm   = db.Column(db.String(180), nullable=True)
    proof_ext = db.Column(db.String(180), nullable=True)
    info_status = db.Column(db.Boolean, nullable=True)
    projected_start     = db.Column(DATE, nullable=True)
    projected_end       = db.Column(DATE, nullable=True)
    actual_start        = db.Column(DATE, nullable=True)
    actual_end          = db.Column(DATE, nullable=True)
    last_modified       = db.Column(TIMESTAMP, nullable=True)
    id                  = db.Column(db.String(180), primary_key=True, nullable=True) 

    def __repr__(self):
        return f'<Research Name {self.name_research}, Sponsor {self.sponsor}, Amount Granted {self.amount_granted},\
            Progress {self.progress}, Projected Start {self.projected_start}, Projected End {self.projected_end},\
                Actual Start {self.actual_start}, Actual End {self.actual_end}, Co-researchers (DPSM) {self.coresearchers_dpsm},\
                    Co-researchers (Non-DPSM) {self.coresearchers_nondpsm}, Proof {self.proof_ext}, Last Modified {self.last_modified}>'

class LicensureExams(UserMixin, db.Model):
    __table_args__ = {
        'schema':schema,
        'extend_existing': True
    }
    __tablename__ = 'licensure_exams'
    user_id                     = db.Column(db.String(180), nullable=True)
    id                          = db.Column(db.String(180), primary_key=True, nullable=True)
    name_exam                   = db.Column(db.String(180), nullable=True)
    rank                        = db.Column(db.String(180), nullable=True)
    license_number              = db.Column(db.String(180), nullable=True)
    date                        = db.Column(DATE, nullable=True)
    proof_ext                   = db.Column(db.String(180), nullable=True)
    info_status                 = db.Column(db.Boolean, nullable=True)
    last_modified               = db.Column(TIMESTAMP, nullable=True)
    
    def __repr__(self):
        return f'<Licensure Exam Name {self.name_exam},\
            Rank {self.rank}, License Number {self.license_number},\
                Date {self.date}, Proof {self.proof_ext}, Last Modified {self.last_modified}>'

class TrainingSeminar(UserMixin, db.Model):
    __table_args__ = {
        'schema':schema,
        'extend_existing': True
    }
    __tablename__ = 'training_seminar'
    user_id                     = db.Column(db.String(180), nullable=True)
    id                          = db.Column(db.String(180), primary_key=True, nullable=True)
    name_training               = db.Column(db.String(180), nullable=True)
    role                        = db.Column(db.String(180), nullable=True)
    remarks                     = db.Column(db.String(180), nullable=True)
    start_date                  = db.Column(DATE, nullable=True)
    end_date                    = db.Column(DATE, nullable=True)
    proof_ext                   = db.Column(db.String(180), nullable=True)
    info_status                 = db.Column(db.Boolean, nullable=True)
    last_modified               = db.Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return f'<Training/Seminar Name {self.name_training},\
            Role {self.role}, Remarks {self.remarks},\
                Start Date {self.start_date}, End Date {self.end_date}, Proof {self.proof_ext}, Last Modified {self.last_modified}>'

class FacultySETRecords(UserMixin, db.Model):
    __table_args__ = {
        'schema':schema,
        'extend_existing': True
    }
    __tablename__ = 'faculty_set_records'
    seq_id                      = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    id                          = db.Column(db.String(180), nullable=True)
    course_code                 = db.Column(db.String(180), nullable=True)
    section                     = db.Column(db.String(180), nullable=True)
    semester                    = db.Column(db.String(180), nullable=True)
    sy                          = db.Column(db.String(180), nullable=True)
    schedule                    = db.Column(db.String(180), nullable=True)
    number_students             = db.Column(db.String(180), nullable=True)
    fsr_score                   = db.Column(db.String(180), nullable=True) 
    set_score                   = db.Column(db.String(180), nullable=True)
    last_modified               = db.Column(TIMESTAMP, nullable=True)
    syllabus_f_ext              = db.Column(db.String(180), nullable=True)
    set_f_ext                   = db.Column(db.String(180), nullable=True)
    # status                      = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return f'<Course Code {self.course_code}, Section {self.section}, Semester {self.semester}\
            SY {self.sy}, Schedule {self.schedule}, Number of Students {self.number_students}\
                FSR Score {self.fsr_score}, SET Score {self.set_score}, Last Modified {self.last_modified}>\
                    Syllabus {self.syllabus_f_ext}, SET Proof {self.set_f_ext}'

class UnitHeadNominations(UserMixin, db.Model):
    __table_args__ = {
        'schema':schema,
        'extend_existing': True
    }
    __tablename__ = 'unit_head_nominations'
    id                          = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    curr_unit_head              = db.Column(db.String(180), nullable=True)
    nominated_unit_head         = db.Column(db.String(180), nullable=True)
    approval_status             = db.Column(db.String(180), nullable=True)
    approver_remarks            = db.Column(db.String(180), nullable=True)
    status                      = db.Column(db.Boolean, nullable=True, default=True)
    unit                        = db.Column(db.String(180), nullable=True)

class ClerkPeronsalInformation(UserMixin, db.Model):
    __table_args__ = {
        'schema':schema,
        'extend_existing': True
    }
    __tablename__ = 'clerk_personal_information'
    id                          = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name                        = db.Column(db.String(180), nullable=True)
    user_id                     = db.Column(db.String(180), nullable=True)

class RejectedInfo(UserMixin, db.Model):
    __table_args__ = {
        'schema' : schema, 
        'extend_existing': True
    }
    __tablename__ = 'rejected_info'
    seq_id          = db.Column(db.Integer, primary_key=True, nullable=True)
    info_by         = db.Column(db.String(180), nullable=True)
    info_id         = db.Column(db.String(180), nullable=True)
    remarks         = db.Column(db.String(180), nullable=True)
    rejected_by     = db.Column(db.String(180), nullable=True)