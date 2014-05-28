Name:		CharLS
Version:	1.0
Release:	1%{?dist}
Summary:	An optimized implementation of the JPEG-LS standard
Group:		Development/Libraries
License:	BSD
URL:		http://charls.codeplex.com/
# CharLS uses an interactive download link that asks you to accept the
# (BSD-like) license before obtaining the source code.
# You can find the download link at http://charls.codeplex.com/
Source0:	CharLS-source-1.0.zip
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:		charls_add_cmake_install_target.patch
Patch1:		charls_add_sharedlib_soname.patch
Patch2:		charls_fix_tests.patch

BuildRequires:	cmake >= 2.6.0
BuildRequires:	dos2unix

%description
An optimized implementation of the JPEG-LS standard for loss less and 
near loss less image compression. JPEG-LS is a low-complexity standard that
matches JPEG 2000 compression ratios. In terms of speed, CharLS outperforms
open source and commercial JPEG LS implementations.

JPEG-LS (ISO-14495-1/ITU-T.87) is a standard derived from the Hewlett Packard
LOCO algorithm. JPEG LS has low complexity (meaning fast compression) and high
compression ratios, similar to JPEG 2000. JPEG-LS is more similar to the old
loss less JPEG than to JPEG 2000, but interestingly the two different techniques
result in vastly different performance characteristics.

%prep
%setup -c -q

rm CharLS.vcproj
rm CharLS.sln

dos2unix *.h
dos2unix *.c*
dos2unix *.txt

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%cmake -DBUILD_SHARED_LIBS:BOOL=ON\
	-Dcharls_BUILD_SHARED_LIBS:BOOL=ON\
       -DCMAKE_BUILD_TYPE:STRING="Release"\
       -DCMAKE_VERBOSE_MAKEFILE=ON\
       -DBUILD_TESTING=ON .

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%check
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.
ctest .

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc License.txt
%{_libdir}/*.so.*


%package        devel
Summary:	Libraries and headers for CharLS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel

CharLS Library Header Files and Link Libraries

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}/
%{_includedir}/%{name}/*
%{_libdir}/*.so

%changelog
* Thu Feb 3 2011 Mario Ceresa mrceresa@gmail.com CharLS 1.0-1
- Update to new version
- Applied patch to fix bug http://charls.codeplex.com/workitem/7823

* Wed Feb 17 2010 Mario Ceresa mrceresa@gmail.com CharLS 1.0-0.1.b
- Changed name schema to comply with pre-release packages

* Wed Feb 17 2010 Mario Ceresa mrceresa@gmail.com CharLS 1.0b-1
- Initial RPM Release
