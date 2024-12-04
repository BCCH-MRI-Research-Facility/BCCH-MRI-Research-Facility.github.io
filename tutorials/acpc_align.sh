#!/bin/sh

Usage() {
    echo ""
    echo "Usage: acpc_align subjectbrain.nii.gz -a x y z -p x y z"
    echo ""
    echo "-a AC coordinates in voxel space (e.g. -a 89 110 200)"
    echo "-p PC coordinates in voxel space (e.g. -a 89 75 188)" 
    exit 1
}

[ "$1" = "" ] && Usage

brain=$1
shift
while [ ! -z "$1" ]
do
  case "$1" in
	-a) acx=$2;acy=$3;acz=$4;shift;shift;shift;;
	-p) pcx=$2;pcy=$3;pcz=$4;shift;shift;shift;;
	*) break;;
  esac
  shift
done

[ "$brain" = "" ] && Usage
[ "$acx" = "" ] && Usage
[ "$acy" = "" ] && Usage
[ "$acz" = "" ] && Usage
[ "$pcx" = "" ] && Usage
[ "$pcy" = "" ] && Usage
[ "$pcz" = "" ] && Usage

#XROTATION

X=`echo "$acy-$pcy" | bc -l`
Y=`echo "$acz-$pcz" | bc -l`
tanth=`echo "$Y / $X" | bc -l`
th=`echo "a ($tanth)" | bc -l`
th=`echo "$th * -1" | bc -l`

costh=`echo "c ($th)" | bc -l`
sinth=`echo "s ($th)" | bc -l`
negsinth=`echo "$sinth * -1" | bc -l`

newacy=`echo "$acy * $costh - $acz * $sinth" | bc -l`
newacz=`echo "$acy * $sinth + $acz * $costh" | bc -l`

transy=`echo "$acy - $newacy" | bc -l`
transz=`echo "$acz - $newacz" | bc -l`

echo "1 0 0 0" > .rotx.mat
echo "0 $costh $negsinth $transy" >> .rotx.mat
echo "0 $sinth $costh $transz" >> .rotx.mat
echo "0 0 0 1" >> .rotx.mat

pcy=`echo "$pcy * $costh - $pcz * $sinth + $transy" | bc -l`

#ZROTATION

X=`echo "$acy-$pcy" | bc -l`
Y=`echo "$acx-$pcx" | bc -l`
tanth=`echo "$Y / $X" | bc -l`
th=`echo "a ($tanth)" | bc -l`

costh=`echo "c ($th)" | bc -l`
sinth=`echo "s ($th)" | bc -l`
negsinth=`echo "$sinth * -1" | bc -l`

newacx=`echo "$acx * $costh - $acy * $sinth" | bc -l`
newacy=`echo "$acx * $sinth + $acy * $costh" | bc -l`

transx=`echo "$acx - $newacx" | bc -l`
transy=`echo "$acy - $newacy" | bc -l`

echo "$costh $negsinth 0 $transx" > .rotz.mat
echo "$sinth $costh 0 $transy" >> .rotz.mat
echo "0 0 1 0" >> .rotz.mat
echo "0 0 0 1" >> .rotz.mat

$FSLDIR/bin/convert_xfm -omat .rotxz.mat -concat .rotz.mat .rotx.mat
$FSLDIR/bin/flirt -in $brain -applyxfm -init .rotxz.mat -out acpc_$brain -paddingsize 0.0 -interp trilinear -ref $brain
rm .rot*.mat
