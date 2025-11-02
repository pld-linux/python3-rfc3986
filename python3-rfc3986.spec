#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Validating URI References per RFC 3986
Summary(pl.UTF-8):	Sprawdzanie poprawności URI według RFC 3986
Name:		python3-rfc3986
Version:	2.0.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/r/rfc3986/rfc3986-%{version}.tar.gz
# Source0-md5:	bbf20302bf26bc771e88cc775fbde3bc
Patch0:		rfc3986-intersphinx.patch
URL:		https://pypi.org/project/rfc3986
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-idna
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx-prompt
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python implementation of RFC 3986 including validation and authority
parsing.

%description -l pl.UTF-8
Pythonowa implementacja RFC 3986 obejmująca sprawdzanie poprawności i
analizę wiarygodności.

%package apidocs
Summary:	API documentation for Python rfc3986 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona rfc3986
Group:		Documentation

%description apidocs
API documentation for Pythona rfc3986 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona rfc3986.

%prep
%setup -q -n rfc3986-%{version}
%patch -P0 -p1

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 docs/source docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst LICENSE README.rst
%{py3_sitescriptdir}/rfc3986
%{py3_sitescriptdir}/rfc3986-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,api-ref,release-notes,user,*.html,*.js}
%endif
