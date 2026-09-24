import hashlib
import json
import os


BASELINE_FILE = "baseline.json"
MONITOR_FOLDER = "test_files"


def show_banner():
    print("""
╔════════════════════════════════════════╗
║        🔐 FILE INTEGRITY MONITOR       ║
║          SHA-256 Security Tool         ║
╚════════════════════════════════════════╝
""")


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def create_baseline():
    baseline = {}

    if not os.path.exists(MONITOR_FOLDER):
        print("\n❌ Monitoring folder not found!")
        return

    for file_name in os.listdir(MONITOR_FOLDER):
        file_path = os.path.join(MONITOR_FOLDER, file_name)

        if os.path.isfile(file_path):
            baseline[file_name] = calculate_hash(file_path)

    with open(BASELINE_FILE, "w", encoding="utf-8") as file:
        json.dump(baseline, file, indent=4)

    print("\n✅ Baseline created successfully!")
    print(f"Files monitored: {len(baseline)}")


def check_integrity():
    if not os.path.exists(BASELINE_FILE):
        print("\n❌ No baseline found.")
        print("Please create a baseline first.")
        return

    with open(BASELINE_FILE, "r", encoding="utf-8") as file:
        baseline = json.load(file)

    if not os.path.exists(MONITOR_FOLDER):
        print("\n❌ Monitoring folder not found!")
        return

    print("\n🔍 Checking file integrity...\n")

    current_files = set()

    safe_count = 0
    modified_count = 0
    deleted_count = 0
    new_count = 0

    # Get current files
    for file_name in os.listdir(MONITOR_FOLDER):
        file_path = os.path.join(MONITOR_FOLDER, file_name)

        if os.path.isfile(file_path):
            current_files.add(file_name)

    # Check files from the original baseline
    for file_name, original_hash in baseline.items():

        file_path = os.path.join(MONITOR_FOLDER, file_name)

        # File deleted
        if not os.path.exists(file_path):
            print(f"❌ {file_name} - FILE DELETED")
            deleted_count += 1
            continue

        # Calculate current hash
        current_hash = calculate_hash(file_path)

        # Compare hashes
        if current_hash == original_hash:
            print(f"✅ {file_name} - No changes")
            safe_count += 1
        else:
            print(f"⚠️ {file_name} - MODIFIED")
            modified_count += 1

    # Detect newly added files
    for file_name in current_files:

        if file_name not in baseline:
            print(f"🆕 {file_name} - NEW FILE DETECTED")
            new_count += 1

    # Security summary
    print("\n╔════════════════════════════════════════╗")
    print("║           SECURITY SUMMARY             ║")
    print("╚════════════════════════════════════════╝")

    print(f"\nFiles checked : {len(baseline)}")
    print(f"Safe          : {safe_count}")
    print(f"Modified      : {modified_count}")
    print(f"Deleted       : {deleted_count}")
    print(f"New files     : {new_count}")

    if modified_count > 0 or deleted_count > 0 or new_count > 0:
        print("\n⚠️ SECURITY ALERT: Changes detected!")
    else:
        print("\n✅ SYSTEM SECURE: No changes detected!")


def main():
    while True:

        show_banner()

        print("1. Create baseline")
        print("2. Check integrity")
        print("3. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            create_baseline()

        elif choice == "2":
            check_integrity()

        elif choice == "3":
            print("\n👋 Goodbye!")
            break

        else:
            print("\n❌ Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
