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
BuildRequires:	enca-devel
BuildRequires:	eject
BuildRequires:	mencoder
BuildRequires:	gettext-devel
BuildRequires:	gocr >= 0.39
BuildRequires:	hal-devel >= 0.4.2
BuildRequires:	intltool
BuildRequires:	lame >= 3.96
BuildRequires:	libdvdread-devel >= 0.9
BuildRequires:	libgnomeui-devel >= 2.6.0
BuildRequires:	libstdc++-devel
BuildRequires:	libuuid-devel
%{?with_matroska:BuildRequires:	mkvtoolnix >= 0.9.5}
BuildRequires:	mplayer >= 0.92
BuildRequires:	ogmtools >= 1.0
BuildRequires:	pkgconfig
BuildRequires:	vorbis-tools >= 1.0
Requires:	eject
Requires:	gocr >= 0.39
Requires:	lame >= 3.96
%{?with_matroska:Requires:	mkvtoolnix >= 0.9.5}
Requires:	mplayer >= 0.92
Requires:	mencoder
Requires:	ogmtools >= 1.0
Requires:	vorbis-tools >= 1.0
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
	--disable-schemas-install \
	--with-html-dir=%{_gtkdocdir} 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*.1.*
%dir %{_gtkdocdir}/ogmdvd
%doc %{_gtkdocdir}/ogmdvd/*
%dir %{_gtkdocdir}/ogmdvd-gtk
%doc %{_gtkdocdir}/ogmdvd-gtk/*
%dir %{_gtkdocdir}/ogmjob
%doc %{_gtkdocdir}/ogmjob/*
%dir %{_gtkdocdir}/ogmrip-gtk
%doc %{_gtkdocdir}/ogmrip-gtk/*
%dir %{_gtkdocdir}/ogmrip
%doc %{_gtkdocdir}/ogmrip/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*
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
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_libdir}/%{name}/audio-codecs/*.la
%{_libdir}/%{name}/containers/*.la
%{_libdir}/%{name}/subp-codecs/*.la
%{_libdir}/%{name}/video-codecs/*.la
%{_includedir}/*
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
%{_libdir}/%{name}/audio-codecs/*.a
%{_libdir}/%{name}/containers/*.a
%{_libdir}/%{name}/subp-codecs/*.a
%{_libdir}/%{name}/video-codecs/*.a
