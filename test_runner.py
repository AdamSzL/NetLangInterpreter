import subprocess
import os
import difflib
import sys

if len(sys.argv) < 2:
    print("Usage: python test_runner.py <package_number> [files_to_skip...]")
    sys.exit(1)

PACKAGE_NUMBER = sys.argv[1]
SKIP_FILES = set(sys.argv[2:])

SOURCE_DIR = os.path.join("programs", "source", PACKAGE_NUMBER)
OUTPUT_DIR = os.path.join("programs", "output", PACKAGE_NUMBER)

passed = 0
failed = 0

for filename in os.listdir(SOURCE_DIR):
    if not filename.endswith(".netlang"):
        continue
    if filename in SKIP_FILES:
        print(f"[!] Skipping {filename}")
        continue

    basename = filename[:-8]  # usuwa .netlang
    source_path = os.path.join(SOURCE_DIR, filename)
    expected_path = os.path.join(OUTPUT_DIR, basename + ".expected.txt")

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
            print(f"[✓] {filename}")
            passed += 1
        else:
            print(f"[✗] {filename} — output mismatch")
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
        print(f"[✗] {filename} — timeout")
        failed += 1

print(f"\nSummary: {passed} passed, {failed} failed")