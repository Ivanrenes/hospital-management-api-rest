from app import app, jsonify, request, db,  ma, uuid, make_response, mail
from flask_mail import Mail, Message
from app.models import User, user_schema, users_schema
from app.models import Patient, patient_schema, patients_schema
from app.models import Hospital, hospital_schema, hospitals_schema
from app.models import MedicalHistory, medical_history, medical_histories
from app.models import Doctor, doctor_schema, doctors_schema
from  werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass
#  Here we have PyJWT Authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps


random_uuid = uuid.uuid4()

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            current_user =User.query\
                .filter_by(uuid = data['public_id'])\
                .first()
            print(current_user)
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)

    return decorated


""" INDEX """
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message from 1v4nC0d3" : "Welcome to my API!",
        "routes":"/",
        "methods":"POST, PUT, DELETE, GET",
        "data-typ":"JSON"
    })

""" AUTH MODULE """
@app.route('/auth/signup', methods=['POST'])
def signup():

    auth = request.json
    num_doc = auth['num_doc']
    email = auth['email']
    password = auth['password']
    telphone = auth['telphone']
    uuid = random_uuid
    account_verified = 0
    rol = auth['rol']


    if not num_doc or not email or not password or not telphone or not rol:
        return jsonify({"message" : "User information incomplete"}), 422

    if rol > 2 or rol <= 0:
        return jsonify({"message" : "Just 2 types of users allowed by this sign up",
                        "types" : "USER, 1 for PATIENT, 2 for HOSPITAL"}), 422

    #CHECKING FOR EXISTING USER
    user =  user = User.query\
            .filter_by(num_doc = auth['num_doc'])\
            .first()

    if not user:
        new_user = User(
            num_doc,
            email,
            telphone,
            generate_password_hash(password, method='sha256'),
            uuid, account_verified,
            rol)
        # GO INSERT USER
        db.session.add(new_user)
        db.session.commit()

        confirmation_code_msg = Message('Codigo de confirmación [SISGESMEDHIS]', sender = 'gestionmedcentesting@gmail.com', recipients = [email])
        confirmation_code_msg.body = "Codigo de confirmación de tu cuenta : " + str(uuid)
        mail.send(confirmation_code_msg)
        return jsonify({'message' : 'Successfully registered',
                        'important' : 'Confirmation code was sent to your email'}), 201
    else:
        return make_response('User already exists. Please Log in.', 409)

@app.route('/auth/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.json

    if not auth or not auth['email'] or not auth['password']:
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required"'}
        )

    user = User.query\
        .filter_by(email = auth['email'])\
        .first()

    #CODE FOR CONFIRM USER VERIFIED
    #if user.account_verified == 0:
        #return jsonify({"message":"You have to confirm your account"})

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist"'},
        )

    if check_password_hash(user.password, auth['password']):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.uuid,
            'exp' : datetime.utcnow() + timedelta(minutes = 120)
        }, app.config['SECRET_KEY'])
        return make_response(jsonify({'token' : token}), 200)

    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )


@app.route('/auth/recover-password', methods=['POST'])
def recoverPassword():

    auth = request.json
    email = auth['email']
    user = User.query\
    .filter_by(email = email)\
    .first()

    if not email:
        return jsonify({"message" : "Email information incomplete"}), 422
    if user:
        return jsonify({"message" : "Password sent to the email"}), 200
    else:
        return jsonify({"message" : "Not user found"}), 404


@app.route('/auth/change-password', methods=['PUT'])
@token_required
def changePassword(current_user):

    auth = request.json
    new_password = auth['new_password']

    if new_password:
        current_user.password = generate_password_hash(new_password, method='sha256')
        if current_user.rol == 3:
            doctor = Doctor.query\
                .filter_by(id_user = current_user.id)\
                .first()
            doctor.password_changed = 1
            db.session.commit()
            return jsonify({"message" : "Doctor password changed succesfully"}), 200

        db.session.commit()
        return jsonify({"message" : "Password changed succesfully"}), 200
    else:
        return jsonify({"message" : "Please send the new password"}), 422


@app.route('/auth/confirm-signup', methods=['POST'])
@token_required
def confirmSignup(current_user):
    auth = request.json
    confirm_code = current_user.uuid

    if confirm_code == auth['uuid']:
        current_user.account_verified = 1
        db.session.commit()
        return jsonify({"message" : "Your account was verified succesfully"}), 200
    else:
        return jsonify({"message" : "Confirm code wrong!"}), 422



@app.route('/auth/complete-signup', methods=['POST'])
@token_required
def completeSignUp(current_user):
    if current_user.account_verified == 0:
        return make_response('Forbidden: First confirm your account', 403)

    auth = request.json


    patient = Patient.query\
                    .filter_by(id_user = current_user.id)\
                    .first()

    hospital = Hospital.query\
                    .filter_by(id_user = current_user.id)\
                    .first()

    if patient or hospital or current_user.rol == 3:
        return jsonify({"message" : "Sign up have been completed yet"}), 409
    #PATIENT
    if current_user.rol == 1:
        name = auth['name']
        address = auth['address']
        birthdate = datetime.strptime(auth['birthdate'], '%d/%m/%y')
        id_user = current_user.id

        complete_signup = Patient(name, address, birthdate, id_user)

        if not name or not address or not birthdate:
            return make_response('Patient information incomplete', 400)
        else:
            db.session.add(complete_signup)
            db.session.commit()
            return jsonify({'message' : 'Sign Up Completed Successfully'}), 200


    #HOSPITAL
    if current_user.rol == 2:
        name = auth['name']
        address = auth['address']
        id_medicalservice = auth['id_medicalservice']
        id_user = current_user.id

        complete_signup = Hospital(name, address, id_medicalservice, id_user)


        if not name or not address or not id_medicalservice:
            return make_response('Hospital information incomplete', 422)
        else:
            db.session.add(complete_signup)
            db.session.commit()
            return jsonify({'message' : 'Sign Up Completed Successfully'}), 200



""" HOSPITALS MODULE """
@app.route('/hospitals/medical-histories', methods=['GET'])
@token_required
def getMedicalHistoriesByDoctors(current_user):
    if current_user.account_verified == 0:
        return make_response('Forbidden: First confirm your account', 403)

    if current_user.rol != 2:
        return  make_response('Forbidden: Access is denied', 403)


    result = medical_histories.dump(MedicalHistory.query\
                                        .all())
    if result:
        return jsonify({"All medical histories" : result })
    else:
        return jsonify({"message" : "Not medical histories found"})


@app.route('/hospitals/medical-histories/<id_doctor>', methods=['GET'])
@token_required
def getMedicalHistoriesByDoctorID(current_user, id_doctor):
    if current_user.account_verified == 0:
        return make_response('Forbidden: First confirm your account', 403)

    if current_user.rol != 2:
        return  make_response('Forbidden: Access is denied', 403)

    result = medical_histories.dump(MedicalHistory.query\
                                        .filter_by(id_doctor = id_doctor.id)
                                        .all())
    if result:
        return jsonify({"All medical histories" : result })
    else:
        return jsonify({"message" : "Not medical histories found"})

@app.route('/hospitals/doctors', methods=['POST'])
@token_required
def signUpDoctor(current_user):
    if current_user.account_verified == 0:
        return make_response('Forbidden: First confirm your account', 403)

    if current_user.rol != 2:
        return make_response('Forbidden: Access is denied', 403)

    hospital = Hospital.query\
                    .filter_by(id_user = current_user.id)\
                    .first()

    data = request.json
    #USER TABLE INFORMATION TO INSERT
    num_doc = data['num_doc']
    email = data['email']
    password = data['password']
    telphone = data['telphone']
    uuid = random_uuid
    account_verified = 1
    rol = 3

    new_user = User(
        num_doc,
        email,
        telphone,
        generate_password_hash(password, method='sha256'),
        uuid, account_verified,
        rol)
    # GO INSERT USER
    db.session.add(new_user)
    db.session.commit()

    hospital = Hospital.query\
                .filter_by(id_user = current_user.id)\
                .first()
    print(hospital)
    #FIND NEW USER
    user = User.query\
                .filter_by(num_doc = num_doc)\
                .first()

    #DOCTOR TABLE INFORMATION TO INSERT
    name = data['name']
    address = data['address']
    password_changed = 0
    id_medicalservice = data['id_medicalservice']
    birthdate = datetime.strptime(data['birthdate'], '%d/%m/%y')
    id_user = user.id
    id_hospital = hospital.id

    if not data or not name or not address or not id_medicalservice or not birthdate:
        return make_response('Doctor information incomplete', 422)


    new_doctor = Doctor(name, address, birthdate, password_changed, id_medicalservice, id_user, id_hospital)
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({'message' : 'Doctor successfully registered',
                    'important' : 'Confirmation code was sent to Doctor email',
                    'confirmation_code' : uuid}), 201





""" PATIENTS MODULE """
@app.route('/patients/medical-history', methods=['GET'])
@token_required
def getMedicalHistory(current_user):
    if current_user.account_verified == 0:
        return make_response('Forbidden: First confirm your account', 403)

    if current_user.rol != 1:
        return  make_response('Forbidden: Access is denied', 403)

    patient = Patient.query\
                    .filter_by(id_user = current_user.id)\
                    .first()

    result = medical_histories.dump(MedicalHistory.query\
                                        .filter_by(id_patient = patient.id)\
                                        .all())

    if result:
        return jsonify({"All medical histories" : result })
    else:
        return jsonify({"message" : "Not medical histories found"})

""" DOCTORS MODULE """

@app.route('/doctors/medical-histories', methods=['POST'])
@token_required
def addMedicalHistory(current_user):
    if current_user.rol != 3:
        return  make_response('Forbidden: Access is denied', 403)

    doctor = Doctor.query\
        .filter_by(id_user = current_user.id)\
        .first()

    if doctor.password_changed == 0:
        return  make_response('Forbidden: Change your password for get access', 403)

    data = request.json
    id_patient = data['id_patient']
    id_doctor = doctor.id
    id_patientstatus = data['id_patientstatus']
    id_specialty = data['id_specialty']
    observation = data['observation']

    if not data or not id_patientstatus or not id_specialty or not observation:
        return make_response('Medical History information incomplete', 422)

    new_medicalhistory = MedicalHistory(id_patient, id_doctor, id_patientstatus, id_specialty, observation)
    db.session.add(new_medicalhistory)
    db.session.commit()

    return jsonify({"message" : "Medical History registered succesfully"}), 201


@app.route('/doctors/medical-histories', methods=['GET'])
@token_required
def getMedicalHistories(current_user):
    if current_user.rol != 3:
        return  make_response('Forbidden: Access is denied', 403)

    doctor = Doctor.query\
                .filter_by(id_user = current_user.id)\
                .first()

    if doctor.password_changed == 0:
        return  make_response('Forbidden: Change your password for get access', 403)

    result = medical_histories.dump(MedicalHistory.query\
                                        .filter_by(id_doctor = doctor.id)
                                        .all())
    if result:
        return jsonify({"All medical histories" : result })
    else:
        return jsonify({"message" : "Not medical histories found"})


@app.route('/doctors/medical-histories/<id_patient>', methods=['GET'])
@token_required
def getMedicalHistoryByPatientID(current_user, id_patient):
    if current_user.rol != 3:
            return  make_response('Forbidden: Access is denied', 403)

    doctor = Doctor.query\
        .filter_by(id_user = current_user.id)\
        .first()

    if doctor.password_changed == 0:
        return  make_response('Forbidden: Change your password for get access', 403)

    result = medical_histories.dump(MedicalHistory.query\
                                            .filter_by(id_doctor = doctor.id)\
                                            .filter_by(id_patient = id_patient)
                                            .all())
    if result:
        return jsonify({"All medical histories" : result }), 200
    else:
        return jsonify({"message" : "Not medical histories found"}), 404




