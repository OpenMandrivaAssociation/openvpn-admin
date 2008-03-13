%define name openvpn-admin
%define version 1.9.4

%define Summary An openvpn GUI

Summary: 	%Summary
Name: 		%name
Version: 	%version
Release: 	%mkrel 3
License: 	GPL
Group: 		Networking/Other
URL:		http://sourceforge.net/projects/openvpn-admin

Source:		http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:	%name-icons.tar.bz2
Patch:          openvpn-admin-1.9.4-pam.patch
# http://openvpn-admin.svn.sourceforge.net/viewvc/openvpn-admin?view=rev&revision=160
Patch1:         openvpn-admin-1.9.4-newsharpbuild.patch
# http://qa.mandriva.com/show_bug.cgi?id=38809
Patch2:		openvpn-admin-1.9.4-fix-exe-x86_64.patch
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
%patch -p1
%patch1 -p2
%patch2 -p1

%build
%configure2_5x

%make WARN_CFLAGS=""

%install
rm -rf %buildroot

%makeinstall_std

%find_lang %name

#fix icon path in desktop file
sed '/Icon/d' %{buildroot}%{_datadir}/applications/%{name}.desktop  > %{buildroot}%{_datadir}/applications/temp.desktop
sed '/^Exec/a Icon=openvpn-admin' %{buildroot}%{_datadir}/applications/temp.desktop > %{buildroot}%{_datadir}/applications/%{name}.desktop
rm -f %{buildroot}%{_datadir}/applications/temp.desktop


desktop-file-install --vendor="" \
  --remove-key="Version" \
  --remove-category="Application" \
  --add-category="Network" \
  --add-category="Settings" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# icon
%__install -D -m 644 %{name}48.png %buildroot/%_liconsdir/%name.png
%__install -D -m 644 %{name}32.png %buildroot/%_iconsdir/%name.png
%__install -D -m 644 %{name}16.png %buildroot/%_miconsdir/%name.png

mkdir %buildroot/usr/bin
ln -s /usr/sbin/%name %buildroot/usr/bin/%name

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
%_liconsdir/%name.png
%_miconsdir/%name.png
%_iconsdir/%name.png

