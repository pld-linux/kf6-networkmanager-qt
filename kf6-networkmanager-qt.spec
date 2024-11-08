#
# Conditional build:
%bcond_with	tests		# build without tests
#
%define		kdeframever	6.8
%define		qtver		5.15.2
%define		kfname		networkmanager-qt
Summary:	Qt wrapper for NetworkManager DBus API
Name:		kf6-%{kfname}
Version:	6.8.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	c811350927525bf652782afa92af26c6
URL:		http://www.kde.org/
BuildRequires:	NetworkManager-devel
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt wrapper for NetworkManager DBus API.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{_datadir}/qlogging-categories6/networkmanagerqt.categories
%attr(755,root,root) %{_libdir}/libKF6NetworkManagerQt.so.*.*.*
%ghost %{_libdir}/libKF6NetworkManagerQt.so.6
%{_datadir}/qlogging-categories6/networkmanagerqt.renamecategories
%dir %{_libdir}/qt6/qml/org/kde/networkmanager
%{_libdir}/qt6/qml/org/kde/networkmanager/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/networkmanager/libnetworkmanagerqtqml.so
%{_libdir}/qt6/qml/org/kde/networkmanager/networkmanagerqtqml.qmltypes
%{_libdir}/qt6/qml/org/kde/networkmanager/qmldir


%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6NetworkManagerQt.so
%{_includedir}/KF6/NetworkManagerQt
%{_libdir}/cmake/KF6NetworkManagerQt
