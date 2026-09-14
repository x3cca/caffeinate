# Automated upstream maintenance

This repository is a small downstream of Caffeine. Keep its original Git
history intact and fetch upstream only through the read-only `upstream` remote.
Never force-push or rewrite published history.

For a scheduled upstream-sync run:

1. Fetch `upstream` and compare `main` with `upstream/master`. If there are no
   new upstream commits, make no changes and report that the repository is
   current.
2. Merge `upstream/master` into `main`. Preserve the Caffeinate-specific seams:
   `lidInhibitor.js`, the integration hooks in `extension.js`, the
   `agent-enabled` schema key, `watcher/`, and `packaging/`.
3. Run `npm install --no-package-lock --ignore-scripts`, `make lint`,
   `bash -n install.sh watcher/caffeinate-watch`,
   `glib-compile-schemas --strict --dry-run caffeine@patapon.info/schemas`, and
   `make clean build`. Stop without publishing if any check fails or a merge
   conflict cannot be resolved confidently.
4. Increment the patch component in `VERSION`. Set `version-name` in
   `caffeine@patapon.info/metadata.json` and the fallback
   `caffeinate_version` in `packaging/caffeinate.spec` to the same value. Add a
   dated RPM changelog entry describing the upstream sync.
5. Commit the tested merge and release metadata, create the annotated tag
   `v<VERSION>`, then push `main` and that tag to `origin`. Do not create a tag
   when no upstream changes were merged.

The version tag is the publishing handoff. `.github/workflows/release.yml`
builds and signs the extension and RPM, creates the GitHub Release, and deploys
the signed DNF repository. After pushing, wait for the tag workflow and report
its URL and final status. Do not expose, replace, or export the RPM private key.
