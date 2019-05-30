"""
Author: Muhammad Umar Riaz
"""
import os
import numpy as np
import random
import argparse
import tools as myTools
from svg.path import parse_path
from xml.dom import minidom

parser = argparse.ArgumentParser()

parser.add_argument('--dataAugN', type=int, default=5, help='Number of augmented samples required')

parser.add_argument('--inDir', type=str, default='./Input/', help='Input directory containing TU Berlin style data with transformed values')
parser.add_argument('--outDir', type=str, default='./Output/', help='Output directory')

parser.add_argument('--transXVar', type=float, default=5.0, help='Translation along x axis - max absolute value')
parser.add_argument('--transYVar', type=float, default=5.0, help='Translation along y axis - max absolute value')

parser.add_argument('--rotateVar', type=int, default=7, help='Degrees of rotation - max absolute value')

parser.add_argument('--scaleXVar', type=float, default=0.07, help='Scale along x axis - max absolute value')
parser.add_argument('--scaleYVar', type=float, default=0.07, help='Scale along y axis - max absolute value')

parser.add_argument('--skewXVar', type=float, default=3, help='Skew along x axis - max absolute value')
parser.add_argument('--skewYVar', type=float, default=3, help='Skew along y axis - max absolute value')

parser.add_argument('--pathXVar', type=int, default=7, help='Path jittering along x axis - max absolute value')
parser.add_argument('--pathYVar', type=int, default=7, help='Path jittering along y axis - max absolute value')

parser.add_argument('--curveXVar', type=int, default=4, help='Curve jittering along x axis - max absolute value')
parser.add_argument('--curveYVar', type=int, default=4, help='Curve jittering along y axis - max absolute value')

parser.add_argument('--strokeWidth', type=int, default=3, help='Stroke width in output svg files')

args = parser.parse_args()

if not os.path.exists(args.outDir):
    os.makedirs(args.outDir)

dataList = myTools.folder2files(args.inDir, format='.svg')

for inputIdx, svgFileName in enumerate(dataList):
    print(str(inputIdx+1) + " / " + str(len(dataList)))

    outDirFinal = args.outDir + svgFileName.split("/")[-1][:-4]

    if not os.path.exists(outDirFinal):
        os.makedirs(outDirFinal)

    for dataAugIdx in range(args.dataAugN):

        svgFile = minidom.parse(svgFileName)

        ################################################################################
        ## Svg header modification for scale, translation, rotation and skew values.
        ################################################################################

        svgProperties = svgFile.getElementsByTagName("g")[0]
        svgProperties.attributes["stroke-width"].value = str(args.strokeWidth)

        scaleValueX = str(np.float32(1 + random.uniform(-args.scaleXVar,args.scaleXVar)))
        scaleValueY = str(np.float32(1 + random.uniform(-args.scaleYVar,args.scaleYVar)))
        transValueX = str(np.float32(random.uniform(-args.transXVar,args.transXVar)))
        transValueY = str(np.float32(random.uniform(-args.transYVar,args.transYVar)))
        rotateValue = str(np.int32(random.randint(-args.rotateVar,args.rotateVar)))
        skewValueX  = str(np.float32(random.uniform(-args.skewXVar, args.skewXVar)))
        skewValueY  = str(np.float32(random.uniform(-args.skewYVar, args.skewYVar)))
        rotateCenter = str(400)

        attributeStr =  "translate(" + transValueX + "," + transValueY + ") rotate(" + rotateValue + "," + rotateCenter + "," + rotateCenter + ") scale(" + scaleValueX + "," + scaleValueY + ") skewX(" + skewValueX + ") skewY(" + skewValueY + ")"

        transformPar = svgFile.getElementsByTagName("g")[1]
        transformPar.setAttribute("transform", attributeStr)

        ################################################################################
        ## Path and curve jittering.
        ################################################################################

        pathList = svgFile.getElementsByTagName("path")

        for pathIdx, pathEle in enumerate(pathList):

            mypath  = parse_path(pathEle.attributes["d"].value)

            randPathValue = complex(random.randint(-args.pathXVar,args.pathXVar), random.randint(-args.pathYVar,args.pathYVar))

            for pathEleIdx, pathEleCurve in enumerate(mypath):

                randCurveValue = complex(random.randint(-args.curveXVar,args.curveXVar), random.randint(-args.curveYVar,args.curveYVar))

                if type(pathEleCurve).__name__ == 'CubicBezier':
                    pathEleCurve.control1 = pathEleCurve.control1 + randPathValue + randCurveValue
                    pathEleCurve.control2 = pathEleCurve.control2 + randPathValue + randCurveValue

                if pathIdx == 0 and pathEleIdx == 0:
                    pathEleCurve.end = pathEleCurve.end + randPathValue
                elif pathIdx == len(pathList)-1 and pathEleIdx == len(mypath)-1:
                    pathEleCurve.start = pathEleCurve.start + randPathValue
                else:
                    pathEleCurve.start = pathEleCurve.start + randPathValue
                    pathEleCurve.end = pathEleCurve.end + randPathValue

            pathEle.attributes["d"].value = mypath.d()

        with open(outDirFinal + "/" + str(dataAugIdx) + ".svg", "w") as f:
            dom_string = svgFile.toprettyxml(indent='\r')
            dom_string = os.linesep.join([s for s in dom_string.splitlines() if s.strip()])
            f.write(dom_string)