#!/bin/bash

TARGET_DIR="/usr/local/bin"
SCRIPTS_DIR="/opt/Scripts"

find "$SCRIPTS_DIR" -type f -name "*.py" -executable | while read -r script; do
    script_name=$(basename "$script" .py)
    symlink_path="$TARGET_DIR/$script_name"
    if [ -L "$symlink_path" ] || [ -e "$symlink_path" ]; then
        sudo rm -f "$symlink_path"
    fi
    sudo ln -s "$script" "$symlink_path"
done

echo "Done."
