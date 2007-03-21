# TODO
# - browser plugins v2 (see template-browser-plugin.spec)
%define		_realname	swfdec-mozilla
%define		_pluginname	libswfdecmozilla
Summary:	Flash player for webbrowsers
Summary(pl.UTF-8):	Odtwarzacz plików w formacie Flash dla przeglądarek internetowych
Name:		browser-plugin-swfdec
Version:	0.4.2
Release:	0.1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://swfdec.freedesktop.org/download/swfdec-mozilla/0.4/%{_realname}-%{version}.tar.gz
# Source0-md5:	55de4eb6d2b7820c56eac3520c8f1734
Patch0:		%{name}-xulrunner.patch
URL:		http://swfdec.freedesktop.org/wiki/
BuildRequires:	swfdec-devel >= 0.4.2
BuildRequires:	rpmbuild(macros) >= 1.236
Requires:	browser-plugins(%{_target_base_arch})
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# directory where you store the plugin
%define		_plugindir	%{_libdir}/browser-plugins

# use macro, otherwise extra LF inserted along with the ifarch
%define	browsers xulrunner, mozilla, mozilla-firefox, mozilla-firefox-bin, konqueror, opera, seamonkey

%description
This package delivers a video/audio player plugin for web browsers.

Supported browsers: %{browsers}.

%description -l pl.UTF-8
Ta paczka dostarcza wtyczki odtwarzacza wideo/audio dla przeglądarek
internetowych.

Obsługiwane przeglądarki: %{browsers}.

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
	--prefix=%{_plugindir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_plugindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_libdir}/xulrunner/plugins/*.so $RPM_BUILD_ROOT%{_plugindir}
rm -rf $RPM_BUILD_ROOT%{_libdir}/xulrunner

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- xulrunner
%nsplugin_install -d %{_libdir}/xulrunner/plugins %{_pluginname}.so

%triggerin -- mozilla-firefox
%nsplugin_install -d %{_libdir}/mozilla-firefox/plugins %{_pluginname}.so

%triggerun -- mozilla-firefox
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox/plugins %{_pluginname}.so

%triggerin -- mozilla-firefox-bin
%nsplugin_install -d %{_libdir}/mozilla-firefox-bin/plugins %{_pluginname}.so

%triggerun -- mozilla-firefox-bin
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox-bin/plugins %{_pluginname}.so

%triggerin -- mozilla
%nsplugin_install -d %{_libdir}/mozilla/plugins %{_pluginname}.so

%triggerun -- mozilla
%nsplugin_uninstall -d %{_libdir}/mozilla/plugins %{_pluginname}.so

%triggerin -- opera
%nsplugin_install -d %{_libdir}/opera/plugins %{_pluginname}.so

%triggerun -- opera
%nsplugin_uninstall -d %{_libdir}/opera/plugins %{_pluginname}.so

%triggerin -- konqueror
%nsplugin_install -d %{_libdir}/kde3/plugins/konqueror %{_pluginname}.so

%triggerun -- konqueror
%nsplugin_uninstall -d %{_libdir}/kde3/plugins/konqueror %{_pluginname}.so

%triggerin -- seamonkey
%nsplugin_install -d %{_libdir}/seamonkey/plugins %{_pluginname}.so

%triggerun -- seamonkey
%nsplugin_uninstall -d %{_libdir}/seamonkey/plugins %{_pluginname}.so

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_plugindir}/%{_pluginname}.so
