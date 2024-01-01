#!/bin/bash

# SPDX-FileCopyrightText: 2023 Aravinth Manivannan <realaravinth@batsense.net>
#
# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: MIT

readonly PROJECT_ROOT=$(pwd)
readonly SOURCE=https://dl.mcaptcha.org/mcaptcha/cli/0.3.0/x86_64-unknown-linux-gnu.tar.gz
readonly BIN_PATH=tmp/cli/mcaptcha-cli
readonly TARBALL=mcaptcha-cli.tar.gz


download() {
	if [ ! -e $BIN_PATH ];
	then
		mkdir -p tmp/cli
		cd tmp/cli/
		wget $SOURCE --quiet --output-document=$TARBALL $SOURCE
		tar -xvzf $TARBALL > /dev/null
		rm $TARBALL
		echo "[*] Downloaded mCaptcha CLI"
		mv build/x86_64-unknown-linux-gnu/mcaptcha-cli .
		rm -rf build/
		cd $PROJECT_ROOT
	fi
}

# 1: widget URI
gen_pow() {
	$BIN_PATH widget-url $2 | cut -d ':' -f 2 | tr -d ' '
}

$1 $@
