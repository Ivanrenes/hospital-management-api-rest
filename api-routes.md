**API DOCUMENTATION**
**TOKEN JWT - HEADER EXAMPLE**
Get when user get login

    x-access-token : TOKEN

POST /auth/signup/ 
Data Example 

    {
		"num_doc" : "01",
		"email" : "test@gmail.com",
		"password": "01",
		"telphone" : "01",
		"rol" : 2
	}
	
POST /auth/confirm-signup/

UUID is your Confirmation Code
Data Example

    {
		"uuid" : "1c8e9ccd-e0f3-4a8e-817d-39fdf03e7854"
	}

POST /auth/recover-password/ 
Data Example

    {
		"email" : "test@tests.com"
	}

POST /auth/change-password/
Data Example

    {
		"new_password" : "123456"
	}


POST /auth/login/
Data Example 

    {
	    "email" : "test@test.com",
	    "password": "123456"
    }


POST /auth/complete-signup/
Data Example 

USER PATIENT

    {
		"name" : "Alberto",
		"address" : "Calle 55H N4-34",
		"birthday" : "21/12/01"
	}

USER HOSPITAL

    {
		"name" : "Alberto",
		"address" : "Calle 55H N4-34",
		"id_medicalservice" : "0"
	}

GET /hospitals/medical-histories/

    NOT DATA

GET /hospitals/medical-histories/< id_doctor >/

    NOT DATA
POST /hospitals/doctors/
Data Example 


    {
		"num_doc" : "02",
		"email":"doctor@doctor.io",
		"password":"123456",
		"telphone" : "30052525252",
		"name" : "Juan Perez",
		"address" : "Cra 45 #100-14",
		"id_medicalservice" : "0",
		"birthdate" : "12/06/00"
	}

GET /patients/medical-history/

    NOT DATA

POST /doctors/medical-histories/

    {
		"id_patient" : "1",
		"id_patientstatus" : "1",
		"id_specialty" : "1",
		"observation" : "El paciente se encuentra estable"
	}

GET /doctors/medical-histories/ 

    NOT DATA

GET /doctors/medical-histories/< id_patient >

    NOT DATA












