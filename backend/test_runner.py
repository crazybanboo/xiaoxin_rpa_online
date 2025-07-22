#!/usr/bin/env python3
"""
Test runner script for the backend application
Provides different test execution modes and reporting options
"""

import sys
import subprocess
from pathlib import Path


def run_command(cmd: list, description: str = ""):
    """Run a command and handle output"""
    if description:
        print(f"\n{'='*50}")
        print(f"Running: {description}")
        print(f"Command: {' '.join(cmd)}")
        print('='*50)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode == 0


def main():
    """Main test runner function"""
    if len(sys.argv) < 2:
        print("Usage: python test_runner.py <mode>")
        print("\nAvailable modes:")
        print("  unit        - Run only unit tests")
        print("  integration - Run only integration tests")
        print("  all         - Run all tests")
        print("  coverage    - Run all tests with detailed coverage report")
        print("  quick       - Run tests without coverage")
        print("  models      - Run only model tests")
        print("  crud        - Run only CRUD tests")
        print("  api         - Run only API tests")
        print("  schemas     - Run only schema tests")
        print("  parallel    - Run tests in parallel")
        print("  watch       - Run tests in watch mode (requires pytest-watch)")
        sys.exit(1)

    mode = sys.argv[1].lower()
    
    # Base pytest command
    base_cmd = ["python", "-m", "pytest"]
    
    # Mode-specific configurations
    if mode == "unit":
        cmd = base_cmd + ["-m", "unit", "--tb=short"]
        description = "Unit Tests"
        
    elif mode == "integration":
        cmd = base_cmd + ["-m", "integration", "--tb=short"]
        description = "Integration Tests"
        
    elif mode == "all":
        cmd = base_cmd + ["--tb=short"]
        description = "All Tests"
        
    elif mode == "coverage":
        cmd = base_cmd + [
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=xml",
            "--tb=short"
        ]
        description = "All Tests with Coverage"
        
    elif mode == "quick":
        cmd = base_cmd + ["--no-cov", "--tb=line"]
        description = "Quick Tests (No Coverage)"
        
    elif mode == "models":
        cmd = base_cmd + ["-m", "models", "--tb=short"]
        description = "Model Tests"
        
    elif mode == "crud":
        cmd = base_cmd + ["-m", "crud", "--tb=short"]
        description = "CRUD Tests"
        
    elif mode == "api":
        cmd = base_cmd + ["-m", "api", "--tb=short"]
        description = "API Tests"
        
    elif mode == "schemas":
        cmd = base_cmd + ["-m", "schemas", "--tb=short"]
        description = "Schema Tests"
        
    elif mode == "parallel":
        cmd = base_cmd + ["-n", "auto", "--tb=short"]  # Requires pytest-xdist
        description = "Parallel Tests"
        
    elif mode == "watch":
        cmd = ["python", "-m", "ptw", "--", "--tb=short"]  # Requires pytest-watch
        description = "Watch Mode Tests"
        
    elif mode == "verbose":
        cmd = base_cmd + ["-v", "-s", "--tb=long"]
        description = "Verbose Tests"
        
    elif mode == "failed":
        cmd = base_cmd + ["--lf", "--tb=short"]  # Last failed
        description = "Re-run Failed Tests"
        
    elif mode == "debug":
        cmd = base_cmd + ["-v", "-s", "--tb=long", "--pdb"]
        description = "Debug Mode Tests (with PDB)"
        
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)
    
    # Run the tests
    success = run_command(cmd, description)
    
    # Additional reporting for coverage mode
    if mode == "coverage" and success:
        print("\n" + "="*50)
        print("Coverage report generated in htmlcov/index.html")
        print("="*50)
        
        # Try to open coverage report if running interactively
        try:
            import webbrowser
            coverage_path = Path("htmlcov/index.html")
            if coverage_path.exists():
                print(f"Opening coverage report: {coverage_path.absolute()}")
                webbrowser.open(f"file://{coverage_path.absolute()}")
        except:
            pass
    
    # Print summary
    if success:
        print(f"\n✅ {description} completed successfully!")
    else:
        print(f"\n❌ {description} failed!")
        sys.exit(1)


def show_test_stats():
    """Show test statistics"""
    cmd = ["python", "-m", "pytest", "--collect-only", "-q"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Test Statistics:")
        print(result.stdout)
    else:
        print("Failed to collect test statistics")


if __name__ == "__main__":
    # Show test stats first
    if len(sys.argv) > 1 and sys.argv[1] in ["stats", "info"]:
        show_test_stats()
        sys.exit(0)
        
    main()