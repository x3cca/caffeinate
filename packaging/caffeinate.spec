%global debug_package %{nil}
%{!?caffeinate_version:%global caffeinate_version 0.1.0}

Name:           gnome-shell-extension-caffeinate
Version:        %{caffeinate_version}
Release:        1%{?dist}
Summary:        Keep GNOME awake, including on lid close and during agent turns

License:        GPL-2.0-or-later
URL:            https://github.com/x3cca/caffeinate
Source0:        caffeinate-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  glib2
BuildRequires:  systemd-rpm-macros
Requires:       bash
Requires:       glib2
Requires:       gnome-shell >= 45
Requires:       procps-ng
Requires:       python3
Requires:       systemd

%description
Caffeinate combines the Caffeine GNOME Shell extension with a systemd-logind
lid-switch inhibitor and a user-session watcher for local Codex and T3 Code
agent turns.

%prep
%autosetup -n caffeinate-%{version}

%build

%install
extension_dir="%{buildroot}%{_datadir}/gnome-shell/extensions/caffeinate@x3cca.github.com"
install -d "${extension_dir}/schemas"
install -m 0644 caffeine@patapon.info/extension.js "${extension_dir}/"
install -m 0644 caffeine@patapon.info/lidInhibitor.js "${extension_dir}/"
install -m 0644 caffeine@patapon.info/metadata.json "${extension_dir}/"
install -m 0644 caffeine@patapon.info/mprisMediaPlayer2.js "${extension_dir}/"
install -m 0644 caffeine@patapon.info/prefs.js "${extension_dir}/"
cp -a caffeine@patapon.info/icons "${extension_dir}/"
cp -a caffeine@patapon.info/preferences "${extension_dir}/"
install -m 0644 caffeine@patapon.info/schemas/*.xml "${extension_dir}/schemas/"
glib-compile-schemas "${extension_dir}/schemas"

for po_file in caffeine@patapon.info/locale/*.po; do
    language=$(basename "${po_file}" .po)
    locale_dir="${extension_dir}/locale/${language}/LC_MESSAGES"
    install -d "${locale_dir}"
    msgfmt "${po_file}" -o "${locale_dir}/gnome-shell-extension-caffeine.mo"
done

install -Dpm 0755 watcher/caffeinate-watch \
    "%{buildroot}%{_libexecdir}/caffeinate/caffeinate-watch"
install -Dpm 0644 watcher/caffeinate-watch.service \
    "%{buildroot}%{_userunitdir}/caffeinate-watch.service"
sed -i 's|%h/.local/libexec/caffeinate-watch|%{_libexecdir}/caffeinate/caffeinate-watch|' \
    "%{buildroot}%{_userunitdir}/caffeinate-watch.service"

%post
%systemd_user_post caffeinate-watch.service

%preun
%systemd_user_preun caffeinate-watch.service

%postun
%systemd_user_postun_with_restart caffeinate-watch.service

%files
%license COPYING
%doc README.md
%{_datadir}/gnome-shell/extensions/caffeinate@x3cca.github.com/
%{_libexecdir}/caffeinate/
%{_userunitdir}/caffeinate-watch.service

%changelog
* Sun Sep 13 2026 x3cca <10494276+x3cca@users.noreply.github.com> - 0.1.0-1
- Initial Caffeinate package
