import email
from sched import scheduler
from src import login_manager, db
from flask import Blueprint, render_template, redirect, url_for, flash, g
import flask
from flask import session
from flask import current_app as app
import flask_login
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, request
import os
from datetime import datetime as dt, date
from datetime import timedelta, date
import requests
import pip._vendor.cachecontrol as cacheControl
import json

#Models
from ..models import EducationalAttainment, FacultyPersonalInformation, FacultySETRecords, LicensureExams, TrainingSeminar, WorkExperience, Accomplishment, ResearchGrant, Publication, RejectedInfo
from ...auth.models import UserCredentials

#External Functions
# from .functions.generate_educational_attaintment_id import generate_educational_attainment_id
from .functions.generate_ids import generate_id

faculty_blueprint = Blueprint('faculty_blueprint', __name__)

EDUC_PROOF_DIR = r"src\static\img\educ_proof"
WORK_PROOF_DIR = r"src\static\img\work_proof"
ACC_PROOF_DIR = r"src\static\img\accomplishment_proof"
PUB_PROOF_DIR = r"src\static\img\publication_proof"
LIC_PROOF_DIR = r"src\static\img\licensure_proof"
RG_PROOF_DIR = r"src\static\img\research_grant_proof"
TS_PROOF_DIR = r"src\static\img\training_seminar_proof"
FSRSET_PROOF_DIR = r"src\static\img\fsr_set_proof"

@login_manager.user_loader
def load_user(user_id):
	return UserCredentials.query.get(user_id)

@faculty_blueprint.route('/faculty/faculty_landing_page', methods = ['GET', 'POST'])
@login_required
def view_info():
    try:
        if request.method == 'GET':
            personal_info = FacultyPersonalInformation.query.filter_by(user_id=current_user.user_id, info_status=None).first()
            educ_attainment = EducationalAttainment.query.filter_by(user_id=current_user.user_id, info_status=True).all()
            work_experience = WorkExperience.query.filter_by(user_id=current_user.user_id, info_status=True).all()
            accomplishment = Accomplishment.query.filter_by(user_id=current_user.user_id, info_status=True).all()
            publication = Publication.query.filter_by(user_id=current_user.user_id, info_status=True).all()
            licensure = LicensureExams.query.filter_by(user_id=current_user.user_id, info_status=True).all()
            research_grant = ResearchGrant.query.filter_by(user_id=current_user.user_id, info_status=True).all()
            training = TrainingSeminar.query.filter_by(user_id=current_user.user_id, info_status=True).all()
            fsr = FacultySETRecords.query.filter_by(id=current_user.user_id).all()

            rejected_info_id = RejectedInfo.query.with_entities(RejectedInfo.info_id)

            fsr_dict = {} # Keys = initial school year, Value = list of records within that year

            for  record in fsr:
                if record.sy in fsr_dict:
                    fsr_dict[record.sy].append(record.__dict__)
                else:
                    fsr_dict[record.sy] = [record.__dict__]

            return render_template(
                'faculty/faculty_landing_page.html',
                personal_info=personal_info,
                educ_attainment=educ_attainment,
                work_experience=work_experience,
                accomplishment=accomplishment,
                publication=publication,
                licensure=licensure,
                research_grant=research_grant,
                training=training,
                fsr_dict=fsr_dict,
                rejected_info_id=rejected_info_id
                )
        elif request.method == 'POST':
            pass
    except Exception as e:
        print(e)
        return e, 500


@faculty_blueprint.route('/faculty/faculty_landing_page/<string:filename>', methods=['GET'])
@login_required
def view_proof(id, proof_type, filename):
    try:
        CURR_FILE_DIR = os.path.join(proof_type, id)
        print(CURR_FILE_DIR)
        FILE_PATH = os.path.join(CURR_FILE_DIR, filename)
        _, proof_f_ext = os.path.splitext(filename)
        response = json.dumps({
            'proof_file':str(FILE_PATH),
            'file_ext':proof_f_ext
		})
        print(FILE_PATH)
        return response, 200
    except Exception as e:
        print(e)
        return 'Error displaying syllabus. Please try again.', 400


# # edit personal information
@faculty_blueprint.route('/faculty/update_personal_info', methods = ['GET', 'POST'])
@login_required
def update_personal_info():
    try:
        if request.method == 'GET':
            faculty_info_record = FacultyPersonalInformation.query.filter_by(user_id=current_user.user_id).first()
            return render_template(
            'faculty/update_info.html',
            faculty_info_record=faculty_info_record
            )
        elif request.method == 'POST':
            faculty_info_form = request.form
            faculty_info_record = FacultyPersonalInformation.query.filter_by(user_id=faculty_info_form['faculty_id_number']).first()

            faculty_info_record.first_name             = faculty_info_form['first_name'],
            faculty_info_record.middle_name            = faculty_info_form['middle_name'],
            faculty_info_record.last_name              = faculty_info_form['last_name'],
            faculty_info_record.suffix                 = faculty_info_form['suffix'],
            faculty_info_record.date_of_birth          = faculty_info_form['date_of_birth'],
            faculty_info_record.place_of_birth         = faculty_info_form['place_of_birth'],
            faculty_info_record.present_address        = faculty_info_form['present_address'],
            faculty_info_record.permanent_address      = faculty_info_form['permanent_address'],
            faculty_info_record.civil_status           = faculty_info_form['civil_status'],
            faculty_info_record.religion               = faculty_info_form['religion'],
            faculty_info_record.landline               = faculty_info_form['landline'],
            faculty_info_record.mobile_number          = faculty_info_form['mobile_number'],
            faculty_info_record.primary_email          = faculty_info_form['primary_email'],
            faculty_info_record.alternate_email        = faculty_info_form['alternate_email'],
            faculty_info_record.emergency_contact_person     = faculty_info_form['emergency_contact_person'],
            faculty_info_record.emergency_contact_number     = faculty_info_form['emergency_contact_number'],
            faculty_info_record.dependent_name          = faculty_info_form['dependent_name'],
            faculty_info_record.dependent_birthdate     = faculty_info_form['dependent_birthdate'],
            faculty_info_record.dependent_relationship  = faculty_info_form['dependent_relationship'],
            faculty_info_record.last_modified       = date.today()

            db.session.commit()

            flash('Personal Information Record Successfully Updated.', 200)
            return render_template('faculty/update_info.html',faculty_info_record=faculty_info_record)
    except Exception as e:
        print(e)
        return 'An error has occured.', 500

from pprint import pprint
from PIL import Image
@faculty_blueprint.route('/faculty/add_educational_attainment', methods=['GET', 'POST'])
@login_required
def add_educational_attainment():
    try:
        if request.method == 'GET':
            #pass
            return render_template('faculty/add_educational.html')
        elif request.method == 'POST':
            educational_attainment_form = request.form
            educational_attainment_files = request.files

            CURR_EDUC_PROOF_DIR = os.path.join(EDUC_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_EDUC_PROOF_DIR, exist_ok=True)

            educ_proof = educational_attainment_files['educ_proof']
            _, educ_proof_ext = os.path.splitext(educ_proof.filename)

            if (educ_proof_ext == '.jpg' or educ_proof_ext == '.png'):
                educ_proof_img = Image.open(educ_proof)

                educ_proof_filename = '{}_{}_{}.{}'.format(
                    'EDUC_PROOF', 
                    current_user.user_id, 
                    date.today(), 
                    educ_proof_ext[1:]
                )

                EDUC_PROOF_PATH = os.path.join(CURR_EDUC_PROOF_DIR, educ_proof_filename)
                educ_proof_img.save(EDUC_PROOF_PATH)

                id = generate_id("ea")
                new_record = EducationalAttainment(
                    id                  = id,
                    user_id             = current_user.user_id,
                    school              = educational_attainment_form['school'],
                    degree              = educational_attainment_form['degree'],
                    specialization      = educational_attainment_form['specialization'],
                    degree_type         = educational_attainment_form['degree_type'],
                    info_status         = False,
                    proof_ext           = educ_proof_ext[1:],
                    start_date          = educational_attainment_form['start_date'],
                    end_date            = educational_attainment_form['end_date'],
                    last_modified       = date.today()
                )
                db.session.add(new_record)
                db.session.commit()
                    # educational_attainment_record = EducationalAttainment.query.filter_by(id=id).first()
                return 'Educational Attainment Record Successfully Added.', 200
        
            else:
                return 'Error! File uploaded must only be of file type jpg or png', 500
    except Exception as e:
        print(e)
        return e, 500


@faculty_blueprint.route('/faculty/delete_educational_attainment/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_educational_attainment(id):    
    educational_delete = EducationalAttainment.query.filter_by(id=id).first()
    try:
        if request.method == 'GET':
            db.session.delete(educational_delete)
            db.session.commit()
            return 'Record successfully deleted.', 200 
        elif request.method == 'POST':
            pass
    except Exception as e:
        print(e)
        return e, 500     

@faculty_blueprint.route('/faculty/update_educational_attainment/<string:id>', methods=['GET', 'POST'])
@login_required
def update_educational_attainment(id):
    try:
        if request.method == 'GET':
            educational_attainment_record = EducationalAttainment.query.filter_by(id=id)
            print(educational_attainment_record.__dict__)
            return render_template('faculty/update_educational.html', educ_record=educational_attainment_record)
        elif request.method == 'POST':
            educational_attainment_form = request.form
            educational_attainment_files = request.files

            CURR_EDUC_PROOF_DIR = os.path.join(EDUC_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_EDUC_PROOF_DIR, exist_ok=True)

            educ_proof = educational_attainment_files['educ_proof']
            _, educ_proof_ext = os.path.splitext(educ_proof.filename)
            educ_proof_img = Image.open(educ_proof)

            educ_proof_filename = '{}_{}_{}.{}'.format(
                'EDUC_PROOF', 
                current_user.user_id, 
                date.today(), 
                educ_proof_ext[1:]
            )

            EDUC_PROOF_PATH = os.path.join(CURR_EDUC_PROOF_DIR, educ_proof_filename)
            educ_proof_img.save(EDUC_PROOF_PATH)

            id = generate_id("ea")
            new_record = EducationalAttainment(
                id                  = id,
                user_id             = current_user.user_id,
                school              = educational_attainment_form['school'],
                degree              = educational_attainment_form['degree'],
                specialization      = educational_attainment_form['specialization'],
                degree_type         = educational_attainment_form['degree_type'],
                info_status         = False,
                proof_ext           = educ_proof_ext[1:],
                start_date          = educational_attainment_form['start_date'],
                end_date            = educational_attainment_form['end_date'],
                last_modified       = date.today()
            )
            db.session.add(new_record)
            db.session.commit()
            return 'Educational Attainment Record Successfully Added.', 200
    except Exception as e:
        print(e)
        return e, 500

@faculty_blueprint.route('/faculty/add_work_experience', methods=['GET', 'POST'])
@login_required
def add_work_experience():
    try:
        if request.method == 'GET':
            #pass
            return render_template('faculty/add_work.html')
        elif request.method == 'POST':
            work_experience_form = request.form
            work_experience_files = request.files

            CURR_WORK_PROOF_DIR = os.path.join(WORK_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_WORK_PROOF_DIR, exist_ok=True)

            work_proof = work_experience_files['work_proof']
            _, work_proof_ext = os.path.splitext(work_proof.filename)

            if (work_proof_ext == '.jpg' or work_proof_ext == '.png'):
                work_proof_img = Image.open(work_proof)

                work_proof_filename = '{}_{}_{}.{}'.format(
                    'WORK_PROOF', 
                    current_user.user_id, 
                    date.today(), 
                    work_proof_ext[1:]
                )

                WORK_PROOF_PATH = os.path.join(CURR_WORK_PROOF_DIR, work_proof_filename)
                work_proof_img.save(WORK_PROOF_PATH)

                id = generate_id("we")
                new_record = WorkExperience(
                    id                  = id,
                    user_id             = current_user.user_id,
                    name_employer       = work_experience_form['name_employer'],
                    location            = work_experience_form['location'],
                    title               = work_experience_form['title'],
                    description         = work_experience_form['description'],
                    info_status         = False,
                    proof_ext           = work_proof_ext[1:],
                    start_date          = work_experience_form['start_date'],
                    end_date            = work_experience_form['end_date'],
                    last_modified       = date.today()
                )
                db.session.add(new_record)
                db.session.commit()
                return 'Work Experience Successfully Added.', 200
            
            else:
                return 'Error! File uploaded must only be of file type jpg or png', 500
    except Exception as e:
        print(e)
        return e, 500

@faculty_blueprint.route('/faculty/delete_work_experience/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_work_experience(id):    
    work_delete = WorkExperience.query.filter_by(id=id).first()
    try:
        if request.method == 'GET':
            db.session.delete(work_delete)
            db.session.commit()
            return 'Record successfully deleted.', 200 
        elif request.method == 'POST':
            pass
    except Exception as e:
        print(e)
        return e, 500     

@faculty_blueprint.route('/faculty/update_work_experience/<string:id>', methods=['GET', 'POST'])
@login_required
def update_work_experience(id):
    try:
        if request.method == 'GET':
            work_experience_record = WorkExperience.query.filter_by(id=id)
            return render_template(
            'faculty/update_work.html',
            work_record=work_experience_record
            )
        elif request.method == 'POST':
            work_experience_form = request.form
            work_experience_files = request.files

            CURR_WORK_PROOF_DIR = os.path.join(WORK_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_WORK_PROOF_DIR, exist_ok=True)

            work_proof = work_experience_files['work_proof']
            _, work_proof_ext = os.path.splitext(work_proof.filename)
            work_proof_img = Image.open(work_proof)

            work_proof_filename = '{}_{}_{}.{}'.format(
                'WORK_PROOF', 
                current_user.user_id, 
                date.today(), 
                work_proof_ext[1:]
            )

            WORK_PROOF_PATH = os.path.join(CURR_WORK_PROOF_DIR, work_proof_filename)
            work_proof_img.save(WORK_PROOF_PATH)

            id = generate_id("we")
            new_record = WorkExperience(
                id                  = id,
                user_id             = current_user.user_id,
                name_employer       = work_experience_form['name_employer'],
                location            = work_experience_form['location'],
                title               = work_experience_form['title'],
                description         = work_experience_form['description'],
                info_status         = False,
                proof_ext           = work_proof_ext[1:],
                start_date          = work_experience_form['start_date'],
                end_date            = work_experience_form['end_date'],
                last_modified       = date.today()
            )
            db.session.add(new_record)
            db.session.commit()

            return 'Work Experience Successfully Added.', 200
    except Exception as e:
        print(e)
        return e, 500


@faculty_blueprint.route('/faculty/add_accomplishment', methods=['GET', 'POST'])
@login_required
def add_accomplishment():
    try:
        if request.method == 'GET':
            #pass
            return render_template('faculty/add_accomplishment.html')
        elif request.method == 'POST':
            accomplishment_form = request.form
            accomplishment_files = request.files

            CURR_ACC_PROOF_DIR = os.path.join(ACC_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_ACC_PROOF_DIR, exist_ok=True)

            acc_proof = accomplishment_files['accomplishment_proof']
            _, acc_proof_ext = os.path.splitext(acc_proof.filename)
            
            if (acc_proof_ext == '.png' or acc_proof_ext == '.jpg'):
                acc_proof_img = Image.open(acc_proof)
                acc_proof_filename = '{}_{}_{}.{}'.format(
                    'ACCOMPLISHMENT_PROOF', 
                    current_user.user_id, 
                    date.today(), 
                    acc_proof_ext[1:]
                )

                ACC_PROOF_PATH = os.path.join(CURR_ACC_PROOF_DIR, acc_proof_filename)
                acc_proof_img.save(ACC_PROOF_PATH)

                id = generate_id("ac")
                new_record = Accomplishment(
                    id                  = id,
                    user_id             = current_user.user_id,
                    position            = accomplishment_form['position'],
                    organization        = accomplishment_form['organization'],
                    type_contribution   = accomplishment_form['type_contribution'],
                    description         = accomplishment_form['description'],
                    info_status         = False,
                    proof_ext           = acc_proof_ext[1:], 
                    start_date          = accomplishment_form['start_date'],
                    end_date            = accomplishment_form['end_date'],
                    last_modified       = date.today()
                )
                db.session.add(new_record)
                db.session.commit()
                return 'Accomplishment Successfully Added.', 200
            
            else:
                 return 'Error! File uploaded must only be of file type jpg or png', 500
    except Exception as e:
        print(e)
        return e, 500


@faculty_blueprint.route('/faculty/delete_accomplishment/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_accomplishment(id):    
    accomplishment_delete = Accomplishment.query.filter_by(id=id).first()
    try:
        if request.method == 'GET':
            db.session.delete(accomplishment_delete)
            db.session.commit()
            return 'Record successfully deleted.', 200 
        elif request.method == 'POST':
            pass
    except Exception as e:
        print(e)
        return e, 500     

@faculty_blueprint.route('/faculty/update_accomplishment/<string:id>', methods=['GET', 'POST'])
@login_required
def update_accomplishment(id):
    try:
        if request.method == 'GET':
            accomplishment_record = db.session.query(Accomplishment).filter_by(id=id)
            print(accomplishment_record)
            return render_template('faculty/update_accomplishment.html', accomplishment_record = accomplishment_record)
        elif request.method == 'POST':
            accomplishment_form = request.form
            accomplishment_files = request.files

            CURR_ACC_PROOF_DIR = os.path.join(ACC_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_ACC_PROOF_DIR, exist_ok=True)

            acc_proof = accomplishment_files['accomplishment_proof']
            _, acc_proof_ext = os.path.splitext(acc_proof.filename)
            acc_proof_img = Image.open(acc_proof)

            acc_proof_filename = '{}_{}_{}.{}'.format(
                'ACCOMPLISHMENT_PROOF', 
                current_user.user_id, 
                date.today(), 
                acc_proof_ext[1:]
            )

            ACC_PROOF_PATH = os.path.join(CURR_ACC_PROOF_DIR, acc_proof_filename)
            acc_proof_img.save(ACC_PROOF_PATH)

            new_record = Accomplishment(
                id                  = id,
                user_id             = current_user.user_id,
                position            = accomplishment_form['position'],
                organization        = accomplishment_form['organization'],
                type_contribution   = accomplishment_form['type_contribution'],
                description         = accomplishment_form['description'],
                info_status         = False,
                proof_ext           = acc_proof_ext[1:], 
                start_date          = accomplishment_form['start_date'],
                end_date            = accomplishment_form['end_date'],
                last_modified       = date.today()
            )
            db.session.add(new_record)
            db.session.commit()
            return 'Accomplishment Successfully Added.', 200

    except Exception as e:
        print(e)
        return e, 500

@faculty_blueprint.route('/faculty/add_publication', methods=['GET', 'POST'])
@login_required
def add_publication():
    try:
        if request.method == 'GET':
            faculty_list = []
            faculty_records = FacultyPersonalInformation.query.all()

            for record in faculty_records:
                if record.middle_name is None:
                    faculty_name = "{} {}".format(record.first_name, record.last_name)
                else:
                    faculty_name = "{} {} {}".format(record.first_name, record.middle_name, record.last_name)
                # info_dict = record.__dict__
                # info_dict['faculty_name'] = faculty_name
                faculty_list.append(faculty_name)

            return render_template('faculty/add_publication.html', faculty_list=faculty_list)
        elif request.method == 'POST':
            publication_form = request.form
            publication_files = request.files

            CURR_PUB_PROOF_DIR = os.path.join(PUB_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_PUB_PROOF_DIR, exist_ok=True)

            pub_proof = publication_files['publication_proof']
            _, pub_proof_ext = os.path.splitext(pub_proof.filename)

            if (pub_proof_ext == '.png' or pub_proof_ext == '.jpg'):
                pub_proof_img = Image.open(pub_proof)

                pub_proof_filename = '{}_{}_{}.{}'.format(
                    'PUBLICATION_PROOF', 
                    current_user.user_id, 
                    date.today(), 
                    pub_proof_ext[1:]
                )

                PUB_PROOF_PATH = os.path.join(CURR_PUB_PROOF_DIR, pub_proof_filename)
                pub_proof_img.save(PUB_PROOF_PATH)

                id = generate_id("pb")
                new_record = Publication(
                    id                  = id,
                    user_id             = current_user.user_id,
                    publication         = publication_form['publication'],
                    citation            = publication_form['citation'],
                    url                 = publication_form['url'],
                    coauthors_dpsm      = publication_form['coauthors_dpsm'],
                    coauthors_nondpsm   = publication_form['coauthors_nondpsm'],
                    date_published      = publication_form['date_published'],
                    info_status         = False,
                    proof_ext           = pub_proof_ext[1:],
                    last_modified       = date.today()
                )
                db.session.add(new_record)
                db.session.commit()
                return 'Publication Successfully Added.', 200
            
            else:
                return 'Error! File uploaded must only be of file type jpg or png', 500
    except Exception as e:
        print(e)
        return e, 500

@faculty_blueprint.route('/faculty/delete_publication/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_publication(id):    
    publication_delete = Publication.query.filter_by(id=id).first()
    try:
        if request.method == 'GET':
            print(publication_delete)
            db.session.delete(publication_delete)
            db.session.commit()
            return render_template('/faculty/faculty_landing_page.html')
        elif request.method == 'POST':
            pass
    except Exception as e:
        print(e)
        return e, 500            

@faculty_blueprint.route('/faculty/update_publication/<string:id>', methods=['GET', 'POST'])
@login_required
def update_publication(id):
    try:
        if request.method == 'GET':
            publication_record = Publication.query.filter_by(id=id)

            faculty_list = []
            faculty_records = FacultyPersonalInformation.query.all()

            for record in faculty_records:
                if record.middle_name is None:
                    faculty_name = "{} {}".format(record.first_name, record.last_name)
                else:
                    faculty_name = "{} {} {}".format(record.first_name, record.middle_name, record.last_name)
                faculty_list.append(faculty_name)

            return render_template(
                'faculty/update_publication.html',
                publication_record = publication_record,
                faculty_list = faculty_list
            )
        elif request.method == 'POST':
            publication_form = request.form
            publication_files = request.files

            CURR_PUB_PROOF_DIR = os.path.join(PUB_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_PUB_PROOF_DIR, exist_ok=True)

            pub_proof = publication_files['publication_proof']
            _, pub_proof_ext = os.path.splitext(pub_proof.filename)
            pub_proof_img = Image.open(pub_proof)

            pub_proof_filename = '{}_{}_{}.{}'.format(
                'PUBLICATION_PROOF', 
                current_user.user_id, 
                date.today(), 
                pub_proof_ext[1:]
            )

            PUB_PROOF_PATH = os.path.join(CURR_PUB_PROOF_DIR, pub_proof_filename)
            pub_proof_img.save(PUB_PROOF_PATH)

            new_record = Publication(
                id                  = id,
                user_id             = current_user.user_id,
                publication         = publication_form['publication'],
                citation            = publication_form['citation'],
                url                 = publication_form['url'],
                coauthors_dpsm      = publication_form['coauthors_dpsm'],
                coauthors_nondpsm   = publication_form['coauthors_nondpsm'],
                date_published      = publication_form['date_published'],
                info_status         = False,
                proof_ext           = pub_proof_ext[1:],
                last_modified       = date.today()
            )
            db.session.add(new_record)
            db.session.commit()
                
            return 'Publication Successfully Added.', 200
    except Exception as e:
        print(e)
        return e, 500


@faculty_blueprint.route('/faculty/add_research_grant', methods=['GET', 'POST'])
@login_required
def add_research_grant():
    try:
        if request.method == 'GET':
            faculty_list = []
            faculty_records = FacultyPersonalInformation.query.all()

            for record in faculty_records:
                if record.middle_name is None:
                    faculty_name = "{} {}".format(record.first_name, record.last_name)
                else:
                    faculty_name = "{} {} {}".format(record.first_name, record.middle_name, record.last_name)
                # info_dict = record.__dict__
                # info_dict['faculty_name'] = faculty_name
                faculty_list.append(faculty_name)

            return render_template('faculty/add_research.html', faculty_list=faculty_list)
        elif request.method == 'POST':
            research_grant_form = request.form
            research_grant_files = request.files

            CURR_RG_PROOF_DIR = os.path.join(RG_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_RG_PROOF_DIR, exist_ok=True)

            rg_proof = research_grant_files['research_proof']
            _, rg_proof_ext = os.path.splitext(rg_proof.filename)

            if (rg_proof_ext == '.png' or rg_proof_ext == '.jpg'):
                rg_proof_img = Image.open(rg_proof)

                rg_proof_filename = '{}_{}_{}.{}'.format(
                    'RESEARCH_GRANT_PROOF', 
                    current_user.user_id, 
                    date.today(), 
                    rg_proof_ext[1:]
                )

                RG_PROOF_PATH = os.path.join(CURR_RG_PROOF_DIR, rg_proof_filename)
                rg_proof_img.save(RG_PROOF_PATH)

                id = generate_id("rg")
                new_record = ResearchGrant(
                    id                  = id,
                    user_id             = current_user.user_id,
                    name_research       = research_grant_form['name_research'],
                    sponsor             = research_grant_form['sponsor'],
                    progress      = research_grant_form['research_progress'],
                    amount_granted      = research_grant_form['amount_granted'],
                    coresearchers_dpsm      = research_grant_form['coresearchers_dpsm'],
                    coresearchers_nondpsm   = research_grant_form['coresearchers_nondpsm'],
                    projected_start     = research_grant_form['projected_start'],
                    projected_end       = research_grant_form['projected_end'],
                    actual_start        = research_grant_form['actual_start'],
                    actual_end          = research_grant_form['actual_end'],
                    info_status         = False,
                    proof_ext           = rg_proof_ext[1:],
                    last_modified       = date.today()
                )
                db.session.add(new_record)
                db.session.commit()
                return 'Research Grant Successfully Added.', 200
            
            else:
                return 'Error! File uploaded must only be of file type jpg or png', 500
    except Exception as e:
        print(e)
        return e, 500


@faculty_blueprint.route('/faculty/delete_research_grant/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_research_grant(id):    
    research_delete = ResearchGrant.query.filter_by(id=id).first()
    try:
        if request.method == 'GET':
            db.session.delete(research_delete)
            db.session.commit()
            return 'Record successfully deleted.', 200 
        elif request.method == 'POST':
            pass
    except Exception as e:
        print(e)
        return e, 500     

@faculty_blueprint.route('/faculty/update_research_grant/<string:id>', methods=['GET', 'POST'])
@login_required
def update_research_grant(id):
    try:
        if request.method == 'GET':
            research_grant_record = ResearchGrant.query.filter_by(id=id)

            faculty_list = []
            faculty_records = FacultyPersonalInformation.query.all()

            for record in faculty_records:
                print(record)
                if record.middle_name is None:
                    faculty_name = "{} {}".format(record.first_name, record.last_name)
                else:
                    faculty_name = "{} {} {}".format(record.first_name, record.middle_name, record.last_name)
                # info_dict = record.__dict__
                # info_dict['faculty_name'] = faculty_name
                faculty_list.append(faculty_name)

            return render_template('faculty/update_research.html', research_record=research_grant_record, faculty_list=faculty_list)

        elif request.method == 'POST':
            research_grant_form = request.form
            research_grant_files = request.files

            CURR_RG_PROOF_DIR = os.path.join(RG_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_RG_PROOF_DIR, exist_ok=True)

            rg_proof = research_grant_files['research_proof']
            _, rg_proof_ext = os.path.splitext(rg_proof.filename)
            rg_proof_img = Image.open(rg_proof)

            rg_proof_filename = '{}_{}_{}.{}'.format(
                'RESEARCH_GRANT_PROOF', 
                current_user.user_id, 
                date.today(), 
                rg_proof_ext[1:]
            )

            RG_PROOF_PATH = os.path.join(CURR_RG_PROOF_DIR, rg_proof_filename)
            rg_proof_img.save(RG_PROOF_PATH)

            new_record = ResearchGrant(
                id                  = id,
                user_id             = current_user.user_id,
                name_research       = research_grant_form['name_research'],
                sponsor             = research_grant_form['sponsor'],
                progress      = research_grant_form['research_progress'],
                amount_granted      = research_grant_form['amount_granted'],
                coresearchers_dpsm      = research_grant_form['coresearchers_dpsm'],
                coresearchers_nondpsm   = research_grant_form['coresearchers_nondpsm'],
                projected_start     = research_grant_form['projected_start'],
                projected_end       = research_grant_form['projected_end'],
                actual_start        = research_grant_form['actual_start'],
                actual_end          = research_grant_form['actual_end'],
                info_status         = False,
                proof_ext           = rg_proof_ext[1:],
                last_modified       = date.today()
            )
            db.session.add(new_record)
            db.session.commit()

            return 'Research Grant Successfully Added.', 200
    except Exception as e:
        print(e)
        return e, 500

@faculty_blueprint.route('/faculty/add_licensure', methods=['GET', 'POST'])
@login_required
def add_licensure():
    try:
        if request.method == 'GET':
            #pass
            return render_template('faculty/add_licensure.html')
        elif request.method == 'POST':
            licensure_form = request.form
            licensure_files = request.files

            CURR_LIC_PROOF_DIR = os.path.join(LIC_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_LIC_PROOF_DIR, exist_ok=True)

            lic_proof = licensure_files['licensure_proof']
            _, lic_proof_ext = os.path.splitext(lic_proof.filename)

            if (lic_proof_ext == '.png' or lic_proof_ext == '.jpg'):
                lic_proof_img = Image.open(lic_proof)

                lic_proof_filename = '{}_{}_{}.{}'.format(
                    'LICENSURE_PROOF', 
                    current_user.user_id, 
                    date.today(), 
                    lic_proof_ext[1:]
                )

                LIC_PROOF_PATH = os.path.join(CURR_LIC_PROOF_DIR, lic_proof_filename)
                lic_proof_img.save(LIC_PROOF_PATH)

                id = generate_id("le")
                new_record = LicensureExams(
                    id                  = id,
                    user_id             = current_user.user_id,
                    name_exam           = licensure_form['name_exam'],
                    rank                = licensure_form['rank'],
                    license_number      = licensure_form['license_number'],
                    date                = licensure_form['date'],
                    info_status         = False,
                    proof_ext           = lic_proof_ext[1:],
                    last_modified       = date.today()
                )
                db.session.add(new_record)
                db.session.commit()
                return 'Licensure Exam Successfully Added.', 200
            
            else:
                return 'Error! File uploaded must only be of file type jpg or png', 500
    except Exception as e:
        print(e)
        return e, 500

@faculty_blueprint.route('/faculty/delete_licensure/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_licensure(id):    
    licensure_delete = LicensureExams.query.filter_by(id=id).first()
    try:
        if request.method == 'GET':
            print("dito")
            print(licensure_delete)
            db.session.delete(licensure_delete)
            db.session.commit()
            return 'Record successfully deleted.', 200 
        elif request.method == 'POST':
            pass
    except Exception as e:
        print(e)
        return e, 500     

@faculty_blueprint.route('/faculty/update_licensure_exam/<string:id>', methods=['GET', 'POST'])
@login_required
def update_licensure_exam(id):
    try:
        if request.method == 'GET':
            licensure_record = db.session.query(LicensureExams).filter_by(id=id).all()
            print(licensure_record)
            return render_template('faculty/update_licensure.html', licensure_record=licensure_record)

        elif request.method == 'POST':
            licensure_form = request.form
            licensure_files = request.files

            CURR_LIC_PROOF_DIR = os.path.join(LIC_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_LIC_PROOF_DIR, exist_ok=True)

            lic_proof = licensure_files['licensure_proof']
            _, lic_proof_ext = os.path.splitext(lic_proof.filename)
            lic_proof_img = Image.open(lic_proof)

            lic_proof_filename = '{}_{}_{}.{}'.format(
                'LICENSURE_PROOF', 
                current_user.user_id, 
                date.today(), 
                lic_proof_ext[1:]
            )

            LIC_PROOF_PATH = os.path.join(CURR_LIC_PROOF_DIR, lic_proof_filename)
            lic_proof_img.save(LIC_PROOF_PATH)

            new_record = LicensureExams(
                id                  = id,
                user_id             = current_user.user_id,
                name_exam           = licensure_form['name_exam'],
                rank                = licensure_form['rank'],
                license_number      = licensure_form['license_number'],
                date                = licensure_form['date'],
                info_status         = False,
                proof_ext           = lic_proof_ext[1:],
                last_modified       = date.today()
            )
            db.session.query(LicensureExams).add(new_record)
            db.session.commit()
            print("added and committed")

            return 'Licensure Exam Successfully Added.', 200
    except Exception as e:
        print(e)
        return e, 500

@faculty_blueprint.route('/faculty/add_training', methods=['GET', 'POST'])
@login_required
def add_training():
    try:
        if request.method == 'GET':
            #pass
            return render_template('faculty/add_training.html')
        elif request.method == 'POST':
            training_form = request.form
            training_files = request.files

            CURR_TS_PROOF_DIR = os.path.join(TS_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_TS_PROOF_DIR, exist_ok=True)

            ts_proof = training_files['training_proof']
            _, ts_proof_ext = os.path.splitext(ts_proof.filename)
            
            if (ts_proof_ext == '.png' or ts_proof_ext == '.jpg'):
                ts_proof_img = Image.open(ts_proof)

                ts_proof_filename = '{}_{}_{}.{}'.format(
                    'TRAINING_SEMINAR_PROOF', 
                    current_user.user_id, 
                    date.today(), 
                    ts_proof_ext[1:]
                )

                TS_PROOF_PATH = os.path.join(CURR_TS_PROOF_DIR, ts_proof_filename)
                ts_proof_img.save(TS_PROOF_PATH)

                id = generate_id("ts")
                new_record = TrainingSeminar(
                    id                  = id,
                    user_id             = current_user.user_id,
                    name_training       = training_form['name_training'],
                    role                = training_form['role'],
                    remarks             = training_form['remarks'],
                    start_date          = training_form['start_date'],
                    end_date            = training_form['end_date'],
                    info_status         = False,
                    proof_ext           = ts_proof_ext[1:],
                    last_modified       = date.today()
                )
                db.session.add(new_record)
                db.session.commit()
                return 'Training/Seminar Successfully Added.', 200
            
            else:
                return 'Error! File uploaded must only be of file type jpg or png', 500
    except Exception as e:
        print(e)
        return e, 500

@faculty_blueprint.route('/faculty/delete_training/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_training(id):    
    training_delete = TrainingSeminar.query.filter_by(id=id).first()
    try:
        if request.method == 'GET':
            db.session.delete(training_delete)
            db.session.commit()
            return 'Record successfully deleted.', 200 
        elif request.method == 'POST':
            pass
    except Exception as e:
        print(e)
        return e, 500     

@faculty_blueprint.route('/faculty/update_training/<string:id>', methods=['GET', 'PUT'])
@login_required
def update_training(id):
    try:
        if request.method == 'GET':
            training_record = db.session.query(TrainingSeminar).filter_by(id=id).all()
            return render_template('faculty/update_training.html', training_record=training_record)

        elif request.method == 'PUT':
            training_form = request.form
            training_files = request.files

            CURR_TS_PROOF_DIR = os.path.join(TS_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_TS_PROOF_DIR, exist_ok=True)

            ts_proof = training_files['training_proof']
            _, ts_proof_ext = os.path.splitext(ts_proof.filename)
            ts_proof_img = Image.open(ts_proof)

            ts_proof_filename = '{}_{}_{}.{}'.format(
                'TRAINING_SEMINAR_PROOF', 
                current_user.user_id, 
                date.today(), 
                ts_proof_ext[1:]
            )

            TS_PROOF_PATH = os.path.join(CURR_TS_PROOF_DIR, ts_proof_filename)
            ts_proof_img.save(TS_PROOF_PATH)

            new_record = TrainingSeminar(
                id                  = id,
                user_id             = current_user.user_id,
                name_training       = training_form['name_training'],
                role                = training_form['role'],
                remarks             = training_form['remarks'],
                start_date          = training_form['start_date'],
                end_date            = training_form['end_date'],
                info_status         = False,
                proof_ext           = ts_proof_ext[1:],
                last_modified       = date.today()
            )
            db.session.add(new_record)
            db.session.commit()
                
            return 'Training/Seminar Successfully Added.', 200
    except Exception as e:
        print(e)
        return e, 500

@faculty_blueprint.route('/faculty/add_fsr_set', methods=['GET', 'POST'])
@login_required
def add_fsr_set():
    try:
        if request.method == 'GET':
            #pass
            return render_template('faculty/add_fsr_set.html')
        elif request.method == 'POST':
            fsr_set_form = request.form
            fsr_set_files = request.files

            CURR_FSRSET_PROOF_DIR = os.path.join(FSRSET_PROOF_DIR, current_user.user_id)

            os.makedirs(CURR_FSRSET_PROOF_DIR, exist_ok=True)

            fsr_set_proof = fsr_set_files['fsr_set_proof']
            _, fsr_set_proof_ext = os.path.splitext(fsr_set_proof.filename)

            if (fsr_set_proof_ext == '.png' or fsr_set_proof_ext == '.jpg'):
                fsr_set_proof_img = Image.open(fsr_set_proof)

                fsr_set_proof_filename = '{}_{}_{}.{}'.format(
                    'FSR_SET_PROOF', 
                    current_user.user_id, 
                    date.today(), 
                    fsr_set_proof_ext[1:]
                )

                FSRSET_PROOF_PATH = os.path.join(CURR_FSRSET_PROOF_DIR, fsr_set_proof_filename)
                fsr_set_proof_img.save(FSRSET_PROOF_PATH)
            
                id = generate_id("fsr")
                new_record = FacultySETRecords(
                    id                  = id,
                    user_id             = current_user.user_id,
                    course_code         = fsr_set_form['course_code'],
                    section             = fsr_set_form['section'],
                    semester            = fsr_set_form['semester'],
                    sy                  = fsr_set_form['sy'],
                    schedule            = fsr_set_form['schedule'],
                    number_students     = fsr_set_form['number_students'],
                    fsr_rating          = fsr_set_form['fsr'],
                    set_rating          = fsr_set_form['set'],
                    last_modified       = date.today()
                )
                db.session.add(new_record)
                db.session.commit()
                return 'FSR and SET Successfully Added.', 200
            
            else:
                return 'Error! File uploaded must only be of file type jpg or png', 500
    except Exception as e:
        print(e)
        return e, 500

@faculty_blueprint.route('/faculty/update_fsr_set/<string:id>', methods=['GET', 'PUT'])
@login_required
def update_fsr_set(id):
    try:
        if request.method == 'GET':
            fsr_set_record = FacultySETRecords.query.filter_by(id=id).first()
            return render_template(
            'update_fsr_set.html',
            fsr_set_record
            )
        elif request.method == 'PUT':
            fsr_set_record = FacultySETRecords.query.filter_by(id=id).first()
            fsr_set_form = request.form

            fsr_set_record.course_code = fsr_set_form['name_exam'],
            fsr_set_record.section = fsr_set_form['section'],
            fsr_set_record.semester = fsr_set_form['semester'],
            fsr_set_record.sy = fsr_set_form['sy'],
            fsr_set_record.numbeer_students = fsr_set_form['number_students'],
            fsr_set_record.fsr_set_file = fsr_set_form['fsr_set_file'].read(),
            fsr_set_record.last_modified = date.today()
            db.session.commit()

            return 'FSR and SET Record Successfully Updated.', 200
    except Exception as e:
        print(e)
        return 'An error has occured.', 500

# @faculty_blueprint.route('/<string:user_type>/view_faculty_info/<string:id>/<string:proof_type>/<string:filename>', methods=['GET'])
# def view_proof(user_type, id, proof_type, filename):
#     try:
#         CURR_FILE_DIR = os.path.join(proof_type, id)
#         print(CURR_FILE_DIR)
#         FILE_PATH = os.path.join(CURR_FILE_DIR, filename)
#         _, proof_f_ext = os.path.splitext(filename)
#         response = json.dumps({
#             'proof_file':str(FILE_PATH),
#             'file_ext':proof_f_ext
# 		})

#         return response, 200
#     except Exception as e:
#         print(e)
#         return 'Error displaying syllabus. Please try again.', 400