#!/bin/bash
# Test all agents — discovers both tests/ subdirectories and root-level test_main.py files
# Usage: bash _scripts/test_all.sh [--coverage]

COVERAGE=false
if [[ "$1" == "--coverage" ]]; then
  COVERAGE=true
fi

passed=0
failed=0
skipped=0
total=0
cov_sum=0
cov_count=0

# Coverage JSON output
COV_JSON="[]"

echo "Testing all agents..."

# Collect all unique agent directories that have tests
tested_agents=":"

run_pytest() {
  local agent_dir="$1"
  local test_target="$2"
  local label="$3"

  total=$((total+1))
  echo -n "\rTesting $agent_dir${label:+ ($label)}... "

  if [ "$COVERAGE" = true ]; then
    # Run with coverage and capture the TOTAL line
    output=$(cd "$agent_dir" && python3 -c "import subprocess, sys
try:
    cmd = ['python3', '-m', 'pytest', '-q', '--disable-warnings', '--cov=.', '--cov-report=term-missing']
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    sys.stdout.write(res.stdout)
    sys.stderr.write(res.stderr)
    sys.exit(res.returncode)
except subprocess.TimeoutExpired:
    sys.stderr.write('Timeout!\n')
    sys.exit(124)
" 2>&1)
    exit_code=$?

    # Extract coverage % from TOTAL line
    cov_pct=$(echo "$output" | grep "^TOTAL" | awk '{print $NF}' | tr -d '%')
    if [ -n "$cov_pct" ] && [ "$cov_pct" -eq "$cov_pct" ] 2>/dev/null; then
      cov_sum=$((cov_sum + cov_pct))
      cov_count=$((cov_count + 1))
      COV_JSON=$(echo "$COV_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
data.append({'agent': '$agent_dir', 'coverage': $cov_pct})
json.dump(data, sys.stdout)
")
    fi
  else
    (cd "$agent_dir" && python3 -m pytest -q --disable-warnings > /dev/null 2>&1)
    exit_code=$?
  fi

  if [ $exit_code -eq 0 ]; then
    passed=$((passed+1))
  else
    failed=$((failed+1))
    echo -e "\n❌ FAILED: $agent_dir"
  fi
}

# 1) Agents with tests/ subdirectory (pytest on tests/)
for d in $(find . -maxdepth 5 -type d -name "tests" ! -path './.git/*' ! -path './_scripts/*' | sort); do
  agent_dir=$(dirname "$d")
  [[ "$tested_agents" == *":$agent_dir:"* ]] && continue
  tested_agents="${tested_agents}${agent_dir}:"

  # Check for Python test files
  py_tests=$(find "$d" -maxdepth 1 -name "test_*.py" 2>/dev/null | head -1)
  ts_tests=$(find "$d" -maxdepth 1 \( -name "*.test.ts" -o -name "*.test.js" -o -name "*.spec.ts" -o -name "*.spec.js" \) 2>/dev/null | head -1)

  if [ -n "$py_tests" ]; then
    run_pytest "$agent_dir" "tests/" ""
  elif [ -n "$ts_tests" ]; then
    total=$((total+1))
    echo -n "\rTesting $agent_dir (TS)... "
    if (cd "$agent_dir" && npm test --silent > /dev/null 2>&1); then
      passed=$((passed+1))
    else
      skipped=$((skipped+1))
      echo -e "\n⏭️  SKIPPED (TS): $agent_dir"
    fi
  else
    skipped=$((skipped+1))
  fi
done

# 2) Agents with test_main.py in root (not inside tests/)
for f in $(find . -maxdepth 4 -name "test_main.py" -type f ! -path '*/tests/*' | sort); do
  agent_dir=$(dirname "$f")
  [[ "$tested_agents" == *":$agent_dir:"* ]] && continue
  tested_agents="${tested_agents}${agent_dir}:"

  run_pytest "$agent_dir" "test_main.py" "root test"
done

echo -e "\r\033[K" # Clear the line
echo "====================================="
echo "Total tested : $total"
echo "✅ Passed    : $passed"
[ "$failed" -gt 0 ] && echo "❌ Failed    : $failed"
[ "$skipped" -gt 0 ] && echo "⏭️  Skipped   : $skipped"

if [ "$COVERAGE" = true ] && [ "$cov_count" -gt 0 ]; then
  avg_cov=$((cov_sum / cov_count))
  echo "📊 Avg Coverage: ${avg_cov}% (${cov_count} agents)"

  # Write coverage report JSON
  report_file="$(dirname "$0")/coverage.json"
  python3 -c "
import json, sys
data = json.loads('''$COV_JSON''')
report = {
    'timestamp': '$(date -u +%Y-%m-%dT%H:%M:%SZ)',
    'summary': {
        'total_agents': $total,
        'agents_with_coverage': $cov_count,
        'average_coverage': $avg_cov,
        'passed': $passed,
        'failed': $failed,
        'skipped': $skipped
    },
    'agents': sorted(data, key=lambda x: x['coverage'], reverse=True)
}
with open('$report_file', 'w') as f:
    json.dump(report, f, indent=2)
print(f'📄 Report written to $report_file')
"
fi

echo "====================================="

if [ "$failed" -gt 0 ]; then
  exit 1
else
  echo "✅ All agents are passing!"
  exit 0
fi
