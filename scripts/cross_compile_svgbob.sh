#!/bin/bash

# NOTE (mb 2021-09-24):
#   This doesn't work and I don't care anymore.
#   Fuck cross compilation with rust.

cd ../svgbob/

git checkout .
git checkout master
git pull

TAG=$(git tag -l --sort=taggerdate | grep -E "^v[0-9]+\.[0-9]+.[0-9]+$" | sort --version-sort | tail -n 1)
echo $TAG
git checkout $TAG

rustup default nightly
rustup target add x86_64-unknown-linux-gnu
rustup target add x86_64-pc-windows-gnu
rustup target add x86_64-apple-darwin

rustup toolchain install stable-x86_64-pc-windows-gnu
rustup toolchain install x86_64-apple-darwin

cargo build --target x86_64-unknown-linux-gnu --release
cargo build --target x86_64-pc-windows-gnu --release
cargo build --target x86_64-apple-darwin --release

cp target/x86_64-unknown-linux-gnu/release/svgbob \
    ../markdown-svgbob/src/markdown_svgbob/bin/svgbob_$TAG_x86_64-Linux.exe

cp target/x86_64-pc-windows-gnu/release/svgbob \
    ../markdown-svgbob/src/markdown_svgbob/bin/svgbob_$TAG_x86_64-Windows.exe

cp target/x86_64-apple-darwin/release/svgbob \
    ../markdown-svgbob/src/markdown_svgbob/bin/svgbob_$TAG_x86_64-Darwin.exe


# pre 2020 attempt

# sudo apt-get install clang-6.0 libclang1-6.0 libobjc-7-dev libxml2-dev
# sudo ln -s /usr/bin/clang++-6.0 /usr/bin/clang++
# sudo ln -s /usr/bin/clang-6.0 /usr/bin/clang

# cat <<EOF >> $HOME/.cargo/config

# [target.x86_64-apple-darwin]
# linker = "x86_64-apple-darwin15-cc"
# ar = "x86_64-apple-darwin15-ar"

# EOF

# git clone https://github.com/tpoechtrager/osxcross
# cd osxcross/
# wget https://s3.dockerproject.org/darwin/v2/MacOSX10.11.sdk.tar.xz
# mv MacOSX10.11.sdk.tar.xz tarballs/
# sed -i -e 's|-march=native||g' build_clang.sh wrapper/build.sh

# UNATTENDED=yes OSX_VERSION_MIN=10.7 ./build.sh
# sudo mkdir -p /usr/local/osx-ndk-x86
# sudo mv target/* /usr/local/osx-ndk-x86

# cd ../svgbob/svgbob_cli
# export PATH=/usr/local/osx-ndk-x86/bin:$PATH
# export PKG_CONFIG_ALLOW_CROSS=1
# cargo build --target=x86_64-apple-darwin --release
