def build_room_name(doctor_name, patient_name):
    return f"OpenTMSRoom{doctor_name.replace(' ', '')}{patient_name.replace(' ', '')}"
