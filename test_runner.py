import subprocess
import os
import difflib

SOURCE_ROOT = os.path.join("programs", "source")
OUTPUT_ROOT = os.path.join("programs", "output")

passed = 0
failed = 0
missing = 0
total = 0

missing_files = []

for folder in sorted(os.listdir(SOURCE_ROOT)):
    source_dir = os.path.join(SOURCE_ROOT, folder)
    output_dir = os.path.join(OUTPUT_ROOT, folder)

    if not os.path.isdir(source_dir):
        continue

    for filename in sorted(os.listdir(source_dir)):
        if not filename.endswith(".netlang"):
            continue

        basename = filename[:-8]  # removes .netlang
        source_path = os.path.join(source_dir, filename)
        expected_path = os.path.join(output_dir, basename + ".expected.txt")

        if not os.path.exists(expected_path):
            print(f"[!] Missing expected file for {folder}/{filename}")
            missing += 1
            missing_files.append(f"{folder}/{filename}")
            continue

        total += 1

        with open(expected_path, "r", encoding="utf-8") as f:
            expected_output = f.read().strip()

        try:
            result = subprocess.run(
                ["python", "main.py", source_path],
                capture_output=True,
                text=True,
                timeout=5,
            )
            actual_output = (result.stdout + result.stderr).strip()

            if actual_output == expected_output:
                print(f"[✓] {folder}/{filename}")
                passed += 1
            else:
                print(f"[✗] {folder}/{filename} — output mismatch")
                diff = "\n".join(difflib.unified_diff(
                    expected_output.splitlines(),
                    actual_output.splitlines(),
                    fromfile='expected',
                    tofile='actual',
                    lineterm=''
                ))
                print(diff)
                failed += 1

        except subprocess.TimeoutExpired:
            print(f"[✗] {folder}/{filename} — timeout")
            failed += 1

# Summary
print("\nSummary:")
print(f"  Passed : {passed}")
print(f"  Failed : {failed}")
print(f"  Missing: {missing}")
print(f"  Total  : {total}")

if missing_files:
    print("\nMissing expected output for:")
    for f in missing_files:
        print(f"  - {f}")