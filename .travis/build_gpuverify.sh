#!/bin/bash
set -ev

cd ${GPUVERIFY_DIR}
nuget restore GPUVerify.sln
msbuild /m /p:Configuration=Release \
  /p:CodeAnalysisRuleSet=$PWD/StyleCop.ruleset GPUVerify.sln
cp .travis/gvfindtools.travis_build_and_test.py gvfindtools.py
