#!/bin/bash
sudo apt-get install clang-6.0 libclang1-6.0 libobjc-4.8-dev
sudo ln -s /usr/bin/clang++-6.0 /usr/bin/clang++
sudo ln -s /usr/bin/clang-6.0 /usr/bin/clang

rustup target add x86_64-apple-darwin

cat <<EOF >> $HOME/.cargo/config

[target.x86_64-apple-darwin]
linker = "x86_64-apple-darwin15-cc"
ar = "x86_64-apple-darwin15-ar"

EOF

git clone https://github.com/tpoechtrager/osxcross
cd osxcross/
wget https://s3.dockerproject.org/darwin/v2/MacOSX10.11.sdk.tar.xz
mv MacOSX10.11.sdk.tar.xz tarballs/
sed -i -e 's|-march=native||g' build_clang.sh wrapper/build.sh

UNATTENDED=yes OSX_VERSION_MIN=10.7 ./build.sh
sudo mkdir -p /usr/local/osx-ndk-x86
sudo mv target/* /usr/local/osx-ndk-x86

cd ../svgbob/svgbob_cli
export PATH=/usr/local/osx-ndk-x86/bin:$PATH
export PKG_CONFIG_ALLOW_CROSS=1
cargo build --target=x86_64-apple-darwin --release
