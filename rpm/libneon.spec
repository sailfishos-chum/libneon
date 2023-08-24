# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.32
# 

Name:       libneon

# >> macros
# << macros

Summary:    HTTP and WebDAV client library
Version:    0.32.5
Release:    0
Group:      Applications/Internet
License:    GPLv2
URL:        https://notroj.github.io/neon
Source0:    https://notroj.github.io/neon/%{name}-%{version}.tar.gz
Source100:  libneon.yaml
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libproxy-1.0)
BuildRequires:  libtool
BuildRequires:  autoconf
BuildRequires:  automake

%description
neon is an HTTP/1.1 and WebDAV client library, with a C interface.

    Features:

    High-level wrappers for common HTTP and WebDAV operations (GET, MOVE,
    DELETE, etc) Low-level interface to the HTTP request/response engine,
    allowing the use of arbitrary HTTP methods, headers, etc.

    Authentication support including Basic and Digest support, along with
    GSSAPI-based Negotiate on Unix, and SSPI-based Negotiate/NTLM on
    Win32

    SSL/TLS support using OpenSSL or GnuTLS; exposing an abstraction
    layer for verifying server certificates, handling client
    certificates, and examining certificate properties.

    Smartcard-based client certificates are also supported via a PKCS#11
    wrapper interface

    Abstract interface to parsing XML using libxml2 or expat, and
    wrappers for simplifying handling XML HTTP response bodies

    WebDAV metadata support; wrappers for PROPFIND and PROPPATCH to
    simplify property manipulation

%if 0%{?_chum}
Custom:
  PackagingRepo: https://github.com/sailfishos-chum/libneon
  Repo: https://github.com/notroj/neon
Categories:
 - Network
 - Library
Links:
  Homepage: %{url}
  Help: https://github.com/notroj/neon/discussions
  Bugtracker: https://github.com/notroj/neon/issues
%endif


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
%{summary}.

%if 0%{?_chum}
Custom:
  PackagingRepo: https://github.com/sailfishos-chum/libneon
  Repo: https://github.com/notroj/neon
Categories:
 - Network
 - Library
Links:
  Homepage: %{url}
  Help: https://github.com/notroj/neon/discussions
  Bugtracker: https://github.com/notroj/neon/issues
%endif


%prep
%setup -q -n %{name}-%{version}/upstream

# >> setup
# Fix compatibility with OpenSSL >=1.1.
sed -e "s/RSA_F_RSA_PRIVATE_ENCRYPT/RSA_F_RSA_OSSL_PRIVATE_ENCRYPT/" -i src/ne_pkcs11.c
# << setup

%build
# >> build pre
./autogen.sh
# << build pre

%configure --disable-static \
    --disable-nls \
    --enable-shared \
    --enable-threadsafe-ssl=posix \
    --with-ssl=openssl \
    --with-libproxy \
    --with-libxml2 \
    --with-zlib


# >> build post
#%%make %%{?_smp_mflags}
%make_build
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre

# >> install post
# default make install contains -docs which needs xmlto which fails to run correctly in OBS build environment
%{__make} DESTDIR=%{?buildroot} INSTALL="%{__install} -p" install-lib install-headers install-config
# fix double slash in pkgconfig file (thanks, rpmlint!):
sed -i 's@-L//usr/lib@-L/usr/lib@g' %{buildroot}%{_libdir}/pkgconfig/neon.pc
# << install post

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
# >> files
# << files

%files devel
%defattr(-,root,root,-)
%{_bindir}/neon-config
%dir %{_includedir}/neon
%{_includedir}/neon/*
%{_libdir}/%{name}.so
%{_libdir}/%{name}.la
%{_libdir}/pkgconfig/neon.pc
# >> files devel
# << files devel
