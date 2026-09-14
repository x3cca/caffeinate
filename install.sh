#!/usr/bin/env bash

set -euo pipefail

readonly PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly UUID="caffeinate@x3cca.github.com"

stage_extension_state() {
    local schema key updated

    schema="$1"
    key="$2"
    updated=$(gsettings get "${schema}" "${key}" | python3 -c '
import ast
import sys

values = ast.literal_eval(sys.stdin.read())
remove = {"caffeine@patapon.info", "ignore-lid@gnome-extensions.mfloto.com", "caffeinate@x3cca.github.com"}
values = [value for value in values if value not in remove]
if sys.argv[1] == "enabled-extensions":
    values.append("caffeinate@x3cca.github.com")
print(repr(values))
' "${key}")
    gsettings set "${schema}" "${key}" "${updated}"
}

make -C "${PROJECT_DIR}" build
gnome-extensions install "${PROJECT_DIR}/${UUID}.zip" --force

install -Dm755 "${PROJECT_DIR}/watcher/caffeinate-watch" \
    "${HOME}/.local/libexec/caffeinate-watch"
install -Dm644 "${PROJECT_DIR}/watcher/caffeinate-watch.service" \
    "${HOME}/.config/systemd/user/caffeinate-watch.service"

systemctl --user daemon-reload
systemctl --user enable caffeinate-watch.service
systemctl --user restart caffeinate-watch.service

gnome-extensions disable caffeine@patapon.info 2>/dev/null || true
gnome-extensions disable ignore-lid@gnome-extensions.mfloto.com 2>/dev/null || true
stage_extension_state org.gnome.shell enabled-extensions
stage_extension_state org.gnome.shell disabled-extensions

if gnome-extensions enable "${UUID}" 2>/dev/null; then
    printf 'Caffeinate installed and enabled.\n'
else
    printf 'Caffeinate installed and staged; it will activate at the next GNOME sign-in.\n'
fi
