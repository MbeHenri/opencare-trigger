from threading import Thread
from triggers.patient import main as trigger_patient
from triggers.service import main as trigger_service
from triggers.room import main as trigger_room

# from triggers.doctor import main as trigger_doctor

threads = [
    # trigger des patients
    Thread(target=trigger_patient),
    # trigger des services
    Thread(target=trigger_service),
    # trigger des docteurs (providers)
    # Thread(target=trigger_doctor),
    # trigger pour les rooms
    Thread(target=trigger_room),
]

# Lancement des jobs
for tread in threads:
    tread.start()

# Attendes d'arrets des jobs
for tread in threads:
    tread.join()
