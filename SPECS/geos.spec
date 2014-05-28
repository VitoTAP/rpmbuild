Name:		geos
Version:	3.4.2
Release:	2%{?dist}
Summary:	GEOS is a C++ port of the Java Topology Suite

Group:		Applications/Engineering
License:	LGPLv2
URL:		http://trac.osgeo.org/geos/
Source0:	http://download.osgeo.org/%{name}/%{name}-%{version}.tar.bz2
#Patch0:		geos-gcc43.patch
# fixed in upstream revision 3000
#Patch1:		geos-3.2.1-swig.patch
# Fixes SWIG interface for Ruby 1.9 compatibility.
# http://trac.osgeo.org/geos/ticket/379
#Patch2:		geos-3.3.2-ruby-19.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	doxygen libtool
%if "%{?dist}" != ".el4"
BuildRequires:	swig ruby
#BuildRequires:	python-devel ruby-devel php-devel
%endif

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')}
%{!?php_sitearch: %define php_sitearch %{_libdir}/php/modules}

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology 
Suite (JTS). As such, it aims to contain the complete functionality of 
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial 
predicate functions and spatial operators, as well as specific JTS topology 
functions such as IsValid()

%package devel
Summary:	Development files for GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology 
Suite (JTS). As such, it aims to contain the complete functionality of 
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial 
predicate functions and spatial operators, as well as specific JTS topology 
functions such as IsValid()

This package contains the development files to build applications that 
use GEOS

%if "%{?dist}" != ".el4"
%package python
Summary:	Python modules for GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description python
Python module to build applications using GEOS and python

%package ruby
Summary:	Ruby modules for GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description ruby
Ruby module to build applications using GEOS and ruby

%package php
Summary:	PHP modules for GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description php
PHP module to build applications using GEOS and PHP
%endif

%prep
%setup -q 
#%patch0 -p0 -b .gcc43
#%patch2 -p0 -b .ruby19

%build

# fix python path on 64bit
sed -i -e 's|\/lib\/python|$libdir\/python|g' configure
sed -i -e 's|.get_python_lib(0|.get_python_lib(1|g' configure
sed -i -e 's|find \$i -name libpython|find \$i\/lib*\/ -name libpython|g' configure

# disable internal libtool to avoid hardcoded r-path
for makefile in `find . -type f -name 'Makefile.in'`; do
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done

# Use correct library placement for Ruby 1.9.
#sed -i 's|sitearchdir|vendorarchdir|' configure

%configure --disable-static --disable-dependency-tracking \
%if "%{?dist}" != ".el4"
#           --enable-php
%endif
#make %{?_smp_mflags} CPPFLAGS=-I`ruby -e 'puts File.join(RbConfig::CONFIG[%q(includedir)], RbConfig::CONFIG[%q(sitearch)])'`
make -j2 %{?_smp_mflags}

# Make doxygen documentation files
cd doc
make doxygen-html

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# install php config file
#mkdir -p %{buildroot}%{_sysconfdir}/php.d/
#cat > %{buildroot}%{_sysconfdir}/php.d/%{name}.ini <<EOF
#; Enable %{name} extension module
#extension=geos.so
#EOF

%check

# test module
make %{?_smp_mflags} check || exit 0

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README TODO
%{_libdir}/libgeos-%{version}.so
%{_libdir}/libgeos_c.so.1*
%exclude %{_libdir}/*.a

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen_docs
%{_bindir}/geos-config
%{_includedir}/*
%{_libdir}/libgeos.so
%{_libdir}/libgeos_c.so
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a

%if "%{?dist}" != ".el4"

%endif

%changelog
* Wed Mar 13 2013 Vít Ondruch <vondruch@redhat.com> - 3.3.8-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Mar 6 2013 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.8-1
- Update to 3.3.8, per changes described in:
  http://trac.osgeo.org/geos/browser/tags/3.3.8/NEWS

* Fri Jan 25 2013 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.7-1
- Update to 3.3.7, per changes described in:
  http://trac.osgeo.org/geos/browser/tags/3.3.7/NEWS

* Fri Nov 16 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.6-1
- Update to 3.3.6, per changes described in:
  http://trac.osgeo.org/geos/browser/tags/3.3.6/NEWS

* Tue Nov 13 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.5-1
- Update to 3.3.5
- Remove patch3, already in upstream.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Vít Ondruch <vondruch@redhat.com> - 3.3.2-2
- Rebuilt for Ruby 1.9.3.
- Rebuilt for PHP 5.4.

* Mon Jan 09 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.2-1
- Update to 3.3.2

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 3.3.1-3
- track soname so abi bumps aren't a surprise

* Tue Oct 18 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.1-2
- Enable PHP bindings, per Peter Hopfgartner, bz #746574

* Tue Oct 4 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.1-1
- Update to 3.3.1

* Wed Jun 1 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.0-1
- Update to 3.3.0
- Remove 2 patches.

* Mon May 9 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.2.2-1
- Update to 3.2.2
- Add a patch to fix builds on ARM, per bz #682538

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 21 2010 Dan Horák <dan[at]danny.cz> - 3.2.1-2
- fix build with swig 2.0.0

* Tue Mar 30 2010 Devrim GUNDUZ <devrim@gunduz.org> - 3.2.1-1
- Update to 3.2.1

* Thu Mar 18 2010 Balint Cristian <cristian.balint@gmail.com> - 3.2.0-2
- fix bz#473975

* Sun Dec 20 2009 Devrim GUNDUZ <devrim@gunduz.org> - 3.2.0-1
- Update to 3.2.0

* Thu Dec 03 2009 Devrim GÜNDÜZ <devrim@gunduz.org> - 3.2.0-rc3_1.1
- Fix spec (dep error).

* Wed Dec 2 2009 Devrim GUNDUZ <devrim@gunduz.org> - 3.2.0rc3-1
- Update to 3.2.0 rc3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
