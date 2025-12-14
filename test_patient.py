import sys
import json
from pprint import pprint

from services.patient_service import (
    get_all_patients,
    get_patient_by_id,
    create_patient,
    update_patient,
    delete_patient,
)

# 테스트용 patient_id
PATIENT_ID = 1

# PatientCreate payload
PATIENT_PAYLOAD = {
    "first_name": "John",
    "last_name": "Doe",
    "gender": "male",
    "email": "john.doe@example.com",
    "phone_number": "+1-555-123-4567",
    "address": "123 Main St, New York, NY 10001",
    "emergency_contact": "Jane Doe (Spouse)",
    "condition": "High fever for 2 days",
}


def usage():
    print(
        """
Usage:
  python test_patient.py <command>

Commands:
  1  GET  /patients
  2  POST /patients
  3  GET  /patients/{id}
  4  PUT  /patients/{id}
  5  DELETE /patients/{id}
"""
    )


def test_get_all():
    print("==> GET /patients")
    result = get_all_patients()
    pprint(result)


def test_post():
    print("==> POST /patients")
    result = create_patient(PATIENT_PAYLOAD)
    pprint(result)


def test_get_by_id():
    print(f"==> GET /patients/{PATIENT_ID}")
    result = get_patient_by_id(PATIENT_ID)
    pprint(result)


def test_put():
    print(f"==> PUT /patients/{PATIENT_ID}")
    updated_payload = PATIENT_PAYLOAD | {
        "condition": "Recovered, discharged"
    }
    result = update_patient(PATIENT_ID, updated_payload)
    pprint(result)


def test_delete():
    print(f"==> DELETE /patients/{PATIENT_ID}")
    result = delete_patient(PATIENT_ID)
    pprint(result)


def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    command = sys.argv[1]

    if command == "1":
        test_get_all()
    elif command == "2":
        test_post()
    elif command == "3":
        test_get_by_id()
    elif command == "4":
        test_put()
    elif command == "5":
        test_delete()
    else:
        usage()


if __name__ == "__main__":
    main()
