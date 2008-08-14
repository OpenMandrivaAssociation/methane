%define	name	methane
%define	version	1.4.8
%define	release	%mkrel 4
%define	Summary	Super Methane Brothers

Name:		%{name}
Summary:	%{Summary}
Version:	%{version}
Release:	%{release}
Source0:	http://www.methane.fsnet.co.uk/%{name}-%{version}.tgz
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		methane-1.4.7-score.patch
Patch1:		methane-1.4.7-deps-mkdir-p.patch

URL:		http://methane.sourceforge.net/
License:	GPLv2+
Group:		Games/Arcade
BuildRoot:	 %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	zlib-devel libhermes-devel libmikmod-devel
BuildRequires:	clanlib0.8-devel
Obsoletes:	methane_new

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
export CXXFLAGS="%{optflags}"
%make

%install
rm -rf %{buildroot}
install -m755 source/linux/%{name} -D %{buildroot}%{_gamesbindir}/%{name}

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

install -d %{buildroot}%{_datadir}/applications
cat <<EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=%{Summary}
Comment=A bubble bobble like arcade game
Exec=soundwrapper %{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

chmod a+rx docs

mkdir -p %{buildroot}%{_localstatedir}/lib/games
touch %{buildroot}%{_localstatedir}/lib/games/%{name}scores
chmod a+w %{buildroot}%{_localstatedir}/lib/games/%{name}scores

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 200900
%{update_menus}
%endif
if [ ! -f %{_localstatedir}/lib/games/%{name}scores ]; then
		touch %{_localstatedir}/lib/games/%{name}scores
		chown games.games %{_localstatedir}/lib/games/%{name}scores
		chmod 664 %{_localstatedir}/lib/games/%{name}scores
fi		

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files
%defattr(644,root,root,755)
%doc authors copying readme history install todo docs/
%defattr(-,root,root)
%attr(2755, root, games) %{_gamesbindir}/%{name}
%attr(664, games, games) %ghost %{_localstatedir}/lib/games/%{name}scores
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


