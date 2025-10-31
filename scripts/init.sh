set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_FILE="$PROJECT_ROOT/.env.template"
OUTPUT_FILE="$PROJECT_ROOT/.env"
VENV_DIR="$PROJECT_ROOT/.venv"

if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "Template file '$TEMPLATE_FILE' not found!"
  exit 1
fi

# Use /dev/tty for interactive input
TTY_INPUT="/dev/tty"
if [[ ! -t 0 && -r /dev/tty ]]; then
  INPUT_SOURCE="/dev/tty"
else
  INPUT_SOURCE="/dev/stdin"
fi

> "$OUTPUT_FILE"

echo "Generating $OUTPUT_FILE from $TEMPLATE_FILE..."
echo

while IFS= read -r line || [[ -n "$line" ]]; do
  if [[ -z "$line" || "$line" =~ ^# ]]; then
    echo "$line" >> "$OUTPUT_FILE"
    continue
  fi

  key=$(echo "$line" | cut -d'=' -f1)
  value=$(echo "$line" | cut -d'=' -f2- | tr -d '"')

  if [[ "$value" == "PLACEHOLDER" ]]; then
    # Read from the real terminal if possible
    if [[ -r "$TTY_INPUT" ]]; then
      echo -n "Enter value for $key: " > "$TTY_INPUT"
      read -s user_value < "$TTY_INPUT" || user_value=""
      echo > "$TTY_INPUT"
    else
      read -s -p "Enter value for $key: " user_value || true
      echo
    fi

    if [[ -z "${user_value:-}" ]]; then
      echo "No value entered for $key, leaving empty."
      user_value=""
    fi

    echo "$key=\"$user_value\"" >> "$OUTPUT_FILE"
  else
    echo "$line" >> "$OUTPUT_FILE"
  fi
done < "$TEMPLATE_FILE"

echo
echo ".env file created successfully!"

echo
echo "Checking for uv installation..."

if ! command -v uv &> /dev/null; then
  echo "'uv' not found — installing it now..."
  # Install uv using the official bootstrap script
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
else
  echo "uv is already installed."
fi

# --- Step 3: Run uv sync if needed ---------------------------------------------

if [[ ! -d "$VENV_DIR" ]]; then
  echo
  echo "Python environment not found — running 'uv sync'..."
  uv sync
  echo "uv sync complete."
else
  echo
  echo "Python environment already synchronized — skipping uv sync."
fi

echo
echo "Environment initialization complete!"
exit 0