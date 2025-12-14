import sys
from pprint import pprint

from services.patient_service import (
    get_all_patients,
    get_patient_by_id,
    create_patient,
    update_patient,
    delete_patient,
)

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
  python test_patient.py <command> [patient_id]

Commands:
  1  GET  /patients
  2  POST /patients
  3  GET  /patients/{id}        (requires patient_id: str)
  4  PUT  /patients/{id}        (requires patient_id: str)
  5  DELETE /patients/{id}      (requires patient_id: str)

Examples:
  python test_patient.py 1
  python test_patient.py 2
  python test_patient.py 3 abc123
  python test_patient.py 4 abc123
  python test_patient.py 5 abc123
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


def test_get_by_id(patient_id: str):
    print(f"==> GET /patients/{patient_id}")
    result = get_patient_by_id(patient_id)
    pprint(result)


def test_put(patient_id: str):
    print(f"==> PUT /patients/{patient_id}")
    updated_payload = PATIENT_PAYLOAD | {
        "condition": "Recovered, discharged"
    }
    result = update_patient(patient_id, updated_payload)
    pprint(result)


def test_delete(patient_id: str):
    print(f"==> DELETE /patients/{patient_id}")
    result = delete_patient(patient_id)
    pprint(result)


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    command = sys.argv[1]

    # Commands without patient_id
    if command == "1":
        test_get_all()
        return

    if command == "2":
        test_post()
        return

    # Commands that require patient_id (string)
    if len(sys.argv) < 3:
        print("❌ patient_id (string) is required for this command")
        usage()
        sys.exit(1)

    patient_id = sys.argv[2]  # <-- keep as string

    if command == "3":
        test_get_by_id(patient_id)
    elif command == "4":
        test_put(patient_id)
    elif command == "5":
        test_delete(patient_id)
    else:
        usage()


if __name__ == "__main__":
    main()
