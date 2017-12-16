%global sname plv8

%{?!v8_arches:%global v8_arches %arm %ix86 x86_64}

Summary:	V8 Engine Javascript Procedural Language add-on for PostgreSQL
Name:		%{sname}
Version:	2.1.0
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/%{sname}/%{sname}/archive/v%{version}.tar.gz

Patch0:		plv8-2.1.0-make.patch

URL:		https://github.com/plv8/plv8

BuildRequires:	postgresql-devel
BuildRequires:	v8-devel
BuildRequires:	gcc-c++
BuildRequires:	perl-interpreter

Requires:	postgresql-server
%{?postgresql_module_requires}
Requires:	v8
ExclusiveArch:	%v8_arches


%description
plv8 is a shared library that provides a PostgreSQL procedural language
powered by V8 JavaScript Engine. With this program you can write in JavaScript
your function that is callable from SQL.


%prep
%autosetup -p1


%build
# Setup CFLAGS, etc. by hacked %%configure
%define _configure :
%configure

%make_build


%install
%make_install


%files
%license COPYRIGHT
%doc README.md Changes doc/%{sname}.md
%{_libdir}/pgsql/%{sname}.so
%dir %{_datadir}/pgsql/extension
%{_datadir}/pgsql/extension/plcoffee--%{version}.sql
%{_datadir}/pgsql/extension/plcoffee.control
%{_datadir}/pgsql/extension/plls--%{version}.sql
%{_datadir}/pgsql/extension/plls.control
%{_datadir}/pgsql/extension/%{sname}--%{version}.sql
%{_datadir}/pgsql/extension/%{sname}.control


%changelog
* Sat Dec 16 2017 Pavel Raiskup <praiskup@redhat.com> - 2.1.0-2
- fixes per pre-review by Robert-André Mauchin (rhbz#1036130)
- require proper postgresql-server version

* Fri Dec 15 2017 Pavel Raiskup <praiskup@redhat.com> - 2.1.0-1
- rebase to 2.1.0
- cleanup spec, fix {cxx,ld}flags

* Tue Nov 10 2015 Pavel Kajaba <pkajaba@redhat.com> 1.4.4-1
- Made changes to work under Fedora repos

* Wed Jul 9 2014 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2

* Thu Dec 12 2013 Devrim GÃ¼ndÃ¼z <devrim@gunduz.org> 1.4.1-1
- Initial spec file, per RH #1036130, after doing modifications
  to suit community RPM layout. Original work is by David
  Wheeler and Mikko Tiihonen
