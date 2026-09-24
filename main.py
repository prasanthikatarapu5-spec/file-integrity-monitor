import hashlib
import json
import os
from datetime import datetime


# ==============================
# CONFIGURATION
# ==============================

TEST_FOLDER = "test_files"
BASELINE_FILE = "baseline.json"
LOG_FILE = "scan_log.txt"


# ==============================
# COLORS
# ==============================

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


# ==============================
# BANNER
# ==============================

def show_banner():
    print()
    print("╔════════════════════════════════════════╗")
    print("║        🔐 FILE INTEGRITY MONITOR       ║")
    print("║          SHA-256 Security Tool         ║")
    print("╚════════════════════════════════════════╝")
    print()


# ==============================
# CALCULATE SHA-256 HASH
# ==============================

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                data = file.read(4096)

                if not data:
                    break

                sha256.update(data)

        return sha256.hexdigest()

    except Exception as error:
        print(f"{RED}Error reading {file_path}: {error}{RESET}")
        return None


# ==============================
# GET FILES
# ==============================

def get_files():
    files = []

    if not os.path.exists(TEST_FOLDER):
        os.makedirs(TEST_FOLDER)

    for root, directories, filenames in os.walk(TEST_FOLDER):
        for filename in filenames:
            file_path = os.path.join(root, filename)

            files.append(file_path)

    return sorted(files)


# ==============================
# CREATE BASELINE
# ==============================

def create_baseline():
    print()
    print(f"{CYAN}📌 Creating SHA-256 baseline...{RESET}")
    print()

    files = get_files()

    if not files:
        print(f"{YELLOW}⚠ No files found in '{TEST_FOLDER}'.{RESET}")
        print()
        return

    baseline = {}

    for file_path in files:
        file_hash = calculate_hash(file_path)

        if file_hash:
            relative_path = os.path.relpath(
                file_path,
                TEST_FOLDER
            )

            baseline[relative_path] = file_hash

            print(f"{GREEN}✅ {relative_path}{RESET}")

    with open(BASELINE_FILE, "w", encoding="utf-8") as file:
        json.dump(baseline, file, indent=4)

    print()
    print(f"{GREEN}✅ Baseline created successfully!{RESET}")
    print(f"Files recorded : {len(baseline)}")
    print(f"Saved to       : {BASELINE_FILE}")
    print()


# ==============================
# WRITE SCAN LOG
# ==============================

def write_log(results):
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as log:

        log.write("\n")
        log.write("=" * 55 + "\n")
        log.write(
            f"FILE INTEGRITY SCAN - {timestamp}\n"
        )
        log.write("=" * 55 + "\n")

        for result in results:
            log.write(result + "\n")

        log.write("=" * 55 + "\n")


# ==============================
# CHECK INTEGRITY
# ==============================

def check_integrity():

    print()
    print(f"{CYAN}🔍 Checking file integrity...{RESET}")
    print()

    if not os.path.exists(BASELINE_FILE):

        print(
            f"{YELLOW}⚠ No baseline found.{RESET}"
        )

        print()
        print(
            "Please choose option 1 first "
            "to create a baseline."
        )
        print()

        return

    try:

        with open(
            BASELINE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            baseline = json.load(file)

    except Exception as error:

        print(
            f"{RED}❌ Could not read baseline: "
            f"{error}{RESET}"
        )

        return

    current_files = get_files()

    current_hashes = {}

    for file_path in current_files:

        relative_path = os.path.relpath(
            file_path,
            TEST_FOLDER
        )

        file_hash = calculate_hash(file_path)

        if file_hash:

            current_hashes[
                relative_path
            ] = file_hash

    safe = 0
    modified = 0
    deleted = 0
    new_files = 0

    results = []

    # ==============================
    # CHECK BASELINE FILES
    # ==============================

    for filename in baseline:

        if filename not in current_hashes:

            message = (
                f"❌ {filename} - DELETED"
            )

            print(f"{RED}{message}{RESET}")

            deleted += 1
            results.append(message)

        elif (
            baseline[filename]
            != current_hashes[filename]
        ):

            message = (
                f"⚠️ {filename} - MODIFIED"
            )

            print(f"{YELLOW}{message}{RESET}")

            modified += 1
            results.append(message)

        else:

            message = (
                f"✅ {filename} - No changes"
            )

            print(f"{GREEN}{message}{RESET}")

            safe += 1
            results.append(message)

    # ==============================
    # CHECK NEW FILES
    # ==============================

    for filename in current_hashes:

        if filename not in baseline:

            message = (
                f"🆕 {filename} - NEW FILE"
            )

            print(f"{CYAN}{message}{RESET}")

            new_files += 1
            results.append(message)

    # ==============================
    # SECURITY SUMMARY
    # ==============================

    print()

    print(
        "╔════════════════════════════════════════╗"
    )
    print(
        "║           SECURITY SUMMARY             ║"
    )
    print(
        "╚════════════════════════════════════════╝"
    )

    print()

    print(
        f"Files checked : {len(current_hashes)}"
    )

    print(
        f"{GREEN}Safe          : {safe}{RESET}"
    )

    print(
        f"{YELLOW}Modified      : {modified}{RESET}"
    )

    print(
        f"{RED}Deleted       : {deleted}{RESET}"
    )

    print(
        f"{CYAN}New files     : {new_files}{RESET}"
    )

    print()

    # ==============================
    # SECURITY RESULT
    # ==============================

    if (
        modified == 0
        and deleted == 0
        and new_files == 0
    ):

        print(
            f"{GREEN}"
            "✅ SYSTEM SECURE: "
            "No changes detected!"
            f"{RESET}"
        )

    else:

        print(
            f"{RED}"
            "🚨 SECURITY ALERT: "
            "File changes detected!"
            f"{RESET}"
        )

    # ==============================
    # SAVE LOG
    # ==============================

    write_log(results)

    print()

    print(
        f"{CYAN}"
        "📝 Scan log saved to: "
        f"{LOG_FILE}"
        f"{RESET}"
    )

    print()


# ==============================
# MAIN MENU
# ==============================

def main():

    while True:

        show_banner()

        print("1. Create baseline")
        print("2. Check integrity")
        print("3. Exit")
        print()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":

            create_baseline()

        elif choice == "2":

            check_integrity()

        elif choice == "3":

            print()
            print("👋 Goodbye!")
            break

        else:

            print()

            print(
                f"{RED}"
                "❌ Invalid option. "
                "Please choose 1, 2, or 3."
                f"{RESET}"
            )

            print()


# ==============================
# START PROGRAM
# ==============================

if __name__ == "__main__":
    main()
