%define name	mozart
%define version 1.4.0
%define date    20080704
%define release %mkrel 1
%define _disable_ld_no_undefined 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Mozart, an efficient and distributed implementation of Oz
License:	Mozart License
Group:		Development/Other
Url:		http://www.mozart-oz.org/
Source0:	ftp://ftp.mozart-oz.org/pub/%{version}/tar/%{name}-%{version}.%{date}-src.tar.gz
Patch1:		mozart-1.4.0.20080704-fhs.patch
Patch2:		mozart-1.4.0.20080704-add-missing-man-pages.patch
Patch3:		mozart-1.4.0.20080704-fix-tcl-build.patch
Patch4:     mozart-1.4.0.20080704-fix-build.patch
Patch5:     mozart-1.4.0.20080704-fix-install.patch
BuildRequires:	libgmp-devel
BuildRequires:	libgdbm-devel
BuildRequires:	zlib-devel
BuildRequires:	libxscrnsaver-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	tk
BuildRequires:	tk-devel
BuildRequires:	openjade
BuildRequires:	ghostscript
BuildRequires:	tetex-latex
BuildRequires:	tetex-dvips
BuildRequires:	emacs-bin
BuildRequires:	flex
BuildRequires:	bison
ExclusiveArch:  %{ix86}
BuildRoot:	    %{_tmppath}/%{name}-%{version}

%description
The Mozart system provides state-of-the-art support in two areas: open
distributed computing and constraint-based inference. Mozart
implements Oz, a concurrent object-oriented language with dataflow
synchronization. Oz combines concurrent and distributed programming
with logical constraint-based inference, making it a unique choice for
developing multi-agent systems. Mozart is an ideal platform for both
general-purpose distributed applications as well as for hard problems
requiring sophisticated optimization and inferencing abilities. We
have developed applications in scheduling and time-tabling, in
placement and configuration, in natural language and knowledge
representation, multi-agent systems and sophisticated collaborative
tools.

Mozart has been jointly developed by the Programming Systems Lab at
DFKI and Universität des Saarlandes, the Swedish Institute of Computer
Science, and Université de Louvain.

This package contains all you need to run and develop Oz programs with
Mozart.

%package doc
Summary:	Mozart documentation
Group:		Development/Other

%description doc
This package contains the extensive Mozart online documentation as a
set of HTML pages, postscript and pdf documents. It also contains demo
applications that can directly be started from the pages.

%prep
%setup -q -n %{name}-%{version}.%{date}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%configure \
	--prefix=%{_datadir}/%{name} \
	--disable-copy-tcl-libs \
	--disable-compile-elisp \
    --disable-contrib-micq \
	--enable-opt \
	--enable-doc \
	--with-documents=all

make 

%install
rm -rf %{buildroot}

# generic install
make PREFIX=%{buildroot}%{_datadir}/%{name} install

# fix perms
find %{buildroot} -type f -exec chmod u+w {} \;
find %{buildroot} -type d -exec chmod g-w {} \;

# install man pages
install -d -m 755 %{buildroot}%{_mandir}/man1
install -m 644 doc/man/*.1 %{buildroot}%{_mandir}/man1

install -d -m 755 %{buildroot}%{_bindir}
for f in oz ozengine ozc ozl ozd oztool convertTextPickle ozdoc; do
	mv %{buildroot}%{_datadir}/%{name}/bin/$f %{buildroot}%{_bindir}
done

install -d -m 755 %{buildroot}%{_libdir}/%{name}/bin
mv %{buildroot}%{_datadir}/%{name}/bin/ozplatform \
	%{buildroot}%{_libdir}/%{name}/bin

for f in oldpickle2text pickle2text text2pickle; do
	ln -sf ../../../bin/oz %{buildroot}/%{_libdir}/%{name}/bin/$f
	rm -f %{buildroot}%{_datadir}/%{name}/bin/$f
done

# move architecture-dependent files into /usr/lib/mozart
cd %{buildroot}%{_datadir}/%{name}
find -type f -a -name '*.so-*' | \
tar --create --files-from - --remove-files | \
(cd %{buildroot}%{_libdir}/%{name} && tar --preserve --extract)

rm -rf %{buildroot}%{_datadir}/%{name}/cache/x-oz/boot
rm -rf %{buildroot}%{_libdir}/%{name}/platform

mv %{buildroot}%{_datadir}/%{name}/platform %{buildroot}%{_libdir}/%{name}

# remove superfluous tcl/tk stuff
rm -r %{buildroot}/%{_libdir}/%{name}/platform/*/wish

# move elisp files to their proper place
install -d -m 755 %{buildroot}%{_datadir}/emacs/site-lisp
mv %{buildroot}%{_datadir}/%{name}/share/elisp \
	   %{buildroot}%{_datadir}/emacs/site-lisp/%{name}

# move include files to their proper place
install -d -m 755 %{buildroot}/%{_includedir}
mv %{buildroot}%{_datadir}/%{name}/include \
	   %{buildroot}/%{_includedir}/%{name}

# remove licenses (see debian/copyright)
rm -f %{buildroot}%{_datadir}/%{name}/README \
rm -f %{buildroot}%{_datadir}/%{name}/LICENSE*

# remove useless documentation file
rm -f %{buildroot}%{_datadir}/%{name}/doc/.htaccess
rm -f %{buildroot}%{_datadir}/%{name}/doc/install/*.diff
rm -f %{buildroot}%{_datadir}/%{name}/doc/install/FILES

# move the documentation and the examples 
install -d -m 755 %{buildroot}%{_docdir}
mv %{buildroot}%{_datadir}/%{name}/doc \
	%{buildroot}%{_docdir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/examples \
	%{buildroot}%{_docdir}/%{name}


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README LICENSE LICENSE.html LICENSE.rtf
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/emacs/site-lisp/%{name}
%{_includedir}/%{name}

%files doc
%defattr(-,root,root)
%{_docdir}/%{name}
