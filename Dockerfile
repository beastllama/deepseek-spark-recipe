# Source build for the published overlay; no weights, Keys, Engram or kernel kit.
# Mirrors the compiler invocation in the pinned Mia recipe's zig/Dockerfile.
ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:26.07-py3
FROM ${BASE_IMAGE}
ARG ZIG_VERSION=0.17.0
ARG ZIG_ARCHIVE_SHA256=9e8d11661d4ae3bd57702a3832781e23ad151dde5798e16a5ccd503f65234ff8
RUN curl --fail --location --retry 3 --connect-timeout 20 --max-time 300 \
      "https://ziglang.org/download/${ZIG_VERSION}/zig-aarch64-linux-${ZIG_VERSION}.tar.xz" -o /tmp/zig.tar.xz \
    && echo "${ZIG_ARCHIVE_SHA256}  /tmp/zig.tar.xz" | sha256sum -c - \
    && mkdir /opt/zig && tar -xJf /tmp/zig.tar.xz -C /opt/zig --strip-components=1 \
    && rm /tmp/zig.tar.xz
COPY tensorfold /tensorfold
WORKDIR /tensorfold
RUN /opt/zig/zig build -Dnvcc=/usr/local/cuda/bin/nvcc -Dsm=121 \
      -Doptimize=ReleaseFast -j2 install native fatbins --summary all --prefix /opt/tensorfold \
    && mkdir -p /opt/tensorfold/share/doc/tensorfold \
    && cp LICENSE NOTICE THIRD_PARTY_NOTICES.md /opt/tensorfold/share/doc/tensorfold/ \
    && cp -r LICENSES /opt/tensorfold/share/doc/tensorfold/
ENV PATH=/opt/tensorfold/native/bin:/opt/tensorfold/bin:${PATH}
