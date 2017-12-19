%global sname plv8

%bcond_without check

%{?!v8_arches:%global v8_arches %arm %ix86 x86_64}

Summary:	V8 Engine Javascript Procedural Language add-on for PostgreSQL
Name:		%{sname}
Version:	2.1.0
Release:	5%{?dist}
License:	BSD
Source0:	https://github.com/%{sname}/%{sname}/archive/v%{version}/%{name}-%{version}.tar.gz

# Please self-document the patches inside ('git am' format for backports)
# -----------------------------------------------------------------------
# Ensure build system respects Fedora's CXXFLAGS for hardening.
Patch0:		plv8-2.1.0-make-respects-CXXFLAGS.patch
# Support RPM_HACK_LDFLAGS to work-around rhzb#1517657 below.
Patch1:		plv8-2.1.0-make-bug-1517657.patch
# Support for 'make test' in %%check section.
Patch2:		plv8-2.1.0-make-test.patch

URL:		https://github.com/plv8/plv8

BuildRequires:	postgresql-devel
BuildRequires:	v8-devel
BuildRequires:	gcc-c++
BuildRequires:	perl-interpreter
%if %{with check}
BuildRequires:	postgresql-server
%endif

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

# rhbz#1517657
ln -s %{_libdir}/libv8_libplatform.so.? libv8_libplatform.so
export LDFLAGS="$LDFLAGS -L$PWD"

%make_build RPM_HACK_LDFLAGS="-L$PWD"


%if %{with check}
%check
make test || {
    find -name '*.diffs' -exec cat {} +
# Known to fail on armv7hl architecture, reported in pull request #247.
%ifnarch %arm
    false
%endif
}
%endif


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
* Tue Dec 19 2017 Pavel Raiskup <praiskup@redhat.com> - 2.1.0-5
- review requirement - in-spec docs for patches (rhbz#1036130)

* Tue Dec 19 2017 Pavel Raiskup <praiskup@redhat.com> - 2.1.0-4
- review fixes - per Robert-André Mauchin notes - better github source url,
  drop Group tag, better format of patches (rhbz#1036130)
- ignore test failure on %%arm (reported upstream in PR#247)

* Mon Dec 18 2017 Pavel Raiskup <praiskup@redhat.com> - 2.1.0-3
- enable testsuite

* Sat Dec 16 2017 Pavel Raiskup <praiskup@redhat.com> - 2.1.0-2
- fixes per pre-review by Robert-André Mauchin (rhbz#1036130)
- require proper postgresql-server version
- hack for missing libv8_libplatform.so in v8-devel (rhbz#1517657)

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
