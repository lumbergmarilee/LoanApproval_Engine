from Loan_Approval_Engine import loan_approval_algorithm, scoring_algorithm, find_max_approved, find_suitable_period


# I used Claude Opus 4.6 to write tests for the algorithm

def testing():
    print("=== LOAN DECISION ENGINE TESTS ===\n")
    passed = 0
    failed = 0

    def check(test_name, actual, expected):
        nonlocal passed, failed
        if actual == expected:
            print(f"  PASS: {test_name}")
            passed += 1
        else:
            print(f"  FAIL: {test_name}")
            print(f"    Expected: {expected}")
            print(f"    Got:      {actual}")
            failed += 1

    # --- Debt scenario: always rejected ---
    print("-- Debt (49002010965) --")
    check("Debt, normal request",
          loan_approval_algorithm(49002010965, 5000, 24), ("negative",))
    check("Debt, small loan short period",
          loan_approval_algorithm(49002010965, 2000, 12), ("negative",))
    check("Debt, max loan max period",
          loan_approval_algorithm(49002010965, 10000, 60), ("negative",))

    # --- Scoring algorithm unit tests ---
    print("\n-- Scoring Algorithm --")
    check("Score exactly 1 is positive",
          scoring_algorithm(100, 2000, 20), ("positive", 2000, 20))
    check("Score above 1",
          scoring_algorithm(300, 2000, 12), ("positive", 2000, 12))
    check("Score below 1",
          scoring_algorithm(100, 2000, 12), ("negative", 0, 12))
    check("Score just below 1",
          scoring_algorithm(100, 5000, 48), ("negative", 0, 48))
    check("Large modifier large amount",
          scoring_algorithm(1000, 10000, 12), ("positive", 10000, 12))

    # --- find_max_approved unit tests ---
    print("\n-- Find Max Approved --")
    check("Modifier 100, period 20: max is 2000",
          find_max_approved(100, 20), ("positive", 2000, 20))
    check("Modifier 300, period 12: max is 3600",
          find_max_approved(300, 12), ("positive", 3600, 12))
    check("Modifier 300, period 24: max is 7200",
          find_max_approved(300, 24), ("positive", 7200, 24))
    check("Modifier 1000, period 12: capped at 10000",
          find_max_approved(1000, 12), ("positive", 10000, 12))
    check("Modifier 1000, period 60: capped at 10000",
          find_max_approved(1000, 60), ("positive", 10000, 60))
    check("Modifier 100, period 12: max is 1200, below minimum -> negative",
          find_max_approved(100, 12), ("negative", 0, 12))

    # --- find_suitable_period unit tests ---
    print("\n-- Find Suitable Period --")
    check("Segment 1, min amount needs 20 months",
          find_suitable_period(100, 2000), ("positive", 2000, 20))
    check("Segment 2, calculated period below 12 gets clamped",
          find_suitable_period(300, 2000), ("positive", 2000, 12))
    check("Segment 3, calculated period well below 12",
          find_suitable_period(1000, 2000), ("positive", 2000, 12))

    # --- Segment 1 (modifier=100) ---
    print("\n-- Segment 1 (credit_modifier=100) --")
    check("Period 20: max approvable is 2000",
          loan_approval_algorithm(49002010976, 5000, 20), ("positive", 2000, 20))
    check("Period 12: no amount works, falls back to period 20",
          loan_approval_algorithm(49002010976, 3000, 12), ("positive", 2000, 20))
    check("Period 60: max approvable is 6000",
          loan_approval_algorithm(49002010976, 3000, 60), ("positive", 6000, 60))

    # --- Segment 2 (modifier=300) ---
    print("\n-- Segment 2 (credit_modifier=300) --")
    check("Period 12: max is 3600",
          loan_approval_algorithm(49002010987, 5000, 12), ("positive", 3600, 12))
    check("Period 24: max is 7200",
          loan_approval_algorithm(49002010987, 3000, 24), ("positive", 7200, 24))
    check("Period 60: capped at 10000",
          loan_approval_algorithm(49002010987, 3000, 60), ("positive", 10000, 60))

    # --- Segment 3 (modifier=1000) ---
    print("\n-- Segment 3 (credit_modifier=1000) --")
    check("Period 12: capped at 10000",
          loan_approval_algorithm(49002010998, 2000, 12), ("positive", 10000, 12))
    check("Period 60: capped at 10000",
          loan_approval_algorithm(49002010998, 5000, 60), ("positive", 10000, 60))
    check("Period 24: capped at 10000",
          loan_approval_algorithm(49002010998, 8000, 24), ("positive", 10000, 24))

    # --- Invalid period triggers find_suitable_period ---
    print("\n-- Invalid Period Fallback --")
    check("Period too short (6), segment 1: finds period 20",
          loan_approval_algorithm(49002010976, 3000, 6), ("positive", 2000, 20))
    check("Period too long (100), segment 2: finds period 12",
          loan_approval_algorithm(49002010987, 3000, 100), ("positive", 2000, 12))
    check("Period too short (5), segment 3: finds period 12",
          loan_approval_algorithm(49002010998, 5000, 5), ("positive", 2000, 12))

    # --- Return format consistency ---
    print("\n-- Return Format --")
    result = loan_approval_algorithm(49002010998, 5000, 24)
    check("Positive result is a tuple with 3 elements",
          isinstance(result, tuple) and len(result) == 3, True)
    check("Elements are (str, number, number)",
          result[0] == "positive" and isinstance(result[1], (int, float)) and isinstance(result[2], (int, float)), True)

    # --- Unknown personal code ---
    print("\n-- Unknown Personal Code --")
    result = loan_approval_algorithm(12345678901, 3000, 24)
    check("Unknown code returns negative",
          result[0], "negative")

    print(f"\n=== RESULTS: {passed} passed, {failed} failed out of {passed + failed} ===")

testing()