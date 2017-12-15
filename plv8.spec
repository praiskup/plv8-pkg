%global pgmajorversion 9.4
%global pginstdir %{_libdir}/pgsql
%global sname plv8
%global extensions /usr/share/pgsql/extension


Summary:	V8 Engine Javascript Procedural Language add-on for PostgreSQL
Name:		%{sname}
Version:	1.4.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/%{sname}/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-makefile.patch
URL:		https://github.com/plv8/plv8

BuildRequires:	postgresql-devel >= %{pgmajorversion}, v8-devel >= 3.14.5, gcc-c++
Requires:	postgresql >= %{pgmajorversion}, v8 >= 3.14.5

%description
plv8 is a shared library that provides a PostgreSQL procedural language
powered by V8 JavaScript Engine. With this program you can write in JavaScript
your function that is callable from SQL.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot} %{?_smp_mflags}
%{__rm} -f  %{buildroot}%{_datadir}/*.sql

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT README Changes doc/%{sname}.md
%{pginstdir}/%{sname}.so
%{extensions}/plcoffee--%{version}.sql
%{extensions}/plcoffee.control
%{extensions}/plls--%{version}.sql
%{extensions}/plls.control
%{extensions}/%{sname}--%{version}.sql
%{extensions}/%{sname}.control

%changelog
* Tue Nov 10 2015 Pavel Kajaba <pkajaba@redhat.com> 1.4.4-1
- Made changes to work under Fedora repos

* Wed Jul 9 2014 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2

* Thu Dec 12 2013 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> 1.4.1-1
- Initial spec file, per RH #1036130, after doing modifications
  to suit community RPM layout. Original work is by David
  Wheeler and Mikko Tiihonen
