#
# Conditional build:
%bcond_without	matroska	# don't build with matroska support
#
Summary:	Ripping and encoding DVD into AVI/OGM files
Summary(pl):	Zgrywanie i kodowanie DVD do plików AVI/OGM
Name:		ogmrip
Version:	0.8.2
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/ogmrip/%{name}-%{version}.tar.gz
# Source0-md5:	c84a295d1b67fa69b8c81b89f54c4acc
BuildRequires:	gettext-devel
BuildRequires:	gocr >= 0.39
BuildRequires:	hal-devel >= 0.4.2
BuildRequires:	intltool
BuildRequires:	lame >= 3.96
BuildRequires:	libdvdread-devel >= 0.9
BuildRequires:	libgnomeui-devel >= 2.6.0
BuildRequires:	libstdc++-devel
%{?with_matroska:BuildRequires:	mkvtoolnix >= 0.9.5}
BuildRequires:	mplayer >= 0.92
BuildRequires:	ogmtools >= 1.0
BuildRequires:	pkgconfig
BuildRequires:	vorbis-tools >= 1.0
Requires:	gocr >= 0.39
Requires:	lame >= 3.96
%{?with_matroska:Requires:	mkvtoolnix >= 0.9.5}
Requires:	mplayer >= 0.92
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

%description -l pl
OGMRip jest aplikacj± i zestawem bibliotek s³u¿±cymi do zgrywania i
kodowania DVD do plików AVI/OGM przy u¿yciu wielu ró¿nych kodeków. Do
wykonywania zadañ u¿ywa mplayera, mencodera, ogmtools, oggenc i lame.

Cechy:
- przekodowuje z DVD lub plików,
- na wyj¶ciu daje pliki ogm, avi lub matroska,
- umo¿liwia u¿ywanie wielu kodeków (ogg vorbis, mp3, pcm, ac3, xvid,
  lavc),
- oblicza tempo bitowe dla danego rozmiaru pliku,
- oblicza parametry obcinania i skalowania,
- u¿ywa kodeków z ustawionymi parametrami maksymalnej jako¶ci,
- wspiera wydobycie napisów,
- zgrywa ci±g³e rozdzia³y.

%package libs
Summary:	%{name} libraries
Summary(pl):	Biblioteki %{name}
Group:		Libraries

%description libs
%{name} libraries.

%description libs -l pl
Biblioteki %{name}.

%package devel
Summary:	%{name} header files
Summary(pl):	Pliki nag³ówkowe %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
%{name} header files.

%description devel -l pl
Pliki nag³ówkowe %{name}.

%package static
Summary:	Static %{name} libraries
Summary(pl):	Statyczne biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} libraries.

%description static -l pl
Statyczne biblioteki %{name}.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install

%post	libs	-p /sbin/ldconfig
%postun	libs	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_datadir}/%{name}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/*
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
