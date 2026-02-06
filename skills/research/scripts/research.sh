#!/bin/bash
# Tavily Research API script with async polling support
# Usage: ./research.sh '{"input": "your research query", ...}' [output_file]
# Example: ./research.sh '{"input": "quantum computing trends", "model": "pro"}' results.md

set -e

JSON_INPUT="$1"
OUTPUT_FILE="$2"
POLL_INTERVAL="${POLL_INTERVAL:-5}"
MAX_WAIT="${MAX_WAIT:-180}"

if [ -z "$JSON_INPUT" ]; then
    echo "Usage: ./research.sh '<json>' [output_file]"
    echo ""
    echo "Required:"
    echo "  input: string - The research topic or question"
    echo ""
    echo "Optional:"
    echo "  model: \"mini\", \"pro\", \"auto\" (default)"
    echo "    - mini: Targeted, efficient research for narrow questions"
    echo "    - pro: Comprehensive, multi-agent research for complex topics"
    echo "    - auto: Automatically selects based on query complexity"
    echo "  citation_format: \"numbered\" (default), \"mla\", \"apa\", \"chicago\""
    echo "  output_schema: JSON Schema object for structured output"
    echo ""
    echo "Arguments:"
    echo "  output_file: optional file to save results"
    echo ""
    echo "Environment variables:"
    echo "  POLL_INTERVAL: seconds between polling (default: 5)"
    echo "  MAX_WAIT: max seconds to wait for results (default: 180)"
    echo ""
    echo "Example:"
    echo "  ./research.sh '{\"input\": \"AI agent frameworks comparison\", \"model\": \"pro\"}' report.md"
    exit 1
fi

if [ -z "$TAVILY_API_KEY" ]; then
    echo "Error: TAVILY_API_KEY environment variable not set"
    exit 1
fi

# Validate JSON
if ! echo "$JSON_INPUT" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input"
    exit 1
fi

# Check for required input field
if ! echo "$JSON_INPUT" | jq -e '.input' >/dev/null 2>&1; then
    echo "Error: 'input' field is required"
    exit 1
fi

# Add citation format default if not specified, disable streaming for token management
JSON_INPUT=$(echo "$JSON_INPUT" | jq '
    . + {stream: false} |
    if .citation_format == null then . + {citation_format: "numbered"} else . end
')

INPUT=$(echo "$JSON_INPUT" | jq -r '.input')
MODEL=$(echo "$JSON_INPUT" | jq -r '.model // "auto"')

echo "Researching: $INPUT (model: $MODEL)"
echo "This may take 30-120 seconds..."

# Submit research request
RESPONSE=$(curl -sN --connect-timeout 30 --max-time 120 --request POST \
    --url https://api.tavily.com/research \
    --header "Authorization: Bearer $TAVILY_API_KEY" \
    --header 'Content-Type: application/json' \
    --header 'x-client-source: claude-code-skill' \
    --data "$JSON_INPUT" 2>&1)

# Check if response contains request_id (async mode)
REQUEST_ID=$(echo "$RESPONSE" | jq -r '.request_id // empty')
STATUS=$(echo "$RESPONSE" | jq -r '.status // empty')

if [ -z "$REQUEST_ID" ]; then
    # Sync response or error
    if echo "$RESPONSE" | jq -e '.content' >/dev/null 2>&1; then
        # Already have content
        FINAL_RESPONSE="$RESPONSE"
    else
        echo "Error: Unexpected response format"
        echo "$RESPONSE"
        exit 1
    fi
else
    # Async mode - poll for results
    echo "Request ID: $REQUEST_ID"
    ELAPSED=0

    while [ "$STATUS" != "completed" ] && [ $ELAPSED -lt $MAX_WAIT ]; do
        sleep $POLL_INTERVAL
        ELAPSED=$((ELAPSED + POLL_INTERVAL))

        RESPONSE=$(curl -s --max-time 30 --request GET \
            --url "https://api.tavily.com/research/$REQUEST_ID" \
            --header "Authorization: Bearer $TAVILY_API_KEY" 2>&1)

        STATUS=$(echo "$RESPONSE" | jq -r '.status // empty')

        case "$STATUS" in
            "completed")
                echo "Research completed in ${ELAPSED}s"
                FINAL_RESPONSE="$RESPONSE"
                ;;
            "in_progress"|"pending")
                echo "Status: $STATUS (${ELAPSED}s elapsed)..."
                ;;
            "failed")
                echo "Error: Research failed"
                echo "$RESPONSE" | jq -r '.error // .message // "Unknown error"'
                exit 1
                ;;
            *)
                echo "Warning: Unknown status '$STATUS'"
                ;;
        esac
    done

    if [ "$STATUS" != "completed" ]; then
        echo "Error: Timeout after ${MAX_WAIT}s waiting for results"
        exit 1
    fi
fi

# Output results
if [ -n "$OUTPUT_FILE" ]; then
    # Always save full JSON response
    BASE_NAME="${OUTPUT_FILE%.md}"
    BASE_NAME="${BASE_NAME%.json}"
    JSON_FILE="${BASE_NAME}.json"
    echo "$FINAL_RESPONSE" > "$JSON_FILE"
    echo "Full JSON response saved to: $JSON_FILE"

    # Also create a markdown file with content
    MD_FILE="${BASE_NAME}.md"
    if [ "$MD_FILE" != "$JSON_FILE" ]; then
        echo "$FINAL_RESPONSE" | jq -r '.content // empty' > "$MD_FILE"
        echo "Markdown content saved to: $MD_FILE"
    fi
else
    # Print content to stdout
    CONTENT=$(echo "$FINAL_RESPONSE" | jq -r '.content // empty')
    if [ -n "$CONTENT" ]; then
        echo ""
        echo "========== RESEARCH RESULTS =========="
        echo "$CONTENT"
        echo ""
        echo "========== SOURCES =========="
        echo "$FINAL_RESPONSE" | jq -r '.sources[]? | "[\(.title // "No title")](\(.url))"'
    else
        echo "$FINAL_RESPONSE"
    fi
fi
