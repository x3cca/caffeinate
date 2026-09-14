# Caffeinate

Caffeinate combines [Caffeine](https://github.com/eonpatapon/gnome-shell-extension-caffeine)
with the lid-switch inhibitor pattern from
[Ignore Lid](https://github.com/mfloto/ignore-lid). One coffee toggle now prevents
screen blanking, automatic suspend, and suspend on lid close.

It also includes an optional user service that watches for active local Codex CLI
or T3 Code agent turns. Agent activity is tracked as its own inhibition reason,
so it does not overwrite your manual coffee-toggle state.

## Install

Requirements: GNOME Shell 45–51, systemd-logind, Bash, Python 3, and `make`.

```sh
git clone https://github.com/x3cca/caffeinate.git
cd caffeinate
./install.sh
```

The installer disables the separate Caffeine and Ignore Lid extensions after
Caffeinate has been installed. A newly installed extension may require signing
out and back in before GNOME discovers it; the watcher holds a direct fallback
inhibitor until then, and whenever the extension is unavailable.

## Updating from Caffeine

The project preserves Caffeine's Git history and layout. The original repository
is configured as the `upstream` remote:

```sh
git fetch upstream
git merge upstream/master
```

The integration is intentionally small: a separate `lidInhibitor.js` module,
a few hooks in `extension.js`, one schema key for the watcher, and packaging
metadata. This keeps upstream merges predictable.

## Credits and license

Caffeinate is based on Caffeine by eonpatapon and contributors. Lid-switch logic
is derived from Ignore Lid by mfloto. All three projects are licensed under GPL-2.0.
