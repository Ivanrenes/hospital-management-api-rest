from app import db, ma, migrate


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    num_doc = db.Column(db.BigInteger, unique=True)
    email = db.Column(db.String(40), unique=True)
    telphone = db.Column(db.BigInteger)
    password = db.Column(db.String(100))
    uuid = db.Column(db.String(80))
    account_verified = db.Column(db.Integer)
    rol = db.Column(db.Integer)

    def __init__(self, num_doc, email, telphone, password, uuid, account_verified, rol):
        self.num_doc = num_doc,
        self.email = email,
        self.telphone = telphone,
        self.password = password,
        self.uuid = uuid,
        self.account_verified = account_verified
        self.rol = rol

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'num_doc', 'email', 'telphone', 'password', 'uuid' , 'account_verified', 'rol')

user_schema = UserSchema()
users_schema = UserSchema(many=True)



class Patient(db.Model):
    __tablename__ = 'Patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    address = db.Column(db.String(60))
    birthdate = db.Column(db.Date())
    id_user = db.Column(db.Integer)


    def __init__(self, name, address, birthdate, id_user):
        self.name = name
        self.address = address
        self.birthdate = birthdate
        self.id_user  = id_user

class PatientSchema(ma.Schema):
    class Meta:
        fields = ('id','name','address','birthdate','id_user')

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)



class Hospital(db.Model):
    __tablename__ = 'Hospitals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    address = db.Column(db.String(70))
    id_medicalservice = db.Column(db.Integer)
    id_user = db.Column(db.Integer)


    def __init__(self, name, address, id_medicalservice, id_user):
        self.name = name
        self.address = address
        self.id_medicalservice = id_medicalservice
        self.id_user  = id_user

class HospitalSchema(ma.Schema):
    class Meta:
        fields = ('id','name','address','id_medicalservice','id_user')

hospital_schema = HospitalSchema()
hospitals_schema = HospitalSchema(many=True)




class Doctor(db.Model):
    __tablename__ = 'Doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    address = db.Column(db.String(70))
    birthdate = db.Column(db.Date())
    password_changed = db.Column(db.Integer)
    id_medicalservice = db.Column(db.Integer)
    id_user = db.Column(db.Integer)
    id_hospital = db.Column(db.Integer)


    def __init__(self, name, address, birthdate,password_changed, id_medicalservice, id_user, id_hospital):
        self.name = name
        self.address = address
        self.birthdate = birthdate
        self.password_changed = password_changed
        self.id_medicalservice = id_medicalservice
        self.id_user  = id_user
        self.id_hospital = id_hospital

class DoctorSchema(ma.Schema):
    class Meta:
        fields = ('id','name','address','birthdate','id_medicalservice','id_user', 'id_hospital')

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)

class HospitalDoctor(db.Model):
    __tablename__ = 'HospitalsDoctors'
    id = db.Column(db.Integer, primary_key=True)
    id_hospital = db.Column(db.Integer)
    id_doctor = db.Column(db.Integer)


    def __init__(self, id_doctor, id_hospital):
        self.id = id
        self.id_doctor = id_doctor
        self.id_hospital = id_hospital


class HospitalDoctorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_doctor', 'id_hospital')

hospital_doctor = HospitalDoctorSchema()
hospitals_doctors = HospitalDoctorSchema(many=True)


class MedicalService(db.Model):
    __tablename__ = 'MedicalServices'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(60))

    def __init__(self, description):
        self.description = description


class MedicalServiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description')

medical_service = MedicalServiceSchema()
medical_services = MedicalServiceSchema(many=True)


class PatientStatus(db.Model):
    __tablename__ = 'PatientStatuses'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(60))

    def __init__(self, description):
        self.description = description


class PatientStatusSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description')

patient_service = PatientStatusSchema()
patient_services = PatientStatusSchema(many=True)


class MedicalSpeciality(db.Model):
    __tablename__ = 'MedicalSpecialities'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(60))

    def __init__(self, description):
        self.description = description


class MedicalSpecialitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'description')

medical_speciality = PatientStatusSchema()
medical_specialities = PatientStatusSchema(many=True)



class MedicalHistory(db.Model):
    __tablename__ = 'MedicalHistories'
    id = db.Column(db.Integer, primary_key=True)
    id_patient = db.Column(db.Integer)
    id_doctor = db.Column(db.Integer)
    id_patientstatus = db.Column(db.Integer)
    id_specialty = db.Column(db.Integer)
    observation = db.Column(db.String(244))

    def __init__(self, id_patient, id_doctor, id_patientstatus, id_specialty, observation):
        self.id_patient = id_patient
        self.id_doctor = id_doctor
        self.id_patientstatus = id_patientstatus
        self.id_specialty = id_specialty
        self.observation = observation

class MedicalHistorySchema(ma.Schema):
    class Meta:
        fields = ('id','id_patient','id_doctor','id_patientstatus','id_specialty','observation')

medical_history = MedicalHistorySchema()
medical_histories = MedicalHistorySchema(many=True)



db.create_all()




