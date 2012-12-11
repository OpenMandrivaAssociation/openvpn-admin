%define name openvpn-admin
%define version 1.9.4

%define Summary An openvpn GUI

Summary: 	%Summary
Name: 		%name
Version: 	%version
Release: 	%mkrel 7
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

Requires:      gksu
Requires:      gtk-sharp2
Requires:      mono
Requires:      openvpn

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

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

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



%changelog
* Mon Sep 14 2009 Thierry Vignaud <tvignaud@mandriva.com> 1.9.4-7mdv2010.0
+ Revision: 440446
- rebuild

* Mon Nov 03 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.9.4-6mdv2009.1
+ Revision: 299516
- Add requires for mono and gtk-sharp2 (#45425).

* Wed Jul 30 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.9.4-5mdv2009.0
+ Revision: 254895
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu Mar 13 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.9.4-3mdv2008.1
+ Revision: 187293
- Fixed openvpn-admin symlink in /usr/bin (#38808).
- Fixed openvpn-admin doesn't load on x86_64 (#38809).

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 02 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.9.4-2mdv2008.0
+ Revision: 94827
- Typo fix.

  + Emmanuel Andry <eandry@mandriva.org>
    - fix desktop file validation

  + Andreas Hasenack <andreas@mandriva.com>
    - fix pam config (#20882)
    - fix build with new gtk-sharp


* Wed Feb 28 2007 Jérôme Soyer <saispo@mandriva.org> 1.9.4-1mdv2007.0
+ Revision: 126944
- New release 1.9.4

* Wed Oct 18 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1.9.3-4mdv2007.0
+ Revision: 65806
- Fix Requires

* Tue Oct 17 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1.9.3-3mdv2006.0
+ Revision: 65658
- Add BuildRequires
- Add BuildRequires
- Migrate to XDG
- import openvpn-admin-1.9.3-2mdk

* Sun Apr 23 2006 Jerome Soyer <saispo@mandriva.org> 1.9.3-2mdk
- Readd the exe file
- Use %%{1}mdk

* Sun Apr 23 2006 Jerome Soyer <saispo@mandriva.org> 1.9.3-1mdk
- First build

