%define name openvpn-admin
%define version 1.9.4

%define Summary An openvpn GUI

Summary: 	%Summary
Name: 		%name
Version: 	%version
Release: 	%mkrel 1
License: 	GPL
Group: 		Networking/Other
URL:		http://sourceforge.net/projects/openvpnadmin

Source:		http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:	%name-icons.tar.bz2
BuildRoot: 	%_tmppath/%{name}-%{version}-%{release}-buildroot

BuildRequires: gtk-sharp2
BuildRequires: mono
BuildRequires: gtk+2.0
BuildRequires: desktop-file-utils
BuildRequires: perl(XML::Parser)
BuildRequires: glade-sharp2

Requires:      openvpn
Requires:      gksu
%description
OpenVPN-Admin is a GUI for OpenVPN it is writen in Mono 
and runs under Linux and Windows.

%prep
%setup -q -a1

%build
%configure2_5x

%make WARN_CFLAGS=""

%install
rm -rf %buildroot

%makeinstall_std

%find_lang %name

# menu
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/%name << EOF
?package(%name): \
command="%_bindir/%name" \
needs="x11" \
icon="%name.png" \
section="System/Configuration/Networking" \
title="OpenVPN Admin" \
longtitle="%Summary" \
xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Network" \
  --add-category="Settings" \
  --add-category="X-MandrivaLinux-System-Configuration-Networking" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# icon
%__install -D -m 644 %{name}48.png %buildroot/%_liconsdir/%name.png
%__install -D -m 644 %{name}32.png %buildroot/%_iconsdir/%name.png
%__install -D -m 644 %{name}16.png %buildroot/%_miconsdir/%name.png

mkdir %buildroot/usr/bin
ln -s %buildroot/usr/sbin/%name %buildroot/usr/bin/%name

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(-,root,root)

%doc AUTHORS COPYING NEWS README TODO
%config(noreplace) /etc/pam.d/%name
%config(noreplace) /etc/security/console.apps/%name
%{_bindir}/%name
%{_sbindir}/%name
%{_datadir}/pixmaps/*
%{_datadir}/applications/%name.desktop
%{_libdir}/%name/%name.exe
%_menudir/%name
%_liconsdir/%name.png
%_miconsdir/%name.png
%_iconsdir/%name.png



