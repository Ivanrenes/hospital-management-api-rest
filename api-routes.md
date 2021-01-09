//AUTH ENDPOINTS
POST
/auth/signup/ -> registrar usuarios

POST
/auth/token/refresh/ -> confirmar registros de usuarios


POST
/auth/recover-password/ -> recuperar contraseñas

POST
/auth/change-password/{id}/ -> cambiar contraseñas

POST
/auth/login/ -> inicio de sesion

POST
/auth/complete-signup/ -> registrar datos del usuario


//HOSPITAL ENDPOINTS
GET
/hospitals/clinic-histories/ -> obtiene todas las consultas hechas por los doctores

GET
/hospitals/clinic-histories/{id_doctor} -> obtiener consulta mediante id

POST
/hospitals/doctors -> registra doctores




//PATIENTS ENDPOINTS
POST

GET
/patients/clinic-history/ -> obtiene la historia medica del paciente




//DOCTORS ENDPOINTS
POST
/doctors/clinic-histories/ -> se realiza la consulta medica al paciente

GET
/doctors/clinic-histories/ -> obtiene las historias clinica de los pacientes

GET
/doctors/clinic-histories/{patient_id}/ -> obtiene la historia clinica de un paciente













