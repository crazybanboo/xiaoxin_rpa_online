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
    "auth")
        run_test "auth" "python -m pytest tests/unit/test_auth.py -v --tb=short" "Auth Unit Tests"
        ;;
    "auth-integration")
        run_test "auth-integration" "python -m pytest tests/integration/test_auth_integration.py -v" "Auth Integration Tests"
        ;;
    "api-integration")
        run_test "api-integration" "python -m pytest tests/integration/test_api_integration.py -v" "API Integration Tests"
        ;;
    "db-integration")
        run_test "db-integration" "python -m pytest tests/integration/test_database_integration.py -v" "Database Integration Tests"
        ;;
    "coverage")
        run_test "coverage" "python -m pytest --cov=app --cov-report=html --cov-report=term-missing" "Coverage Tests"
        ;;
    "quick")
        run_test "quick" "python -m pytest --no-cov -x" "Quick Tests"
        ;;
    "all")
        echo "Running all test categories..."
        
        # Unit Tests
        run_test "models" "python -m pytest tests/unit/test_models.py -v" "Model Tests"
        model_result=$?
        
        run_test "crud" "python -m pytest tests/unit/test_crud.py -v" "CRUD Tests" 
        crud_result=$?
        
        run_test "api_unit" "python -m pytest tests/unit/test_api.py -v" "API Unit Tests"
        api_unit_result=$?
        
        run_test "schemas" "python -m pytest tests/unit/test_schemas.py -v" "Schema Tests"
        schema_result=$?
        
        run_test "auth_unit" "python -m pytest tests/unit/test_auth.py -v" "Auth Unit Tests"
        auth_unit_result=$?
        
        # Integration Tests
        run_test "api_integration" "python -m pytest tests/integration/test_api_integration.py -v" "API Integration Tests"
        api_integration_result=$?
        
        run_test "auth_integration" "python -m pytest tests/integration/test_auth_integration.py -v" "Auth Integration Tests"
        auth_integration_result=$?
        
        run_test "db_integration" "python -m pytest tests/integration/test_database_integration.py -v" "Database Integration Tests"
        db_integration_result=$?
        
        # Summary
        echo -e "\n${YELLOW}=== Test Summary ===${NC}"
        echo -e "${YELLOW}Unit Tests:${NC}"
        [ $model_result -eq 0 ] && echo -e "${GREEN}✅ Model Tests: PASSED${NC}" || echo -e "${RED}❌ Model Tests: FAILED${NC}"
        [ $crud_result -eq 0 ] && echo -e "${GREEN}✅ CRUD Tests: PASSED${NC}" || echo -e "${RED}❌ CRUD Tests: FAILED${NC}"
        [ $api_unit_result -eq 0 ] && echo -e "${GREEN}✅ API Unit Tests: PASSED${NC}" || echo -e "${RED}❌ API Unit Tests: FAILED${NC}"
        [ $schema_result -eq 0 ] && echo -e "${GREEN}✅ Schema Tests: PASSED${NC}" || echo -e "${RED}❌ Schema Tests: FAILED${NC}"
        [ $auth_unit_result -eq 0 ] && echo -e "${GREEN}✅ Auth Unit Tests: PASSED${NC}" || echo -e "${RED}❌ Auth Unit Tests: FAILED${NC}"
        
        echo -e "${YELLOW}Integration Tests:${NC}"
        [ $api_integration_result -eq 0 ] && echo -e "${GREEN}✅ API Integration Tests: PASSED${NC}" || echo -e "${RED}❌ API Integration Tests: FAILED${NC}"
        [ $auth_integration_result -eq 0 ] && echo -e "${GREEN}✅ Auth Integration Tests: PASSED${NC}" || echo -e "${RED}❌ Auth Integration Tests: FAILED${NC}"
        [ $db_integration_result -eq 0 ] && echo -e "${GREEN}✅ Database Integration Tests: PASSED${NC}" || echo -e "${RED}❌ Database Integration Tests: FAILED${NC}"
        
        total_failed=$((model_result + crud_result + api_unit_result + schema_result + auth_unit_result + api_integration_result + auth_integration_result + db_integration_result))
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
        echo "Test Categories:"
        echo "  unit              - Run all unit tests"
        echo "  integration       - Run all integration tests"
        echo "  all               - Run all test categories (default)"
        echo ""
        echo "Unit Test Options:"
        echo "  models            - Run model tests only"
        echo "  crud              - Run CRUD tests only"
        echo "  api               - Run API unit tests only"
        echo "  schemas           - Run schema tests only"
        echo "  auth              - Run auth unit tests only"
        echo ""
        echo "Integration Test Options:"
        echo "  api-integration   - Run API integration tests only"
        echo "  auth-integration  - Run auth integration tests only"
        echo "  db-integration    - Run database integration tests only"
        echo ""
        echo "Other Options:"
        echo "  coverage          - Run tests with coverage report"
        echo "  quick             - Run tests quickly without coverage"
        echo "  help              - Show this help message"
        ;;
    *)
        echo "Unknown option: $1"
        echo "Use './run_tests.sh help' for usage information"
        exit 1
        ;;
esac