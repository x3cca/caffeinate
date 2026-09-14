# Caffeinate

Caffeinate combines [Caffeine](https://github.com/eonpatapon/gnome-shell-extension-caffeine)
with the lid-switch inhibitor pattern from
[Ignore Lid](https://github.com/mfloto/ignore-lid). One coffee toggle now prevents
screen blanking, automatic suspend, and suspend on lid close.

It also includes an optional user service that watches for active local Codex CLI
or T3 Code agent turns. Agent activity is tracked as its own inhibition reason,
so it does not overwrite your manual coffee-toggle state.

## Install from the signed Fedora repository

This is the recommended installation on Fedora. It updates the extension and
watcher together through normal DNF transactions, without an
extensions.gnome.org or COPR account.

```sh
sudo dnf config-manager addrepo \
  --from-repofile=https://x3cca.github.io/caffeinate/caffeinate.repo
sudo dnf install gnome-shell-extension-caffeinate
systemctl --user enable --now caffeinate-watch.service
```

Updates then arrive with the rest of the system through `dnf upgrade` or GNOME
Software. GNOME Shell may require one sign-out after extension code changes.

For development installs from a checkout, run `./install.sh`. The local installer
disables the separate Caffeine and Ignore Lid extensions and installs into the
current user's home directory.

## Releases

Set `VERSION` and `version-name` in `metadata.json` to the same semantic version,
commit the change, and push a matching tag such as `v0.2.0`. GitHub Actions then:

1. lints and tests the extension and watcher;
2. builds and signs the binary and source RPMs;
3. creates the GitHub Release with checksums and extension ZIP;
4. publishes signed DNF metadata to GitHub Pages.

The signing public key is committed under `packaging/`; the private key exists
only in the `RPM_SIGNING_KEY` GitHub Actions secret and the maintainer's protected
local keyring.

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
