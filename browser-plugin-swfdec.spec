%define		realname	swfdec-mozilla
Summary:	Flash player for webbrowsers
Summary(pl.UTF-8):	Odtwarzacz plików w formacie Flash dla przeglądarek internetowych
Name:		browser-plugin-swfdec
Version:	0.6.4
Release:	2
License:	LGPL v2.1+
Group:		X11/Applications/Multimedia
Source0:	http://swfdec.freedesktop.org/download/swfdec-mozilla/0.6/%{realname}-%{version}.tar.gz
# Source0-md5:	dc0fb84b5e5c7540ae1231eb04109f0e
URL:		http://swfdec.freedesktop.org/wiki/
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake >= 1.6
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	swfdec-gtk-devel = %{version}
Requires:	browser-plugins >= 2.0
Requires:	swfdec-gtk = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package delivers a video/audio player plugin for web browsers.

%description -l pl.UTF-8
Ten pakiet dostarcza wtyczkę odtwarzacza wideo/audio dla przeglądarek
internetowych.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--with-plugin-dir=%{_browserpluginsdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_browserpluginsdir}/*.la

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
%attr(755,root,root) %{_browserpluginsdir}/libswfdecmozilla.so
