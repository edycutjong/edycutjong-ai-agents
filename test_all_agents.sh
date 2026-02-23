#!/bin/bash
passed=0
failed=0
echo "Testing all agents..."
for d in $(find . -maxdepth 3 -type d -name "tests"); do
  agent_dir=$(dirname "$d")
  if (cd "$agent_dir" && python3 -m pytest tests/ -q --disable-warnings > /dev/null 2>&1); then
    passed=$((passed+1))
    echo "✅ $agent_dir"
  else
    failed=$((failed+1))
    echo "❌ FAILED: $agent_dir"
  fi
done
echo ""
echo "Total passed: $passed"
echo "Total failed: $failed"
