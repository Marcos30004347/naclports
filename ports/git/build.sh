# Copyright (c) 2013 The Native Client Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

EXECUTABLES="git git-remote-http"

BUILD_DIR=${SRC_DIR}
export EXTLIBS+="${NACL_CLI_MAIN_LIB} \
-lppapi_simple -lnacl_io -lppapi -l${NACL_CXX_LIB}"

if [ "${NACL_SHARED}" != "1" ]; then
  # These are needed so that the configure can detect libcurl when statically
  # linked.
  export LIBS="-lcurl -lssl -lcrypto -lz"
  EXTLIBS+=" -lglibc-compat"
fi

if [ ${OS_NAME} = "Darwin" ]; then
  # gettext (msgfmt) doesn't exist on darwin by default.  homebrew installs
  # it to /usr/local/opt/gettext, and we need it to be in the PATH when
  # building git
  export PATH=${PATH}:/usr/local/opt/gettext/bin
fi

ConfigureStep() {
  ChangeDir ${SRC_DIR}
  autoconf

  if [ "${NACL_LIBC}" = "newlib" ]; then
    NACLPORTS_CPPFLAGS+=" -I${NACLPORTS_INCLUDE}/glibc-compat"
    LIBS+=" -lglibc-compat"
  fi

  if [ "${NACL_LIBC}" = "glibc" ]; then
    # Because libcrypto.a needs dlsym we need to add this explicitly.
    # This is not normally needed when libcyrpto is a shared library.
    NACLPORTS_LDFLAGS+=" -ldl"
  fi

  DefaultConfigureStep
}

BuildStep() {
  if [ "${NACL_LIBC}" = "newlib" ]; then
    export NO_RT_LIBRARY=1
  fi
  export CROSS_COMPILE=1
  SetupCrossEnvironment
  ChangeDir ${SRC_DIR}
  # Git's build doesn't support building outside the source tree.
  # Do a clean to make rebuild after failure predictable.
  LogExecute make clean
  export CCLD=${CXX}
  export NEEDS_CRYPTO_WITH_SSL=YesPlease
  DefaultBuildStep
}

InstallStep() {
  return
}

PublishStep() {
  PublishByArchForDevEnv
}
