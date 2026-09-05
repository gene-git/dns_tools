#
# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
#

project('dns_tools', ['c'],
  version: files('src/version.txt'),
  meson_version: '>=1.10.0',
  default_options: [
    'c_std=c23',
    'warning_level=3',
    'b_pie=true',
    'prefix=/usr',
    'mandir=share/man',
    ],
)

d_etc = get_option('sysconfdir')
d_lib = get_option('libdir')
d_bin = get_option('bindir')
d_man = get_option('mandir')
d_share = get_option('datadir')

py_mod = import('python')
py = py_mod.find_installation(pure: false)
src_root = meson.project_source_root()
py_dep = py.dependency(embed: true)

inc_dir = []
lib_sources = []

#
# top-level files
#

#
# Python submodules
#
subdir('src/dns_tools')

#
# Deps
#

#
# Executables
#
configure_file(
  input: 'src/dns_tools/apps/dns-tool.py',
  output: 'dns-tool',
  copy: true,
  install_dir: d_bin,
  install_mode: 'rwxr-xr-x'
)

configure_file(
  input: 'src/dns_tools/apps/dns-prod-push.py',
  output: 'dns-prod-push',
  copy: true,
  install_dir: d_bin,
  install_mode: 'rwxr-xr-x'
)

configure_file(
  input: 'src/dns_tools/apps/dns-serial-bump.py',
  output: 'dns-serial-bump',
  copy: true,
  install_dir: d_bin,
  install_mode: 'rwxr-xr-x'
)

#
# Install
#

s_license = 'src/data/license'
s_changelog = 'src/data/changelog'
s_docs = 'src/data/docs'
s_scripts = 'src/scripts'
s_etc = 'src/data/etc'
manual = 'dns-tools.pdf'

# 
# /etc/dns_tools
# 
install_data(
  [
    s_etc / 'conf.d/config.sample',
  ],
  install_dir: d_etc / 'dns_tools/conf.d'
)

install_data(
  [
    s_etc / 'cron/dnssec-roll.cron',
  ],
  install_dir: d_etc / 'dns_tools/cron'
)

install_data(
  [
    s_scripts / 'gen-hmac.sh',
    s_scripts / 'resign.sh',
    s_scripts / 'zsk-roll-1.sh',
    s_scripts / 'zsk-roll-2.sh',
  ],
  install_dir: d_etc / 'dns_tools/scripts'
)


# 
# /usr/share/dns_tools/docs
# 
install_data(
  [
    s_docs / manual,
  ],
  install_dir: d_share / 'dns_tools/docs'
)

install_subdir(
  [
    s_docs / 'html',
  ],
  install_dir: d_share / 'dns_tools/docs',
  strip_directory: false
)

# 
# /usr/share/dns_tools 
# 
install_data(
  [
    'README.rst',
    s_changelog / 'Changelog.rst',
    'packaging/Changelog',
  ],
  install_dir: d_share / 'dns_tools'
)

# 
# /usr/share/licenses/dns_tools 
# 
install_data(
  [
    s_license / 'License-gpl-2.0.txt',
    s_license / 'License.rst',
  ],
  install_dir: d_share / 'licenses/dns_tools'
)


