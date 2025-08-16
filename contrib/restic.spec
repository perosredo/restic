Name: restic
Version: 0.18.0
Release: 1%{?dist}
Summary: Fast, secure, efficient backup program

%global debug_package %{nil}

Group: Applications/Archiving
License: BSD-2-Clause
URL: https://restic.net/
Source0: https://github.com/restic/restic/releases/download/v%{version}/restic-%{version}.tar.gz

BuildRequires: golang >= 1.23
BuildRequires: make
BuildRequires: git
Requires: /bin/bash

%description
restic is a backup program that is fast, efficient and secure. It supports
the three major operating systems (Linux, macOS, Windows) and a few more.
Restic is a single executable that you can use to backup and restore your
files from/to the cloud.

Design goals:
- Easy: Doing backups should be a frictionless process, otherwise you are
  tempted to skip it.
- Fast: Backing up your data with restic should only be limited by your
  network or hard disk bandwidth.
- Verifiable: Much more important than backup is restore, so restic enables
  you to easily verify that all data can be restored.
- Secure: Restic uses cryptography to guarantee confidentiality and integrity
  of your data.
- Efficient: With the growth of data, additional snapshots should only take
  the storage of the actual increment.
- Free: restic is free software and licensed under the BSD 2-Clause License.

%prep
%setup -q

%build
export CGO_ENABLED=0
export GOOS=linux
%ifarch x86_64
export GOARCH=amd64
%endif
%ifarch aarch64
export GOARCH=arm64
%endif
%ifarch i386 i686
export GOARCH=386
%endif
go run build.go --enable-pie -v

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datarootdir}/zsh/site-functions
mkdir -p %{buildroot}%{_datarootdir}/fish/vendor_completions.d
mkdir -p %{buildroot}%{_datarootdir}/bash-completion/completions

# Install binary
install -p -m 755 restic %{buildroot}%{_bindir}/restic

# Generate and install man pages
%{buildroot}%{_bindir}/restic generate --man %{buildroot}%{_mandir}/man1/

# Generate and install shell completions
%{buildroot}%{_bindir}/restic generate --bash-completion %{buildroot}%{_datarootdir}/bash-completion/completions/restic
%{buildroot}%{_bindir}/restic generate --zsh-completion %{buildroot}%{_datarootdir}/zsh/site-functions/_restic
%{buildroot}%{_bindir}/restic generate --fish-completion %{buildroot}%{_datarootdir}/fish/vendor_completions.d/restic.fish

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/restic
%{_mandir}/man1/restic*.1*
%{_datarootdir}/bash-completion/completions/restic
%{_datarootdir}/zsh/site-functions/_restic
%{_datarootdir}/fish/vendor_completions.d/restic.fish

%changelog
* Fri Aug 16 2024 Petar Sredojevic <petar@sredojevic.ca> - 0.18.0-1
- Adapted for AlmaLinux 10/RHEL 10 from upstream contrib/restic.spec
- Updated to restic 0.18.0 (latest release)
- Build configuration and packaging setup by Claude Code
- Updated Go requirement to 1.23+ as per upstream requirements