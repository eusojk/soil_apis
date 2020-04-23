#!/bin/bash
if ! [ -x "$(command -v gfortran)" ]; then
  echo 'Error: gfortran is not installed. Please install before you proceed' >&2
  exit 1
fi

if ! [ -x "$(command -v make)" ]; then
  echo 'Error: gfortran is not installed. Please install before you proceed' >&2
  exit 1
fi

echo "Started compiling..."

rootdir=$PWD
soilapidir="$rootdir/soilapis"
dotsolexec="$soilapidir/dotSolAPI2.a"
mktxtexec="$soilapidir/make_texture.a"
dotsoldir="$rootdir/soilapis/f90/dotsol"
texturdir="$rootdir/soilapis/f90/texture"

## compile dotSolApi with gfortran and move to parent dir
cd $dotsoldir
make clean
make all
cp dotSolAPI2.a $dotsolexec

cd $texturdir
make clean
make all
cp make_texture.a $mktxtexec

echo "done compiling the fortran code"
