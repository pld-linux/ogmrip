#
# Conditional build:
%bcond_without	matroska	# don't build with matroska support
#
Summary:	Ripping and encoding DVD into AVI/OGM files
Summary(pl.UTF-8):	Zgrywanie i kodowanie DVD do plików AVI/OGM
Name:		ogmrip
Version:	0.11.1
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/ogmrip/%{name}-%{version}.tar.gz
# Source0-md5:	432991f4502ebba8fee51b527ef5b6af
BuildRequires:	GConf2-devel >= 2.6.0
BuildRequires:	dbus-glib-devel >= 0.3.0
BuildRequires:	enca-devel
BuildRequires:	enchant-devel >= 1.1.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	gtk+2-devel >= 2:2.10.0
BuildRequires:	hal-devel >= 0.5.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libdvdread-devel >= 0.9.7
BuildRequires:	libglade2-devel >= 1:2.5.0
BuildRequires:	libgnomeui-devel >= 2.6.0
BuildRequires:	libnotify-devel >= 0.4.3
BuildRequires:	libstdc++-devel
BuildRequires:	libtheora-devel >= 1.0-0.alpha5
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig
# TODO: remove configure checks (just assume support for everything, mkvtoolnix 2.x)
BuildRequires:	mencoder >= 3:1.0-3.rc1
%{?with_matroska:BuildRequires:	mkvtoolnix >= 2}
Requires(post,preun):	GConf2 >= 2.6.0
Requires:	eject
Requires:	gocr >= 0.39
Requires:	lame >= 3.96
%{?with_matroska:Requires:	mkvtoolnix >= 2}
Requires:	mplayer >= 3:1.0-3.rc1
Requires:	mencoder
Requires:	ogmtools >= 1.0
Requires:	vorbis-tools >= 1:1.0
Requires:	%{name}-libs = %{version}-%{release}
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
Summary:	%{name} libraries
Summary(pl.UTF-8):	Biblioteki %{name}
Group:		Libraries

%description libs
%{name} libraries.

%description libs -l pl.UTF-8
Biblioteki %{name}.

%package devel
Summary:	%{name} header files
Summary(pl.UTF-8):	Pliki nagłówkowe %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
%{name} header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe %{name}.

%package static
Summary:	Static %{name} libraries
Summary(pl.UTF-8):	Statyczne biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} libraries.

%description static -l pl.UTF-8
Statyczne biblioteki %{name}.

%prep
%setup -q

%build
%configure \
	EJECT_PROG=/usr/bin/eject \
	FAAC_PROG=/usr/bin/faac \
	GOCR_PROG=/usr/bin/gocr \
	LAME_PROG=/usr/bin/lame \
	MENCODER_PROG=/usr/bin/mencoder \
	MKVMERGE_PROG=/usr/bin/mkvmerge \
	MPLAYER_PROG=/usr/bin/mplayer \
	OCRAD_PROG=/usr/bin/ocrad \
	OGGENC_PROG=/usr/bin/oggenc \
	OGMMERGE_PROG=/usr/bin/ogmmerge \
	OGMSPLIT_PROG=/usr/bin/ogmsplit \
	--disable-schemas-install \
	--with-html-dir=%{_gtkdocdir} \
	--with-mplayer-version=1.0rc1
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# broken install dependecies (/usr/bin/ld: cannot find -logmrip-mplayer)
%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/{audio-codecs,containers,subp-codecs,video-codecs}/*.{la,a}

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
%attr(755,root,root) %{_bindir}/dvdcpy
%attr(755,root,root) %{_bindir}/ogmrip
%attr(755,root,root) %{_bindir}/srtutil
%attr(755,root,root) %{_bindir}/subp2pgm
%attr(755,root,root) %{_bindir}/theoraenc
%{_sysconfdir}/gconf/schemas/ogmrip.schemas
%{_desktopdir}/ogmrip.desktop
%{_pixmapsdir}/ogmrip.png
%{_datadir}/%{name}
%{_mandir}/man1/dvdcpy.1*
%{_mandir}/man1/srtutil.1*
%{_mandir}/man1/subp2pgm.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libogmdvd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmdvd.so.0
%attr(755,root,root) %{_libdir}/libogmdvd-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmdvd-gtk.so.0
%attr(755,root,root) %{_libdir}/libogmjob.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmjob.so.0
%attr(755,root,root) %{_libdir}/libogmrip.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmrip.so.0
%attr(755,root,root) %{_libdir}/libogmrip-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmrip-gtk.so.0
%attr(755,root,root) %{_libdir}/libogmrip-mplayer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libogmrip-mplayer.so.0
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/audio-codecs
%attr(755,root,root) %{_libdir}/%{name}/audio-codecs/*.so
%dir  %{_libdir}/%{name}/containers
%attr(755,root,root) %{_libdir}/%{name}/containers/*.so
%dir %{_libdir}/%{name}/subp-codecs
%attr(755,root,root) %{_libdir}/%{name}/subp-codecs/*.so
%dir %{_libdir}/%{name}/video-codecs
%attr(755,root,root) %{_libdir}/%{name}/video-codecs/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libogmdvd.so
%attr(755,root,root) %{_libdir}/libogmdvd-gtk.so
%attr(755,root,root) %{_libdir}/libogmjob.so
%attr(755,root,root) %{_libdir}/libogmrip.so
%attr(755,root,root) %{_libdir}/libogmrip-gtk.so
%attr(755,root,root) %{_libdir}/libogmrip-mplayer.so
%{_libdir}/libogmdvd.la
%{_libdir}/libogmdvd-gtk.la
%{_libdir}/libogmjob.la
%{_libdir}/libogmrip.la
%{_libdir}/libogmrip-gtk.la
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

%files static
%defattr(644,root,root,755)
%{_libdir}/libogmdvd.a
%{_libdir}/libogmdvd-gtk.a
%{_libdir}/libogmjob.a
%{_libdir}/libogmrip.a
%{_libdir}/libogmrip-gtk.a
%{_libdir}/libogmrip-mplayer.a
