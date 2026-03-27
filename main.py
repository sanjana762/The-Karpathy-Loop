from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
import subprocess
import sys
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_code():
    # Initial version: correct but inefficient O(n^2)
    code = """
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
"""
    with open("generated_code.py", "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")

def run_tests():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "test_code.py"],
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr

def fallback_improved_code():
    # Local fallback if API quota is unavailable
    return """
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []
""".strip() + "\n"

def improve_code(current_code, feedback):
    prompt = f"""
Improve the following Python code based on test feedback.
Optimize it if there is a performance issue.
Return ONLY valid Python code, no explanations.

Current code:
{current_code}

Test feedback:
{feedback}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip() + "\n"

    except RateLimitError:
        print("OpenAI quota unavailable. Using local optimized fallback.")
        return fallback_improved_code()

    except Exception as e:
        print(f"OpenAI call failed: {e}")
        print("Using local optimized fallback.")
        return fallback_improved_code()

def tests_passed(feedback):
    text = feedback.lower()
    return (
        "passed" in text
        and "failed" not in text
        and "error" not in text
        and "internalerror" not in text
    )

def main():
    generate_code()

    for i in range(3):
        print(f"\nIteration {i + 1}")

        feedback = run_tests()
        print(feedback)

        if tests_passed(feedback):
            print("✅ Code passed all tests!")
            break

        with open("generated_code.py", "r", encoding="utf-8") as f:
            current_code = f.read()

        improved_code = improve_code(current_code, feedback)

        with open("generated_code.py", "w", encoding="utf-8") as f:
            f.write(improved_code)

if __name__ == "__main__":
    main()