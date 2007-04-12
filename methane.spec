%define	name	methane
%define	version	1.4.6
%define	release	%mkrel 8
%define	Summary	Super Methane Brothers

Name:		%{name}
Summary:	%{Summary}
Version:	%{version}
Release:	%{release}
Source0:	http://www.methane.fsnet.co.uk/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		methane-1.4.4-score.patch
Patch1:		methane-1.4.6-deps-mkdir-p.patch

URL:		http://www.methane.fsnet.co.uk/index.html
License:	GPL
Group:		Games/Arcade
BuildRoot:	 %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	zlib-devel libhermes-devel libmikmod-devel
BuildRequires:	clanlib0.6-devel >= 0.6.5 
# (gc) needed because of binary incompatibility of datafiles between versions of clanlib
Requires:	clanlib0.6 = 0.6.5
# Author: rombust@postmaster.co.uk
Conflicts:	methane_new

%description
A bubble bobble like arcade game.

IMPORTANT NOTE: this is a conversion of the Commodore Amiga game. The
author had been given permission by the company (Apache Software Ltd) to
release this game as GPL. However - THE ORIGINAL AMIGA VERSION OF SUPER
METHANE BROTHERS IS STILL A COMMERCIAL GAME IT'S LICENCE HAS NOT CHANGED.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -p1 -b .deps-mkdir-p

%build
cd source/linux
export CXXFLAGS="$RPM_OPT_FLAGS"
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_gamesbindir}
install -m755 source/linux/%{name} -D $RPM_BUILD_ROOT%{_gamesbindir}/%{name}

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=%{Summary}
Comment=A bubble bobble like arcade game
Exec=soundwrapper %{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

chmod a+rx docs

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/games
touch $RPM_BUILD_ROOT%{_localstatedir}/games/%{name}scores
chmod a+w $RPM_BUILD_ROOT%{_localstatedir}/games/%{name}scores

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}
if [ ! -f %{_localstatedir}/games/%{name}scores ]; then
		touch %{_localstatedir}/games/%{name}scores
		chown games.games %{_localstatedir}/games/%{name}scores
		chmod 664 %{_localstatedir}/games/%{name}scores
fi		

%postun
%{clean_menus}

%files
%defattr(644,root,root,755)
%doc authors copying readme history install todo docs/
%defattr(-,root,root)
%attr(2755, root, games) %{_gamesbindir}/%{name}
%attr(664, games, games) %ghost %{_localstatedir}/games/%{name}scores
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


