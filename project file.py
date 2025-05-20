import os
import hashlib
from collections import defaultdict
import time
import csv

def get_file_hash(file_path, block_size=65536):
    """Returns SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(block_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
        return None

def find_duplicate_files(directory):
    print("\n🔍 Scanning directory for duplicate files...\n")
    hashes = defaultdict(list)
    total_files = 0
    scanned = 0

    for root, _, files in os.walk(directory):
        for file in files:
            total_files += 1
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            if file_hash:
                hashes[file_hash].append(file_path)
            scanned += 1
            print(f" Scanned: {scanned}/{total_files}", end='\r')

    duplicates = {hash_: paths for hash_, paths in hashes.items() if len(paths) > 1}
    return duplicates

def save_report(duplicates):
    try:
        with open("duplicate_files_report.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Hash", "Duplicate Files"])
            for hash_, files in duplicates.items():
                writer.writerow([hash_, " | ".join(files)])
        print("\n✅ Duplicate report saved as 'duplicate_files_report.csv'")
    except Exception as e:
        print(f"⚠️ Error saving report: {e}")

def display_duplicates(duplicates):
    if not duplicates:
        print("\n🎉 No duplicate files found!")
        return

    print("\n⚠️ Duplicate Files Found:")
    for hash_, files in duplicates.items():
        print(f"\n🔁 Duplicate Group (Hash: {hash_[:10]}...)")
        for file in files:
            print(f" - {file}")

# ----------- MAIN PROGRAM -------------
if __name__ == "__main__":
    path = input("📁 Enter the folder path to scan for duplicates: ").strip()

    if not os.path.isdir(path):
        print("❌ Invalid folder path.")
    else:
        start_time = time.time()
        duplicates = find_duplicate_files(path)
        end_time = time.time()

        display_duplicates(duplicates)

        save = input("\n💾 Save report as CSV? (y/n): ").strip().lower()
        if save == 'y':
            save_report(duplicates)

        print(f"\n⏱️ Scan completed in {end_time - start_time:.2f} seconds.")
