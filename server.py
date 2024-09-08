from triggers.patient import main as trigger_patient
from triggers.service import main as trigger_service
from triggers.doctor import main as trigger_doctor
from threading import Thread

threads = [
    # trigger des patients
    Thread(target=trigger_patient),
    # trigger des services
    Thread(target=trigger_service),
    # trigger des docteurs (providers)
    Thread(target=trigger_doctor),
]

# Lancement des jobs
for tread in threads:
    tread.start()

# Attendes d'arrets des jobs
for tread in threads:
    tread.join()
