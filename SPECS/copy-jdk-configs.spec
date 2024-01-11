%global project copy_jdk_configs
%global file %{project}.lua
%global fixFile %{project}_fixFiles.sh
%global rpm_state_dir %{_localstatedir}/lib/rpm-state

Name:    copy-jdk-configs

# hash relevant to version tag
%global  htag 88d3ed89f30d8b0eb4877d860fa8d951f224f156
Version: 4.0
Release: 2%{?dist}
Summary: JDKs configuration files copier

License:  BSD
URL:      https://pagure.io/%{project}
Source0:  %{URL}/blob/%{htag}/f/%{file}
Source1:  %{URL}/blob/%{htag}/f/LICENSE
Source2:  %{URL}/blob/%{htag}/f/%{fixFile}

# we need to duplicate msot of the percents in that script so they survive rpm expansion (even in that sed they have to be duplicated)
%global pretrans_install %(cat %{SOURCE0} | sed s/%%/%%%%/g | sed s/\\^%%%%/^%%/g) 

BuildArch: noarch

Requires: lua
#Requires: lua-posix
# rh1965305 - copy-jdk-configs script uses find and xargs but RPM does not depend on them
Requires: findutils
OrderWithRequires: findutils

%description
Utility script to transfer JDKs configuration files between updates or for
archiving. With script to fix incorrectly created rpmnew files

%prep
cp -a %{SOURCE1} .


%build
#blob

%pretrans -p <lua>
function createPretransScript()
-- the sript must be available during pretrans, so multiply it to tmp
  os.execute("mkdir -p %{rpm_state_dir}")
  temp_path="%{rpm_state_dir}/%{file}"
-- print("generating " .. temp_path)
  file = io.open(temp_path, "w")
  file:write([[%{pretrans_install}]])
  file:close()
end

-- in netinst, the above call may fail. pcall should save instalation (as there is nothing to copy anyway)
-- https://bugzilla.redhat.com/show_bug.cgi?id=1295701
-- todo, decide whether to check for {rpm_state_dir} and skip on not-existing, or keep creating
if pcall(createPretransScript) then
-- ok
else
--  print("Error running %{name} pretrans.")
end

%install
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}
cp -a %{SOURCE0} $RPM_BUILD_ROOT/%{_libexecdir}/%{file}
chmod 644 $RPM_BUILD_ROOT/%{_libexecdir}/%{file}
cp -a %{SOURCE2} $RPM_BUILD_ROOT/%{_libexecdir}/%{fixFile}

%posttrans
# remove file created in pretrans
# echo "removing %{rpm_state_dir}/%{file}" || :
rm "%{rpm_state_dir}/%{file}" 2> /dev/null || :

%files 
%{_libexecdir}/%{file}
%{_libexecdir}/%{fixFile}
%license LICENSE

%changelog
* Tue Jun 08 2021 Jiri Vanek <jvanek@redhat.com> - 4.0-2
- commented out requires lua-posix, it was always commented out in el8, never in fedora. IDK
- Resolves: rhbz#1953923

* Tue Jun 08 2021 Jiri Vanek <jvanek@redhat.com> - 4.0-1
- rebased to 4.0
- Resolves: rhbz#1953923

* Thu Jul 09 2020 Jiri Vanek <jvanek@redhat.com> - 3.7-3
- added link to http://hydra.brq.redhat.com:8080/view/c~j~c/#projectstatus
- removed source check from test.yaml
- added gating.yaml
- Resolves: rhbz#1855374

* Thu Jul 09 2020 Jiri Vanek <jvanek@redhat.com> - 3.7-3
- added gatnig placeholder
- Resolves: rhbz#1855374

* Thu Jul 09 2020 Jiri Vanek <jvanek@redhat.com> - 3.7-2
- added nss.fips.cfg to cared files
- Resolves: rhbz#1855374

* Wed May 02 2018 Jiri Vanek <jvanek@redhat.com> - 3.7-1
- udpated to latst relase
- configurable blacklist
- listed all java keystores

* Wed May 02 2018 Jiri Vanek <jvanek@redhat.com> - 3.3-12
- blackidrs put on single line

* Wed May 02 2018 Jiri Vanek <jvanek@redhat.com> - 3.3-11
- added more files to balcklist based on oralce and ibm jdks

* Mon Apr 30 2018 Jiri Vanek <jvanek@redhat.com> - 3.3-10
- added javaws.policy and blacklist
- fixed rhbz#1541838

* Tue Apr 03 2018 Jiri Vanek <jvanek@redhat.com> - 3.3-5
- fixed rhbz#1541838

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 18 2017 Jiri Vanek <jvanek@redhat.com> - 3.3-2
- added another subdirs for policies files

* Wed Oct 18 2017 Jiri Vanek <jvanek@redhat.com> - 3.3-1
- handled new paths for policies files

* Thu Oct 05 2017 Jiri Vanek <jvanek@redhat.com> - 3.1-1
- moved to newest release 3.1 whcih conf and lib/security as directories

* Thu Oct 05 2017 Jiri Vanek <jvanek@redhat.com> - 3.0-1
- moved to newest release 3.0 whcih support linked configs

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 22 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3
- updated to latest head

* Wed Feb 22 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2
- added "jre/lib/security/blacklisted.certs" to cared files

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Jiri Vanek <jvanek@redhat.com> - 2.1-1
- moved to newest release 2.1

* Fri Jan 20 2017 Jiri Vanek <jvanek@redhat.com> - 2.0-1
- moved to new upstream at pagure.io
- moved to newest release 2.0
- added new script of copy_jdk_configs_fixFiles.sh 
- copy_jdk_configs.lua  aligned to it

* Tue Aug 09 2016 Jiri Vanek <jvanek@redhat.com> - 1.2-1
- updated to 1,3 which fixing nss minor issue

* Tue Jul 12 2016 Jiri Vanek <jvanek@redhat.com> - 1.1-5
- posttrans silenced, the error is appearing only in state, when there is nothing to copy

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Jiri Vanek <jvanek@redhat.com> - 1.1-3
- pretrasn lua call now done in pcall (protected call)
- also posttrans now always return 0

* Wed Dec 16 2015 Jiri Vanek <jvanek@redhat.com> - 1.1-2
- package now "installs" also during pretrans, so pretrasn scripts can use it
- pretrasn "install" is removed in postrans

* Wed Nov 25 2015 Jiri Vanek <jvanek@redhat.com> - 1.1-1
- initial package
