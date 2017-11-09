from glEngine import glmesh


class MESHTYPE:
    CUBE = 'cube'

class mesh_factory:

    def __init__(self):
        pass

    @staticmethod
    def create_meshlist(path, type):
        return glmesh.Mesh('{}/{}.yml'.format(path, type))
