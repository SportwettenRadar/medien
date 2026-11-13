import sys, subprocess, os, json
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__))
def build_page(name):
    tpl=open(f'{S}/page.html.tpl').read().replace('CFG.js',f'cfg_{name}.js').replace('VID.js',f'{name}.js')
    open(f'{S}/page_{name}.html','w').write(tpl)
def frames(name, times, outdir):
    build_page(name); os.makedirs(outdir,exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
        pg.on('console',lambda m:print('console:',m.text)); pg.on('pageerror',lambda e:print('ERR',e))
        pg.goto(f'file://{S}/page_{name}.html'); pg.wait_for_function('window.ready===true',timeout=20000)
        for t in times:
            pg.evaluate(f'render({t})'); pg.screenshot(path=f'{outdir}/{name}_{t:05.2f}.png')
        b.close()
def video(name, dur, wav, out, fps=30):
    build_page(name); n=int(dur*fps)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror',lambda e:print('ERR',e))
        pg.goto(f'file://{S}/page_{name}.html'); pg.wait_for_function('window.ready===true',timeout=20000)
        ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(fps),'-c:v','mjpeg','-i','-','-i',wav,
          '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r',str(fps),'-af','loudnorm=I=-15:TP=-1.5:LRA=11','-ar','44100','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],stdin=subprocess.PIPE)
        for i in range(n):
            pg.evaluate(f'render({i/fps})'); ff.stdin.write(pg.screenshot(type='jpeg',quality=94))
        ff.stdin.close(); ff.wait(); b.close()
if __name__=='__main__':
    mode=sys.argv[1]; name=sys.argv[2]
    if mode=='frames': frames(name,[float(x) for x in sys.argv[3].split(',')],f'{S}/prev')
    else: video(name,float(sys.argv[3]),sys.argv[4],sys.argv[5])
