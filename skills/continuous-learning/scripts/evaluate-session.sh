#!/bin/bash
# evaluate-session.sh - Called by Claude Code Stop hook
# Evaluates session for extractable patterns and stages to pending

set -e

PENDING_FILE="${HOME}/.claude/pending-skills.md"
LOG_FILE="${HOME}/.claude/continuous-learning-log.md"
CONFIG_FILE="${HOME}/.claude/skills/continuous-learning/config.json"

# Default config
MIN_SESSION_LENGTH=10

# Load config if exists
if [ -f "$CONFIG_FILE" ]; then
    MIN_SESSION_LENGTH=$(jq -r '.min_session_length // 10' "$CONFIG_FILE" 2>/dev/null || echo 10)
fi

# Get session transcript from stdin (piped by Claude Code hook)
TRANSCRIPT=$(cat)

# Count messages (rough estimate by counting "Human:" and "Assistant:" markers)
MESSAGE_COUNT=$(echo "$TRANSCRIPT" | grep -c -E "^(Human|Assistant):" 2>/dev/null || echo 0)

# Skip short sessions
if [ "$MESSAGE_COUNT" -lt "$MIN_SESSION_LENGTH" ]; then
    exit 0
fi

# Create pending file if not exists
mkdir -p "$(dirname "$PENDING_FILE")"
touch "$PENDING_FILE"

# Log evaluation
echo "---" >> "$LOG_FILE"
echo "- date: $(date -Iseconds)" >> "$LOG_FILE"
echo "- messages: $MESSAGE_COUNT" >> "$LOG_FILE"

# Pattern detection markers to look for in transcript
# These indicate potentially extractable knowledge
PATTERNS=(
    "error.*fix"
    "bug.*solution"
    "workaround"
    "the issue was"
    "root cause"
    "不要.*用"
    "别.*用"
    "必须.*用"
    "always use"
    "never use"
    "don't use"
)

DETECTED=0
for pattern in "${PATTERNS[@]}"; do
    if echo "$TRANSCRIPT" | grep -qi "$pattern"; then
        DETECTED=1
        echo "- pattern_match: $pattern" >> "$LOG_FILE"
    fi
done

if [ "$DETECTED" -eq 1 ]; then
    echo "- status: patterns_detected" >> "$LOG_FILE"
    echo "[ContinuousLearning] Patterns detected. Run /learn to review." >&2
else
    echo "- status: no_patterns" >> "$LOG_FILE"
fi

exit 0
