# based on work by The Fedora Project (2017)
# Copyright (c) 1998, 1999, 2000 Thai Open Source Software Center Ltd
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

%global sepol_ver 2.8
%global selinux_ver 2.8

%if ! %{defined python3_sitearch}
%define python3_sitearch /%{_libdir}/python3.?/site-packages
%endif

Name:           setools
Version:        4.2.0
Release:        1
Summary:        Policy analysis tools for SELinux
License:        GPLv2
URL:            https://github.com/TresysTechnology/setools/wiki
Source0:        %{name}-%{version}.tar.bz2
Patch0:         disable_analysis_tools.patch
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  glibc-devel
BuildRequires:  gcc
BuildRequires:  libsepol-devel >= %{sepol_ver}
BuildRequires:  libsepol-static >= %{sepol_ver}
BuildRequires:  libselinux-devel >= %{selinux_ver}
BuildRequires:  swig
BuildRequires:  python3-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-cython > 0.28

Requires:       python3-%{name} = %{version}-%{release}
Requires:       python3-setools = %{version}-%{release}
Requires:       libselinux >= %{selinux_ver}

%description
SETools is a collection of command-line tools designed to
facilitate SELinux policy analysis.

This package includes the following console tools:

  sediff       Compare two policies to find differences.
  seinfo       List policy components.
  sesearch     Search rules (allow, type_transition, etc.)

%package        -n python3-setools
Summary:        Policy analysis tools for SELinux
Provides:       %{name}-python3 = %{version}-%{release}

%description -n python3-setools
SETools python3 is a collection Python 3 modules designed to
facilitate SELinux policy analysis.

%prep
%setup -q -n %{name}-%{version}/%{name}
%patch0 -p1
# removing unneeded tools + their tests (together for patch0)
rm -f setools/{dta.py,infoflow.py,permmap.py}
rm -f tests/{dta.py,infoflow.py,permmap.py}

%build
# enable debugging:
export DISTUTILS_DEBUG=1
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="%{optflags}" %{__python3} setup.py build

%install
rm -rf %{buildroot}
rm -rf %{buildroot}%{_bindir}
# enable debugging:
export DISTUTILS_DEBUG=1
%{__python3} setup.py install --root %{buildroot}

# Remove GUI content (part of gui package in fedora)
rm -f %{buildroot}%{_bindir}/apol
rm -f %{buildroot}%{_mandir}/man1/apol*

# Remove analysis tools and manuals
rm -f %{buildroot}%{_bindir}/sedta
rm -f %{buildroot}%{_bindir}/seinfoflow
rm -f %{buildroot}%{_mandir}/man1/sedta*
rm -f %{buildroot}%{_mandir}/man1/seinfoflow*

%check
# enable debugging:
export DISTUTILS_DEBUG=1
#%{__python3} setup.py test

%files
%defattr(-,root,root,-)
%{_bindir}/sediff
%{_bindir}/seinfo
%{_bindir}/sesearch
%exclude %{_mandir}/man1/sediff*
%exclude %{_mandir}/man1/seinfo*
%exclude %{_mandir}/man1/sesearch*

%files -n python3-setools
%defattr(-,root,root,-)
%doc COPYING
%doc COPYING.GPL
%doc COPYING.LGPL
# For noarch packages: sitelib
# %{python3_sitelib}/*
# For arch-specific packages: sitearch
%exclude %{python3_sitearch}/setoolsgui
%{python3_sitearch}/*

