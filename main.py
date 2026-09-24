import hashlib
import json
import os


BASELINE_FILE = "baseline.json"
MONITOR_FOLDER = "test_files"

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def show_banner():
    print(f"""
{CYAN}╔════════════════════════════════════════╗
║        🔐 FILE INTEGRITY MONITOR       ║
║          SHA-256 Security Tool         ║
╚════════════════════════════════════════╝{RESET}
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
        print(f"\n{RED}❌ Monitoring folder not found!{RESET}")
        return

    for file_name in os.listdir(MONITOR_FOLDER):
        file_path = os.path.join(MONITOR_FOLDER, file_name)

        if os.path.isfile(file_path):
            baseline[file_name] = calculate_hash(file_path)

    with open(BASELINE_FILE, "w", encoding="utf-8") as file:
        json.dump(baseline, file, indent=4)

    print(f"\n{GREEN}✅ Baseline created successfully!{RESET}")
    print(f"Files monitored: {len(baseline)}")


def check_integrity():
    if not os.path.exists(BASELINE_FILE):
        print(f"\n{RED}❌ No baseline found.{RESET}")
        print("Please create a baseline first.")
        return

    with open(BASELINE_FILE, "r", encoding="utf-8") as file:
        baseline = json.load(file)

    if not os.path.exists(MONITOR_FOLDER):
        print(f"\n{RED}❌ Monitoring folder not found!{RESET}")
        return

    print(f"\n{CYAN}🔍 Checking file integrity...{RESET}\n")

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
            print(f"{RED}❌ {file_name} - FILE DELETED{RESET}")
            deleted_count += 1
            continue

        # Calculate current hash
        current_hash = calculate_hash(file_path)

        # Compare hashes
        if current_hash == original_hash:
            print(f"{GREEN}✅ {file_name} - No changes{RESET}")
            safe_count += 1
        else:
            print(f"{YELLOW}⚠️ {file_name} - MODIFIED{RESET}")
            modified_count += 1

    # Detect newly added files
    for file_name in current_files:

        if file_name not in baseline:
            print(f"{RED}🆕 {file_name} - NEW FILE DETECTED{RESET}")
            new_count += 1

    # Security summary
    print(f"""
{CYAN}╔════════════════════════════════════════╗
║           SECURITY SUMMARY             ║
╚════════════════════════════════════════╝{RESET}
""")

    print(f"Files checked : {len(baseline)}")
    print(f"{GREEN}Safe          : {safe_count}{RESET}")
    print(f"{YELLOW}Modified      : {modified_count}{RESET}")
    print(f"{RED}Deleted       : {deleted_count}{RESET}")
    print(f"{RED}New files     : {new_count}{RESET}")

    if modified_count > 0 or deleted_count > 0 or new_count > 0:
        print(f"\n{RED}⚠️ SECURITY ALERT: Changes detected!{RESET}")
    else:
        print(f"\n{GREEN}✅ SYSTEM SECURE: No changes detected!{RESET}")


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
            print(f"\n{RED}❌ Invalid option. Please choose 1, 2, or 3.{RESET}")


if __name__ == "__main__":
    main()
