import sys
from uuid import UUID
from pprint import pprint

from services.transcription_service import (
    get_all_transcriptions,
    get_transcription,
    create_transcription,
    update_transcription,
    delete_transcription,
)

# 테스트용 (실제 존재하는 UUID로 바꿔도 됨)
TRANSCRIPTION_ID = "0257ba86-e027-4edd-b6b1-7f9e026838db"
AUDIO_FILE = "sample.wav"


def usage():
    print("""
Usage:
  python test_transcription.py <command>

Commands:
  1  GET    /transcriptions
  2  POST   /transcriptions   (upload audio)
  3  GET    /transcriptions/{id}
  4  PUT    /transcriptions/{id}
  5  DELETE /transcriptions/{id}
""")


def main():
    global TRANSCRIPTION_ID

    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "1":
        pprint(get_all_transcriptions())

    elif cmd == "2":
        result = create_transcription(AUDIO_FILE)
        pprint(result)

        if result.get("status") == "success":
            TRANSCRIPTION_ID = result["data"]["id"]
            print(f"\nSaved TRANSCRIPTION_ID = {TRANSCRIPTION_ID}")

    elif cmd == "3":
        if not TRANSCRIPTION_ID:
            print("TRANSCRIPTION_ID not set. Run command 2 first.")
            return
        pprint(get_transcription(UUID(TRANSCRIPTION_ID)))

    elif cmd == "4":
        if not TRANSCRIPTION_ID:
            print("TRANSCRIPTION_ID not set. Run command 2 first.")
            return
        pprint(
            update_transcription(
                UUID(TRANSCRIPTION_ID),
                {"status": "reviewed", "text": "Edited transcription"}
            )
        )

    elif cmd == "5":
        if not TRANSCRIPTION_ID:
            print("TRANSCRIPTION_ID not set. Run command 2 first.")
            return
        pprint(delete_transcription(UUID(TRANSCRIPTION_ID)))

    else:
        usage()


if __name__ == "__main__":
    main()
