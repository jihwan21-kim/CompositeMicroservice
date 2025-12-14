import sys
from pprint import pprint
import time

from services.summarization_service import (
    get_summarization,
    create_summarization,
    update_summarization,
    delete_summarization,
    create_async_summarization,
    get_job_status,
)

SUMMARIZATION_ID = 1
INPUT_TEXT = "This is a very long medical transcription that needs summarization."
SUMMARY = "This is"


def usage():
    print("""
Usage:
  python test_summarization.py <command>

Commands:
  1  GET    /summarizations/{id}
  2  POST   /summarizations
  3  PUT    /summarizations/{id}
  4  DELETE /summarizations/{id}
  5  POST   /summarizations/async
  6  GET    /jobs/{job_id}
""")


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "1":
        pprint(get_summarization(SUMMARIZATION_ID))

    elif cmd == "2":
        pprint(create_summarization("0257ba86-e027-4edd-b6b1-7f9e026838db", INPUT_TEXT, SUMMARY))

    elif cmd == "3":
        pprint(update_summarization(SUMMARIZATION_ID, "UPDATED SUMMARY"))

    elif cmd == "4":
        pprint(delete_summarization(SUMMARIZATION_ID))

    elif cmd == "5":
        result = create_async_summarization(INPUT_TEXT)
        pprint(result)

        if "data" in result:
            job_id = result["data"]["job_id"]
            print(f"\nPolling job {job_id}...\n")

            while True:
                status = get_job_status(job_id)
                pprint(status)

                if status.get("data", {}).get("status") in ("completed", "failed"):
                    break

                time.sleep(3)

    elif cmd == "6":
        if len(sys.argv) != 3:
            print("Usage: python test_summarization.py 6 <job_id>")
            sys.exit(1)
        pprint(get_job_status(sys.argv[2]))

    else:
        usage()


if __name__ == "__main__":
    main()
