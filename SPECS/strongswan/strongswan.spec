Summary:          The OpenSource IPsec-based VPN Solution
Name:             strongswan
Version:          5.5.2
Release:          3%{?dist}
License:          GPLv2+
URL:              https://www.strongswan.org/
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          https://download.strongswan.org/%{name}-%{version}.tar.bz2
%define sha1      strongswan=0f181715fd25a98a9e0d3227b594c6fc8ed429c2
Patch0:           CVE-2017-9022.patch
Patch1:           CVE-2017-9023.patch
Patch2:           CVE-2017-11185.patch

BuildRequires:    autoconf

%description
strongSwan is a complete IPsec implementation for Linux 2.6, 3.x, and 4.x kernels.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}
sed -i '/stdlib.h/a #include <stdint.h>' src/libstrongswan/utils/utils.h &&
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/ipsec/*
%{_libexecdir}/*
%{_mandir}/man[158]/*
%{_datadir}/strongswan/*

%changelog
*   Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 5.5.2-3
-   Fix CVE-2017-11185 CVE-2017-9022 and CVE-2017-9023
*   Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 5.5.2-2
-   Fix compilation issue for glibc-2.26
*   Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 5.5.2-1
-   Update to version 5.5.2
*   Wed Dec 21 2016 Xiaolin Li <xiaolinl@vmware.com>  5.5.1-1
-   Initial build.
