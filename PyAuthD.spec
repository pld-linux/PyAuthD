%define	snap	20070218
Summary:	Python module for accessing Extended Attributes of the files
Summary(pl.UTF-8):	Moduł języka Python pozwalający na dostęp do rozszerzonych atrybutów plików
Name:		PyAuthD
Version:	0.1
Release:	0.%{snap}.1
License:	GPL
Group:		Libraries/Python
Source0:	%{name}-20070218.tar.gz
# Source0-md5:	2b7d72bd6c75f0fa58707c25e398f87e
URL:		http://svn.asta.mh-hannover.de/categories/python/pyauthd/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyAuthD is an authentication daemon which implements a unified NSS/PAM
infrastructure for creating virtual user accounts under Unix. It is
similar to the combination of {nss,pam}_ldap to authenticate against a
user database in LDAP, but is more extensible.

%prep
%setup -q -n %{name}

%build
%{__cc} %{rpmcflags} -Wall -fPIC -DPIC -c -I. -Iinclude -o PyAuthD_client.o src/PyAuthD_client.c
%{__cc} %{rpmcflags} -Wall -fPIC -DPIC -c -I. -Iinclude -o PyAuthD_PAM.o src/PyAuthD_PAM.c
%{__cc} %{rpmldflags} -shared PyAuthD_client.o PyAuthD_PAM.o -o pam_PyAuthD.so -lpam

%{__cc} %{rpmcflags} -Wall -fPIC -DPIC -c -I. -Iinclude -o PyAuthD_NSS_passwd.o src/PyAuthD_NSS_passwd.c
%{__cc} %{rpmcflags} -Wall -fPIC -DPIC -c -I. -Iinclude -o PyAuthD_NSS_shadow.o src/PyAuthD_NSS_shadow.c
%{__cc} %{rpmcflags} -Wall -fPIC -DPIC -c -I. -Iinclude -o PyAuthD_NSS_group.o src/PyAuthD_NSS_group.c
%{__cc} %{rpmldflags} -shared PyAuthD_NSS_passwd.o PyAuthD_NSS_shadow.o PyAuthD_NSS_group.o -o libnss_PyAuthD.so.2 -Wl,-soname -Wl,libnss_PyAuthD.so.2

%{__cc} %{rpmcflags} -Wall -fPIC -DPIC -c -I. -Iinclude -o PyAuthD_PPP.o src/PyAuthD_PPP.c
%{__cc} %{rpmldflags} -shared PyAuthD_PPP.o PyAuthD_client.o -o ppp_PyAuthD.so

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.html
%attr(755,root,root) %{py_sitedir}/*.so
