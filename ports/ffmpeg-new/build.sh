#!/bin/bash
# Copyright (c) 2012 The Native Client Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

EXECUTABLES="ffmpeg ffmpeg_g ffprobe ffprobe_g"

ConfigureStep() {
  SetupCrossEnvironment

  local extra_args=""
  if [ "${NACL_ARCH}" = pnacl ]; then
    extra_args="--cc=pnacl-clang --arch=pnacl"
  elif [ "${NACL_ARCH}" = arm ]; then
    extra_args="--arch=arm"
  else
    extra_args="--arch=x86"
  fi

  ../configure \
    --cross-prefix=${NACL_CROSS_PREFIX}- \
    --arch="${NACL_ARCH}" \
    ${extra_args} \
    --target-os=linux \
    --disable-everything \
    --enable-muxer=webm \
    --enable-encoder=libvpx_vp8,libvorbis \
    --enable-filter=null,scale,resample \
    --disable-yasm \
    --disable-asm \
    --enable-static \
    --enable-cross-compile \
    --enable-protocol=file \
    --enable-libvorbis \
    --enable-libvpx \
    --disable-programs \
    --prefix=${PREFIX} 
}

