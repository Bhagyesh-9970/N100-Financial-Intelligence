"""
Master Test File
Sprint 1 Day 3
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

print("=" * 60)
print("N100 FINANCIAL INTELLIGENCE PLATFORM")
print("SPRINT 1 - DAY 3 TEST SUITE")
print("=" * 60)

print("\nRunning Loader Tests...")
import tests.etl.test_loader

print("Loader Tests Passed")

print("\nRunning Normalizer Tests...")
import tests.etl.test_normaliser

print("Normalizer Tests Passed")

print("\nRunning Validator Tests...")
import tests.etl.test_validator

print("Validator Tests Passed")

print("\nRunning Validation Pipeline...")
import tests.etl.test_pipeline

print("Pipeline Tests Passed")

print("\n")
print("=" * 60)
print("ALL TESTS PASSED")
print("=" * 60)