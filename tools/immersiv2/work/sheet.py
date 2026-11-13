import sys,glob
from PIL import Image
names=sys.argv[2:]; out=sys.argv[1]
rows=[]
for n in names:
    fs=sorted(glob.glob(f'prev/{n}_*.png'))
    # waehle bis 6 gleichmaessig
    if len(fs)>6: fs=[fs[int(i*(len(fs)-1)/5)] for i in range(6)]
    rows.append([Image.open(f).resize((250,444)) for f in fs])
W=max(len(r) for r in rows)*250; H=len(rows)*444
sh=Image.new('RGB',(W,H),(0,0,0))
for y,r in enumerate(rows):
    for x,im in enumerate(r): sh.paste(im,(x*250,y*444))
sh.save(out)
