FROM ubuntu:24.04

ENV AWSCLI_VERSION=2.36.19
ENV TERRAFORM_VERSION=1.15.7
ENV UV_VERSION=0.12.1

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      git \
      unzip \
      zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    export ARCHITECTURE=$(dpkg --print-architecture) && \
    export ARCHITECTUREX=$(echo "$ARCHITECTURE" | sed 's/amd64/x86_64/g' | sed 's/arm64/arm/g') && \
    # AWS CLI
    mkdir -p /tmp/awscli && \
    curl --proto "=https" --tlsv1.2 -L "https://awscli.amazonaws.com/awscli-exe-linux-${ARCHITECTUREX}-${AWSCLI_VERSION}.zip" -o /tmp/awscli/awscliv2.zip && \
    unzip /tmp/awscli/awscliv2.zip -d /tmp/awscli && \
    /tmp/awscli/aws/install && \
    rm -rf /tmp/awscli && \
    # Terraform
    mkdir -p /tmp/terraform && \
    curl --proto "=https" --tlsv1.2 -L "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${ARCHITECTURE}.zip" -o "/tmp/terraform/terraform_${TERRAFORM_VERSION}_linux_${ARCHITECTURE}.zip" && \
    unzip "/tmp/terraform/terraform_${TERRAFORM_VERSION}_linux_${ARCHITECTURE}.zip" -d /tmp/terraform && \
    mv /tmp/terraform/terraform /usr/local/bin/terraform && \
    rm -rf /tmp/terraform && \
    # uv
    if [ "$ARCHITECTURE" = "arm64" ]; then export UV_ARCH="aarch64"; else export UV_ARCH="$ARCHITECTUREX"; fi && \
    mkdir -p /tmp/uv && \
    curl --proto "=https" --tlsv1.2 -L "https://releases.astral.sh/github/uv/releases/download/${UV_VERSION}/uv-${UV_ARCH}-unknown-linux-gnu.tar.gz" -o "/tmp/uv/uv-${UV_ARCH}-unknown-linux-gnu.tar.gz" && \
    tar -xzf "/tmp/uv/uv-${UV_ARCH}-unknown-linux-gnu.tar.gz" -C /tmp/uv && \
    mv "/tmp/uv/uv-${UV_ARCH}-unknown-linux-gnu/uv" /usr/local/bin/uv && \
    rm -rf /tmp/uv
