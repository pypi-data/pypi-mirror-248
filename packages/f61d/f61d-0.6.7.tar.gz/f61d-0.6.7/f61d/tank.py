from PIL import Image as img
import sys
import numpy as np
from gmpy2 import invert
from tqdm import tqdm

def TANK(imgA,imgB,verbose):
    global tqdm
    if not verbose:
        tqdm = lambda x:x
    siz = imgA.size
    i = img.new("RGBA",siz)
    for w in tqdm(range(siz[0])):
        for h in range(siz[1]):
            try:
                pA = imgA.getpixel((w,h))
                pB = imgB.getpixel((w,h))
                
                #print(pA,pB,end=' ')
                a = 255 - (pA - pB)
                if a == 0:
                    gray = 0
                else:
                    gray = 255 * pB // a
                #print(gray)
                i.putpixel((w,h),(gray,gray,gray,a))
            except:
                pass
            
    return i



def make(imgOuter,imgInner,output,verbose=0):
    # print(imgOuter,imgInner,output,verbose)
    
    imgOuter = img.open(imgOuter)
    imgOuter = imgOuter.convert('L')
    imgInner = img.open(imgInner)
    imgInner = imgInner.convert('L')
    
    a1 = np.array(imgOuter)
    a2 = 255-(255-a1)//2
    img1 = img.fromarray(a2)
    #img1.show()

    #imgInner = img.open("D:\\Pictures\\bh3rd\\2.png").convert('L')
    a2 = np.array(imgInner)
    img2 = img.fromarray(a2//2)
    #img2.show()

    OutputImg = TANK(img1,img2,verbose)
    OutputImg.save(output)
    print(f'Mirage tank saved as {output}')


if __name__ == '__main__':

    import argparse
    import os

    parser = argparse.ArgumentParser(prog='python -m f61d',
                                 description='f61d functions',
                                 allow_abbrev=True)
    
    parser.add_argument('img1', nargs=1,help='superficial image')
    parser.add_argument('img2', nargs=1,help='interior image')
    parser.add_argument('--verbose','-v',
                        dest='verbose',
                        action='store_true',
                    help='Show verbose')
    
    parser.add_argument('-o','--output',
                        dest='output',
                        metavar='',
                        default='output.png',
                        nargs=1,
                        help='Output path')
    
    args = parser.parse_args()
    if os.path.isabs(args.img1[0]):
        outerImg = args.img1[0]
    else:
        outerImg = os.getcwd() + '\\' + args.img1[0]
    if os.path.isabs(args.img2[0]):
        innerImg = args.img2[0]
    else:
        innerImg = os.getcwd() + '\\' + args.img2[0]

    if type(args.output) is list:
        if os.path.isabs(args.output[0]):
            output = args.output[0]
        else:
            output = os.getcwd() + '\\' + args.output[0]
    else:
        output = args.output
    if not output.endswith('.png'):
        output += '.png'
    VB = args.verbose

    # print(outerImg,innerImg,output,VB)
    make(outerImg,innerImg,output,verbose=VB)


