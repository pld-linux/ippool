Summary:	An IP address pool manager
Summary(pl.UTF-8):	Zarządca pul adresów IP
Name:		ippool
Version:	1.3
Release:	5
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net/openl2tp/%{name}-%{version}.tar.gz
# Source0-md5:	e2401e65db26a3764585b97212888fae
Source1:	%{name}d.init
Source2:	%{name}d.sysconfig
Patch0:		%{name}-headers.patch
Patch1:		%{name}-no_Werror.patch
Patch2:		%{name}-opt.patch
Patch3:		%{name}-tirpc.patch
URL:		http://www.openl2tp.org/
BuildRequires:	libtirpc-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	ppp-plugin-devel
BuildRequires:	readline-devel
BuildRequires:	rpcsvc-proto
Requires:	rpcbind
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

%description -l pl.UTF-8
IpPool to zarządca pul adresów IP.

IpPool jest zaimplementowane jako osobny demon, aby pozwolić dowolnej
aplikacji korzystać z jego pul adresów. Umożliwia to definiowanie pul
adresów współdzielonych przez PPP, L2TP, PPTP itp. Może to być
przydatne w niektórych konfiguracjach serwerów VPN.

IpPool ma w pakiecie także aplikację do zarządzania z linii poleceń -
ippoolconfig, służącą do zarządzania i sprawdzania stanu pul adresów.
Dołączona jest także wtyczka pppd, pozwalająca demonowi pppd na
żądanie adresów IP od ippoold.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make} -j1 \
	CC="%{__cc}" \
	SYS_LIBDIR="%{_libdir}" \
	CFLAGS.optimize="%{rpmcflags} $(pkg-config --cflags libtirpc) -fPIC"

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

# API not exported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libusl.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/ippoolconfig
%attr(755,root,root) %{_sbindir}/ippoold
%attr(755,root,root) %{_libdir}/pppd/plugins/ippool.so
%{_mandir}/man1/ippoolconfig.1*
%{_mandir}/man8/ippoold.8*
%attr(754,root,root) /etc/rc.d/init.d/ippoold
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ippoold
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ippoold.conf

# TODO: -devel?
%dir %{_libdir}/ippool
%{_libdir}/ippool/ippool_rpc.x
%{_mandir}/man4/ippool_rpc.4*
