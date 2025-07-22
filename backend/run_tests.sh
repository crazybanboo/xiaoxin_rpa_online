#!/bin/bash

# Test runner script for xiaoxin_rpa backend
# Runs pytest with different configurations

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== 小新RPA后端单元测试 ===${NC}"

# Activate virtual environment
if [ -d ".env" ]; then
    echo "Activating virtual environment..."
    source .env/bin/activate
fi

# Function to run tests with error handling
run_test() {
    local test_type="$1"
    local test_command="$2"
    local description="$3"
    
    echo -e "\n${YELLOW}Running $description...${NC}"
    echo "Command: $test_command"
    echo "----------------------------------------"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✅ $description completed successfully!${NC}"
        return 0
    else
        echo -e "${RED}❌ $description failed!${NC}"
        return 1
    fi
}

# Parse command line arguments
case "${1:-all}" in
    "unit")
        run_test "unit" "python -m pytest tests/unit/ -v" "Unit Tests"
        ;;
    "integration")
        run_test "integration" "python -m pytest tests/integration/ -v" "Integration Tests"
        ;;
    "models")
        run_test "models" "python -m pytest tests/unit/test_models.py -v" "Model Tests"
        ;;
    "crud")
        run_test "crud" "python -m pytest tests/unit/test_crud.py -v" "CRUD Tests"
        ;;
    "api")
        run_test "api" "python -m pytest tests/unit/test_api.py -v" "API Tests"
        ;;
    "schemas")
        run_test "schemas" "python -m pytest tests/unit/test_schemas.py -v" "Schema Tests"
        ;;
    "coverage")
        run_test "coverage" "python -m pytest --cov=app --cov-report=html --cov-report=term-missing" "Coverage Tests"
        ;;
    "quick")
        run_test "quick" "python -m pytest --no-cov -x" "Quick Tests"
        ;;
    "all")
        echo "Running all test categories..."
        
        run_test "models" "python -m pytest tests/unit/test_models.py -v" "Model Tests"
        model_result=$?
        
        run_test "crud" "python -m pytest tests/unit/test_crud.py -v" "CRUD Tests" 
        crud_result=$?
        
        run_test "api" "python -m pytest tests/unit/test_api.py -v" "API Tests"
        api_result=$?
        
        run_test "schemas" "python -m pytest tests/unit/test_schemas.py -v" "Schema Tests"
        schema_result=$?
        
        # Summary
        echo -e "\n${YELLOW}=== Test Summary ===${NC}"
        [ $model_result -eq 0 ] && echo -e "${GREEN}✅ Model Tests: PASSED${NC}" || echo -e "${RED}❌ Model Tests: FAILED${NC}"
        [ $crud_result -eq 0 ] && echo -e "${GREEN}✅ CRUD Tests: PASSED${NC}" || echo -e "${RED}❌ CRUD Tests: FAILED${NC}"
        [ $api_result -eq 0 ] && echo -e "${GREEN}✅ API Tests: PASSED${NC}" || echo -e "${RED}❌ API Tests: FAILED${NC}"
        [ $schema_result -eq 0 ] && echo -e "${GREEN}✅ Schema Tests: PASSED${NC}" || echo -e "${RED}❌ Schema Tests: FAILED${NC}"
        
        total_failed=$((model_result + crud_result + api_result + schema_result))
        if [ $total_failed -eq 0 ]; then
            echo -e "\n${GREEN}🎉 All tests passed!${NC}"
        else
            echo -e "\n${RED}💥 $total_failed test suite(s) failed${NC}"
            exit 1
        fi
        ;;
    "help")
        echo "Usage: ./run_tests.sh [option]"
        echo ""
        echo "Options:"
        echo "  unit        - Run unit tests only"
        echo "  integration - Run integration tests only"  
        echo "  models      - Run model tests only"
        echo "  crud        - Run CRUD tests only"
        echo "  api         - Run API tests only"
        echo "  schemas     - Run schema tests only"
        echo "  coverage    - Run tests with coverage report"
        echo "  quick       - Run tests quickly without coverage"
        echo "  all         - Run all test categories (default)"
        echo "  help        - Show this help message"
        ;;
    *)
        echo "Unknown option: $1"
        echo "Use './run_tests.sh help' for usage information"
        exit 1
        ;;
esac