#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	Ripping and encoding DVD into AVI/OGM files
Summary(pl.UTF-8):	Zgrywanie i kodowanie DVD do plików AVI/OGM
Name:		ogmrip
Version:	1.0.1
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Applications
Source0:	https://downloads.sourceforge.net/ogmrip/%{name}-%{version}.tar.gz
# Source0-md5:	2c9dbb32c9615ebec05e0104c5becefd
URL:		https://ogmrip.sourceforge.net/en/index.html
BuildRequires:	GConf2-devel >= 2.6.0
BuildRequires:	dbus-glib-devel >= 0.7.2
BuildRequires:	enca-devel
BuildRequires:	enchant-devel >= 1.1.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	hal-devel >= 0.5.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libdvdread-devel >= 0.9.7
BuildRequires:	libglade2-devel >= 1:2.5.0
BuildRequires:	libgnomeui-devel >= 2.6.0
BuildRequires:	libnotify-devel >= 0.7
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtheora-devel >= 1.0-0.alpha5
BuildRequires:	libtiff-devel
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.198
# GNU sed
BuildRequires:	sed
BuildRequires:	which
BuildRequires:	zlib-devel
Requires(post,preun):	GConf2 >= 2.6.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-glib >= 0.7.2
Requires:	eject
Requires:	enchant >= 1.1.0
Requires:	lame >= 3.96
Requires:	libnotify >= 0.7
Requires:	libtheora >= 1.0-0.alpha5
Requires:	mencoder
Requires:	mplayer >= 3:1.0-3.rc1
Requires:	ogmtools >= 1.0
Requires:	vorbis-tools >= 1:1.0
Suggests:	tesseract
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OGMRip is an application and a set of libraries for ripping and
encoding DVD into AVI/OGM files using a wide variety of codecs. It
relies on mplayer, mencoder, ogmtools, oggenc and lame to perform its
tasks.

Features:
- transcodes from DVD or files
- outputs ogm, avi or matroska files
- provides a lot of codecs (ogg vorbis, mp3, pcm, ac3, xvid, lavc)
- calculates video bitrate for a given filesize
- calculates cropping parameters and scaling factors
- uses maximum quality codec switches
- supports subtitles extraction
- rips contiguous chapters

%description -l pl.UTF-8
OGMRip jest aplikacją i zestawem bibliotek służącymi do zgrywania i
kodowania DVD do plików AVI/OGM przy użyciu wielu różnych kodeków. Do
wykonywania zadań używa mplayera, mencodera, ogmtools, oggenc i lame.

Cechy:
- przekodowuje z DVD lub plików,
- na wyjściu daje pliki ogm, avi lub matroska,
- umożliwia używanie wielu kodeków (ogg vorbis, mp3, pcm, ac3, xvid,
  lavc),
- oblicza tempo bitowe dla danego rozmiaru pliku,
- oblicza parametry obcinania i skalowania,
- używa kodeków z ustawionymi parametrami maksymalnej jakości,
- wspiera wydobycie napisów,
- zgrywa ciągłe rozdziały.

%package libs
Summary:	OGMRip libraries
Summary(pl.UTF-8):	Biblioteki OGMRip
Group:		Libraries
Requires:	GConf2-libs >= 2.6.0
Requires:	glib2 >= 1:2.16.0
Requires:	gtk+2 >= 2:2.12.0
Requires:	libdvdread >= 0.9.7
Requires:	libglade2 >= 1:2.5.0

%description libs
OGMRip libraries.

%description libs -l pl.UTF-8
Biblioteki OGMRip.

%package devel
Summary:	OGMRip header files
Summary(pl.UTF-8):	Pliki nagłówkowe OGMRip
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	GConf2-devel >= 2.6.0
Requires:	glib2-devel >= 1:2.16.0
Requires:	gtk+2-devel >= 2:2.12.0
Requires:	libdvdread-devel >= 0.9.7
Requires:	libglade2-devel >= 1:2.5.0

%description devel
OGMRip header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe OGMRip.

%package static
Summary:	Static OGMRip libraries
Summary(pl.UTF-8):	Statyczne biblioteki OGMRip
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OGMRip libraries.

%description static -l pl.UTF-8
Statyczne biblioteki OGMRip.

%prep
%setup -q

%build
%configure \
	MENCODER_PROG=%{_bindir}/mencoder \
	MPLAYER_PROG=%{_bindir}/mplayer \
	--disable-schemas-install \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# broken install dependecies (/usr/bin/ld: cannot find -logmrip-mplayer)
%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/{audio,container,options,subp,video}-plugins/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/{audio,container,options,subp,video}-plugins/*.a
%endif

# wrong location?
%{__mv} $RPM_BUILD_ROOT%{_libdir}/ogmrip/video-plugins/ogmrip-*.h $RPM_BUILD_ROOT%{_includedir}/ogmrip

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install ogmrip.schemas

%preun
%gconf_schema_uninstall ogmrip.schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/avibox
%attr(755,root,root) %{_bindir}/dvdcpy
%attr(755,root,root) %{_bindir}/ogmrip
%attr(755,root,root) %{_bindir}/subp2pgm
%attr(755,root,root) %{_bindir}/subp2png
%attr(755,root,root) %{_bindir}/subp2tiff
%attr(755,root,root) %{_bindir}/subptools
%attr(755,root,root) %{_bindir}/theoraenc
%{_sysconfdir}/gconf/schemas/ogmrip.schemas
%{_desktopdir}/ogmrip.desktop
%{_pixmapsdir}/ogmrip.png
%{_datadir}/%{name}
%{_mandir}/man1/avibox.1*
%{_mandir}/man1/dvdcpy.1*
%{_mandir}/man1/subp2pgm.1*
%{_mandir}/man1/subptools.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libogmdvd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmdvd.so.1
%attr(755,root,root) %{_libdir}/libogmdvd-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmdvd-gtk.so.1
%attr(755,root,root) %{_libdir}/libogmjob.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmjob.so.1
%attr(755,root,root) %{_libdir}/libogmrip.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmrip.so.1
%attr(755,root,root) %{_libdir}/libogmrip-lavc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmrip-lavc.so.1
%attr(755,root,root) %{_libdir}/libogmrip-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmrip-gtk.so.1
%attr(755,root,root) %{_libdir}/libogmrip-mplayer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmrip-mplayer.so.1
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/audio-plugins
%attr(755,root,root) %{_libdir}/%{name}/audio-plugins/*.so
%dir  %{_libdir}/%{name}/container-plugins
%attr(755,root,root) %{_libdir}/%{name}/container-plugins/*.so
%dir %{_libdir}/%{name}/options-plugins
%attr(755,root,root) %{_libdir}/%{name}/options-plugins/*.so
%dir %{_libdir}/%{name}/subp-plugins
%attr(755,root,root) %{_libdir}/%{name}/subp-plugins/*.so
%dir %{_libdir}/%{name}/video-plugins
%attr(755,root,root) %{_libdir}/%{name}/video-plugins/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libogmdvd.so
%attr(755,root,root) %{_libdir}/libogmdvd-gtk.so
%attr(755,root,root) %{_libdir}/libogmjob.so
%attr(755,root,root) %{_libdir}/libogmrip.so
%attr(755,root,root) %{_libdir}/libogmrip-gtk.so
%attr(755,root,root) %{_libdir}/libogmrip-lavc.so
%attr(755,root,root) %{_libdir}/libogmrip-mplayer.so
%{_libdir}/libogmdvd.la
%{_libdir}/libogmdvd-gtk.la
%{_libdir}/libogmjob.la
%{_libdir}/libogmrip.la
%{_libdir}/libogmrip-gtk.la
%{_libdir}/libogmrip-lavc.la
%{_libdir}/libogmrip-mplayer.la
%{_includedir}/ogmdvd
%{_includedir}/ogmjob
%{_includedir}/ogmrip
%{_pkgconfigdir}/ogmdvd.pc
%{_pkgconfigdir}/ogmdvd-gtk.pc
%{_pkgconfigdir}/ogmjob.pc
%{_pkgconfigdir}/ogmrip.pc
%{_pkgconfigdir}/ogmrip-gtk.pc
%{_gtkdocdir}/ogmdvd
%{_gtkdocdir}/ogmdvd-gtk
%{_gtkdocdir}/ogmjob
%{_gtkdocdir}/ogmrip
%{_gtkdocdir}/ogmrip-gtk

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libogmdvd.a
%{_libdir}/libogmdvd-gtk.a
%{_libdir}/libogmjob.a
%{_libdir}/libogmrip.a
%{_libdir}/libogmrip-gtk.a
%{_libdir}/libogmrip-lavc.a
%{_libdir}/libogmrip-mplayer.a
%endif
