Summary:	Ripping and encoding DVD into AVI/OGM files
Summary(pl):	Zgrywanie i kodowanie DVD do plików AVI/OGM
Name:		ogmrip
Version:	0.7.1
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://dl.sf.net/ogmrip/%{name}-%{version}.tar.gz
# Source0-md5:	601470fc028b7c14b9e84455d198b8f9
BuildRequires:	gocr
BuildRequires:	lame
BuildRequires:	libdvdread-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	mplayer
BuildRequires:	ogmtools
BuildRequires:	vorbis-tools
BuildRequires:	pkgconfig
Requires:	gocr
Requires:	lame
Requires:	mplayer
Requires:	ogmtools
Requires:	vorbis-tools
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
Requires:	%{name} = %{version}-%{release}

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
Static lib3ds libraries.

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
