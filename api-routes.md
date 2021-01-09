//AUTH ENDPOINTS
POST
/auth/signup/ -> registrar usuarios DONE!

POST
/auth/token/refresh/ -> confirmar registros de usuarios

data{
    TOKEN
}

POST
/auth/recover-password/ -> recuperar contraseñas DONE!

POST
/auth/change-password/{id}/ -> cambiar contraseñas DONE!

POST
/auth/login/ -> inicio de sesion DONE!

POST
/auth/complete-signup/ -> registrar datos del usuario DONE!



//HOSPITAL ENDPOINTS
GET
/hospitals/clinic-histories/ -> obtiene todas las consultas hechas por los doctores

GET
/hospitals/clinic-histories/{id_doctor} -> obtiener consulta mediante id

POST
/hospitals/doctors -> registra doctores

data{
    DOCTOR
}



//PATIENTS ENDPOINTS
POST

GET
/patients/clinic-history/ -> obtiene la historia medica del paciente




//DOCTORS ENDPOINTS
POST
/doctors/clinic-histories/ -> se realiza la consulta medica al paciente

data{
    HISTORY
}

GET
/doctors/clinic-histories/ -> obtiene las historias clinica de los pacientes

GET
/doctors/clinic-histories/{patient_id}/ -> obtiene la historia clinica de un paciente













