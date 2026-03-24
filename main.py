import asyncio
from agents import create_medical_team
from patient_cases import PATIENT_CASES


async def run_medical_consultation(patient_query: str):
    print("\n" + "=" * 60)
    print("   AI MEDICAL ADVISORY SYSTEM")
    print("=" * 60)

    team = create_medical_team()

    async for message in team.run_stream(task=patient_query):
        if hasattr(message, "source") and hasattr(message, "content"):
            print(f"\n[{message.source}]\n{message.content}\n")
            print("-" * 60)


def main():
    print("Available Patient Cases:")
    for key, case in PATIENT_CASES.items():
        print(f"  [{key}] {case['description']}")

    print("\n  [custom] Enter your own patient case")
    choice = input("\nSelect a case: ").strip().lower()

    if choice in PATIENT_CASES:
        query = PATIENT_CASES[choice]["query"]
    elif choice == "custom":
        print("\nEnter patient details (press Enter twice when done):")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        query = "\n".join(lines)
    else:
        print("Invalid choice. Running case_1 as default.")
        query = PATIENT_CASES["case_1"]["query"]

    asyncio.run(run_medical_consultation(query))


if __name__ == "__main__":
    main()
