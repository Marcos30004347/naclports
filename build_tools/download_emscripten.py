#!/usr/bin/env python
# Copyright 2015 The Native Client Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Download the Emscripten SDK for the current platform.

This script downloads the emscripten tarball and expands it.
It requires gsutil to be in the bin PATH and is currently
supported on Linux and Mac OSX and not windows.

Additional prerequisites include cmake, node.js and Java.
"""

import os
import subprocess
import sys
import tarfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NACLPORTS_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.append(os.path.join(NACLPORTS_ROOT, 'lib'))

import naclports
import naclports.source_package

MIRROR_URL = 'http://storage.googleapis.com/naclports/mirror/emscripten'

EMSDK_SHA1 = '979f2a9f41de3b7057ea9893c663261c44dc7322'
EMSDK_URL = MIRROR_URL + '/emsdk-portable-20150330.tar.gz'

NODEJS_SHA1 = '79880ff2bc95a674bd0701a6dd4ed38f8366db27'
NODEJS_URL = MIRROR_URL + '/node-v0.12.1-linux-x64.tar.gz'

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.dirname(SCRIPT_DIR)
OUT_DIR = os.path.join(SRC_DIR, 'out')
TARGET_DIR = os.path.join(OUT_DIR, 'emscripten_sdk')


def DownloadToCache(url, sha1):
  filename = os.path.basename(url)
  full_name = os.path.join(naclports.paths.CACHE_ROOT, filename)
  if os.path.exists(full_name):
    try:
      naclports.util.VerifyHash(full_name, sha1)
      naclports.Log("Verified cached file: %s" % filename)
      return full_name
    except naclports.util.HashVerificationError:
      naclports.Log("Hash mistmatch on cached download: %s" % filename)

  naclports.DownloadFile(full_name, url)
  naclports.util.VerifyHash(full_name, sha1)
  return full_name


def DownloadAndExtract(url, sha1, target_dir):
  tar_file = DownloadToCache(url, sha1)

  if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

  os.chdir(OUT_DIR)

  # Remove previously extracted archive
  if os.path.exists(target_dir):
    naclports.Log('Cleaning up existing %s...' % target_dir)
    cmd = ['rm', '-rf']
    cmd.append(target_dir)
    subprocess.check_call(cmd)

  # Extract archive
  naclports.Log('Exctacting %s...' % os.path.basename(tar_file))
  if subprocess.call(['tar', 'xf', tar_file]):
    raise naclports.Error('Error unpacking Emscripten SDK')


def main(argv):
  if sys.platform in ['win32', 'cygwin']:
    naclports.Error('Emscripten support is currently not available on Windows.')
    return 1

  DownloadAndExtract(EMSDK_URL, EMSDK_SHA1, 'emsdk_portable')
  DownloadAndExtract(NODEJS_URL, NODEJS_SHA1, 'node-v0.12.1-linux-x64')
  naclports.Log('Emscripten SDK Install complete')
  return 0


if __name__ == '__main__':
  try:
    rtn = main(sys.argv[1:])
  except naclports.Error as e:
    sys.stderr.write('error: %s\n' % str(e))
    rtn = 1
