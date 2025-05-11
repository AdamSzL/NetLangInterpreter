import subprocess
import os
import difflib

TEST_DIR = os.path.join(os.curdir, "programs", "3")
print(TEST_DIR)

passed = 0
failed = 0

for filename in os.listdir(TEST_DIR):
    if not filename.endswith(".netlang"):
        continue

    basename = filename[:-8]  # usuwa .netlang
    source_path = os.path.join(TEST_DIR, filename)
    expected_path = os.path.join(TEST_DIR, basename + ".expected.txt")

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