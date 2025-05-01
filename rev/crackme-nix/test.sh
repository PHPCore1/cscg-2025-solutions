#!/usr/bin/env bash
docker run --rm --ulimit stack=2147483648:2147483648 -v "$(pwd)/crackme.nix:/crackme.nix" nixos/nix:2.26.1 \
  bash -c "nix-instantiate --option max-call-depth 1000000000 --eval /crackme.nix --argstr flag '$1'"