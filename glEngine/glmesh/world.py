from glEngine.glmesh.mesh import *
import yaml

class World:

    def __init__(self, conf_path):
        self.world_mesh = []
        self.index = 0
        try:
            with open(conf_path) as w:
                self.configuration = yaml.load(w)
        except IOError as ie:
            print(ie)
            exit(1)
        except yaml.YAMLError as ye:
            print (ye)
            exit(1)
        print(self.configuration)
        self.__setup()

    def __setup(self):
        for obj in self.configuration['objects']:
            m = Mesh('shapes/{}.yml'.format(obj['name']))
            self.world_mesh.append(m)
        self.max = len(self.world_mesh) - 1

    #Make class iterable
    def __iter__(self):
        return self

    def __next__(self):
        if self.index > self.max:
            self.index = 0
            raise StopIteration
        else:
            self.index += 1
            return self.world_mesh[self.index -1]
