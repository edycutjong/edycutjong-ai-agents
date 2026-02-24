#!/bin/bash
passed=0
failed=0

echo "Testing all agents..."
for d in $(find . -maxdepth 4 -type d -name "tests"); do
  agent_dir=$(dirname "$d")
  echo -n "\rTesting $agent_dir... "
  if (cd "$agent_dir" && python3 -m pytest tests/ -q --disable-warnings > /dev/null 2>&1); then
    passed=$((passed+1))
  else
    failed=$((failed+1))
    echo -e "\n❌ FAILED: $agent_dir"
  fi
done

echo -e "\r\033[K" # Clear the line
echo "====================================="
echo "Total passed: $passed / $((passed+failed))"
if [ "$failed" -gt 0 ]; then
  echo "Total failed: $failed"
  exit 1
else
  echo "✅ All agents are passing!"
  exit 0
fi
