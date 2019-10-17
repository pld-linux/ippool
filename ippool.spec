#
Summary:	An IP address pool manager
Name:		ippool
Version:	1.3
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net/openl2tp/%{name}-%{version}.tar.gz
# Source0-md5:	e2401e65db26a3764585b97212888fae
Source1:	%{name}d.init
Source2:	%{name}d.sysconfig
Patch0:		%{name}-headers.patch
Patch1:		%{name}-no_Werror.patch
URL:		http://www.openl2tp.org/
BuildRequires:	ppp-plugin-devel
BuildRequires:	readline-devel
Requires:	portmap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IpPool is an IP address pool manager.

IpPool is implemented as a separate server daemon to allow any
application to use its address pools. This makes it possible to define
address pools that are shared by PPP, L2TP, PPTP etc. It may be useful
in some VPN server setups.

IpPool comes with a command line management application, ippoolconfig
to manage and query address pool status. A pppd plugin is supplied
which allows pppd to request IP addresses from ippoold.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} -j1 \
	SYS_LIBDIR="%{_libdir}" \
	CFLAGS.optimize="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,%{_libdir}/pppd/plugins}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	SYS_LIBDIR="%{_libdir}" \
	PPPD_LIBDIR=%{_libdir}/pppd/plugins

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ippoold
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ippoold

touch $RPM_BUILD_ROOT%{_sysconfdir}/ippoold.conf

rm -f $RPM_BUILD_ROOT%{_libdir}/libusl.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%dir %{_libdir}/ippool
%attr(755,root,root) %{_bindir}/ippoolconfig
%attr(755,root,root) %{_sbindir}/ippoold
%{_libdir}/ippool/ippool_rpc.x
%attr(755,root,root) %{_libdir}/pppd/plugins/ippool.so
%{_mandir}/man1/ippoolconfig.1*
%{_mandir}/man4/ippool_rpc.4*
%{_mandir}/man8/ippoold.8*
%attr(754,root,root) /etc/rc.d/init.d/ippoold
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ippoold
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ippoold.conf
