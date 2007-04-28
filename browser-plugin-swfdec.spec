%define		_realname	swfdec-mozilla
%define		_pluginname	libswfdecmozilla
Summary:	Flash player for webbrowsers
Summary(pl.UTF-8):	Odtwarzacz plików w formacie Flash dla przeglądarek internetowych
Name:		browser-plugin-swfdec
Version:	0.4.4
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://swfdec.freedesktop.org/download/swfdec-mozilla/0.4/%{_realname}-%{version}.tar.gz
# Source0-md5:	7d546ac5cc296e58198bb53ccb977021
Patch0:		%{name}-xulrunner.patch
URL:		http://swfdec.freedesktop.org/wiki/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	swfdec-devel >= 0.4.4
BuildRequires:	xulrunner-devel
Requires:	browser-plugins >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package delivers a video/audio player plugin for web browsers.

%description -l pl.UTF-8
Ta paczka dostarcza wtyczki odtwarzacza wideo/audio dla przeglądarek
internetowych.

%prep
%setup -q -n %{_realname}-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
CPPFLAGS="-I%{_includedir}/xulrunner"
export CPPFLAGS
%configure \
	--disable-static \
	--prefix=%{_browserpluginsdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_browserpluginsdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_libdir}/xulrunner/plugins/*.so $RPM_BUILD_ROOT%{_browserpluginsdir}
rm -rf $RPM_BUILD_ROOT%{_libdir}/xulrunner

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_browserpluginsdir}/%{_pluginname}.so
