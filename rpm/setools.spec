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

%global sepol_ver 2.7-1
%global selinux_ver 2.7-1

%define python3_sitearch /%{_libdir}/python3.?/site-packages

Name:           setools
Version:        4.1.1
Release:        6%{?setools_pre_ver:.%{setools_pre_ver}}%{?dist}
Summary:        Policy analysis tools for SELinux

License:        GPLv2
URL:            https://github.com/TresysTechnology/setools/wiki
Source0: %{name}-%{version}.tar.bz2
Source1: setup.py
#Patch1:         0001-Do-not-use-Werror-during-build.patch
#Patch2:         0002-Do-not-export-use-setools.InfoFlowAnalysis-and-setoo.patch
#Patch3:         0003-bswap_-macros-are-defined-in-byteswap.h.patch

Obsoletes:      setools < 4.0.0, setools-devel < 4.0.0
BuildRequires:  flex,  bison
BuildRequires:  glibc-devel, gcc
#, git
BuildRequires:  libsepol-devel >= %{sepol_ver}, libsepol-static >= %{sepol_ver}
BuildRequires:  swig
BuildRequires:  python3-devel
BuildRequires:  python-setuptools

# BuildArch:      
Requires:       python3-%{name} = %{version}-%{release}

%description
SETools is a collection of graphical tools, command-line tools, and
Python modules designed to facilitate SELinux policy analysis.

%package     console
Summary:     Policy analysis command-line tools for SELinux
License:     GPLv2
Requires:    python3-setools = %{version}-%{release}
Requires:    libselinux >= %{selinux_ver}

%description console
SETools is a collection of graphical tools, command-line tools, and
libraries designed to facilitate SELinux policy analysis.

This package includes the following console tools:

  sediff       Compare two policies to find differences.
  seinfo       List policy components.
  sesearch     Search rules (allow, type_transition, etc.)


#%package     console-analyses
#Summary:     Policy analysis command-line tools for SELinux
#License:     GPLv2
#Requires:    python3-setools = %{version}-%{release}
#Requires:    libselinux >= %{selinux_ver}
#Requires:    python3-networkx
#
#%description console-analyses
#SETools is a collection of graphical tools, command-line tools, and
#libraries designed to facilitate SELinux policy analysis.
#
#This package includes the following console tools:
#
#  sedta        Perform domain transition analyses.
#  seinfoflow   Perform information flow analyses.


%package     -n python3-setools
Summary:     Policy analysis tools for SELinux  
Obsoletes:   setools-libs < 4.0.0, setools-libs-tcl
Provides: %{name}-python3 = %{version}-%{release}
Provides: %{name}-python3%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}

%description -n python3-setools
SETools is a collection of graphical tools, command-line tools, and
Python 3 modules designed to facilitate SELinux policy analysis.

%prep
%setup -q -n %{name}-%{version}/%{name}
cp %{SOURCE1} ./

%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="%{optflags}" %{__python3} setup.py build

%install
rm -rf %{buildroot}
rm -rf %{buildroot}%{_bindir}
%{__python3} setup.py install --root %{buildroot}

%check
%{__python3} setup.py test

%files

%files console
%{_bindir}/sediff
%{_bindir}/seinfo
%{_bindir}/sesearch
%{_mandir}/man1/sediff*
%{_mandir}/man1/seinfo*
%{_mandir}/man1/sesearch*

#%files console-analyses
#%{_bindir}/sedta
#%{_bindir}/seinfoflow
#%{_mandir}/man1/sedta*
#%{_mandir}/man1/seinfoflow*

%files -n python3-setools
%license COPYING COPYING.GPL COPYING.LGPL
# %doc AUTHORS ChangeLog KNOWN-BUGS NEWS README
# For noarch packages: sitelib
# %{python3_sitelib}/*
# For arch-specific packages: sitearch
%{python3_sitearch}/*