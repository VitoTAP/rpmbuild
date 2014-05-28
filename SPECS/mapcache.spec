Name:           mapcache
Version:        1.2.0
Release:        1%{?dist}
Summary:        Caching server for WMS layers
Group:          Development/Tools
License:        MIT
URL:            http://mapserver.org/trunk/en/mapcache/
Source:         mapcache-%{version}.tar.gz
#Obtain source using git archive available at https://github.com/mapserver/mapcache:
#git archive --format=tar --prefix=mapcache-1.2.0/ master | gzip > mapcache-1.2.0.tar.gz
#or adjust archive available at: https://github.com/mapserver/mapcache/archive/master.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       webserver

BuildRequires:  httpd-devel cmake libcurl-devel fcgi-devel
BuildRequires:  geos-devel proj-devel gdal-devel libjpeg-turbo-devel
BuildRequires:  libpng-devel libtiff-devel pixman-devel sqlite-devel


%description
MapCache is a server that implements tile caching to speed up access to WMS layers. 
The primary objectives are to be fast and easily deployable, while offering the 
essential features (and more!) expected from a tile caching solution.

%prep
%setup -q -n %{name}-%{version}

%build
%cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} \
    install
mv %{buildroot}%{_libdir}/../lib/* %{buildroot}%{_libdir}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL README* LICENSE 
%{_bindir}/*
%{_libdir}/*
#%{_libdir}/../lib/*

%changelog
* Tue Dec 10 2013 Stephan Meissl <stephan.meissl@eox.at> - 1.2.0-1
- Updating to 1.2.0 release

* Fri Aug 23 2013 Stephan Meissl <stephan.meissl@eox.at> - 1.1dev-7
- Resolved double time entries issue (#79)

* Thu Jul 04 2013 Stephan Meissl <stephan.meissl@eox.at> - 1.1dev-6
- Added support for bounding box in time dimension query

* Tue Apr 16 2013 Stephan Meissl <stephan.meissl@eox.at> - 1.1dev-5
- Added max-cached-zoom support

* Tue Jan 08 2013 Stephan Meissl <stephan.meissl@eox.at> - 1.1dev-2
- Added ro-tileset support
