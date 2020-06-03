Name:           expect
Version:        5.45.4
Release:        1
License:        Public Domain
Summary:        A Tool for Automating Interactive Programs
URL:            https://core.tcl.tk/expect/index
Source:         %{name}-%{version}.tar.gz
Patch1:         expect.patch
Patch2:         expect-fixes.patch
Patch3:         expect-log.patch
Patch4:         config-guess-sub-update.patch
BuildRequires:  autoconf
BuildRequires:  tcl-devel

%description
Expect is a tool primarily for automating interactive applications,
such as telnet, ftp, passwd, fsck, rlogin, tip, and more.  Expect
really makes this stuff trivial.  Expect is also useful for testing
these applications.  It is described in many books, articles, papers,
and FAQs.  There is an entire book on it available from O'Reilly.

%package devel
License:        Public Domain
Summary:        Header Files and C API Documentation for expect

%description devel
This package contains header files and documentation needed for linking
to expect from programs written in compiled languages like C, C++, etc.

This package is not needed for developing scripts that run under the
/usr/bin/expect interpreter, or any other Tcl interpreter with the
expect package loaded.

%prep
%autosetup -p0 -n %{name}-%{version}

%build
autoreconf
%configure \
	--with-tcl=%{_libdir} \
	--with-tk=no_tk \
	--with-tclinclude=%{_includedir} \
	--enable-shared
make %{?_smp_mflags} all pkglibdir=%{_libdir}/tcl/%{name}%{version}

%check
make %{?_smp_mflags} test

%install
# set the right path to the expect binary...
sed -i \
    -e '1s,^#![^ ]*expectk,#!%{_bindir}/wish\npackage require Expect,' \
    -e '1s,^#![^ ]*expect,#!%{_bindir}/expect,' \
    example/*
make install DESTDIR=%{buildroot} pkglibdir=%{_libdir}/tcl/%{name}%{version}
# Remove some executables and manpages we don't want to ship
rm %{buildroot}%{_bindir}/*passwd
rm %{buildroot}%{_bindir}/weather
rm %{buildroot}%{_mandir}/*/*passwd*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/tcl/*
%{_libdir}/lib*.so
%{_mandir}/man1/*
%doc ChangeLog HISTORY INSTALL FAQ NEWS README

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
