#!/bin/bash
# Test all agents — discovers both tests/ subdirectories and root-level test_main.py files
passed=0
failed=0
skipped=0
total=0

echo "Testing all agents..."

# Collect all unique agent directories that have tests
declare -A tested_agents

# 1) Agents with tests/ subdirectory (pytest on tests/)
for d in $(find . -maxdepth 5 -type d -name "tests" ! -path './.git/*' ! -path './_scripts/*' | sort); do
  agent_dir=$(dirname "$d")

  # Skip if this is a nested tests dir we already handled
  [[ -n "${tested_agents[$agent_dir]}" ]] && continue
  tested_agents[$agent_dir]=1

  total=$((total+1))

  # Check if tests dir has Python test files
  py_tests=$(find "$d" -maxdepth 1 -name "test_*.py" 2>/dev/null | head -1)
  # Check for TypeScript/JS test files
  ts_tests=$(find "$d" -maxdepth 1 \( -name "*.test.ts" -o -name "*.test.js" -o -name "*.spec.ts" -o -name "*.spec.js" \) 2>/dev/null | head -1)

  if [ -n "$py_tests" ]; then
    echo -n "\rTesting $agent_dir... "
    if (cd "$agent_dir" && python3 -m pytest tests/ -q --disable-warnings > /dev/null 2>&1); then
      passed=$((passed+1))
    else
      failed=$((failed+1))
      echo -e "\n❌ FAILED: $agent_dir"
    fi
  elif [ -n "$ts_tests" ]; then
    # TypeScript tests — try npx jest or npm test
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

  # Skip if already tested via tests/ subdir
  [[ -n "${tested_agents[$agent_dir]}" ]] && continue
  tested_agents[$agent_dir]=1

  total=$((total+1))
  echo -n "\rTesting $agent_dir (root test)... "
  if (cd "$agent_dir" && python3 -m pytest test_main.py -q --disable-warnings > /dev/null 2>&1); then
    passed=$((passed+1))
  else
    failed=$((failed+1))
    echo -e "\n❌ FAILED: $agent_dir"
  fi
done

echo -e "\r\033[K" # Clear the line
echo "====================================="
echo "Total tested : $total"
echo "✅ Passed    : $passed"
[ "$failed" -gt 0 ] && echo "❌ Failed    : $failed"
[ "$skipped" -gt 0 ] && echo "⏭️  Skipped   : $skipped"
echo "====================================="

if [ "$failed" -gt 0 ]; then
  exit 1
else
  echo "✅ All agents are passing!"
  exit 0
fi
