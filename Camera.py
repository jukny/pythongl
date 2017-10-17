import Matrixop as mo


class Camera:
    def __init__(self, conf):
        self.perspective = mo.perspective(conf['fow'], eval(conf['aspect_ratio']), 0.1, 100.0)
        self.target = mo.translate(conf['eye'])
        #self.lookat = mo.lookat(mo.vec(conf['eye']), mo.vec(conf['target']), mo.vec(conf['up']))
