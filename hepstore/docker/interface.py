import docker
import os


class DockerIF:
    def __init__(self,image="GENERATOR",version="TAG",verbose=False):
        self.IMAGE  = image
        self.TAG    = version
        self.name   = "%s:%s" % (self.IMAGE,self.TAG)
        self.verbose= verbose
        self.client = docker.from_env()
        # check if herwig docker image exist
        if not len(self.client.images.list(name=self.IMAGE))>0:
            print "--%s: pull image" % self.name
            self.client.images.pull(self.IMAGE,tag=self.TAG)
            pass
        pass
    def run(self,args,directory=None,verbose=False):
        containername = "%s:%s" % (self.IMAGE,self.TAG)
        try:
            folder    = os.path.realpath(directory)
            volume    = {folder: {'bind': '/UserVolume', 'mode': 'rw'}}
            pass
        except Exception:
            volume    = {}
            pass
        container = self.client.containers.run(containername,command=args,volumes=volume,working_dir='/UserVolume',detach=True)
        for i,line in enumerate(container.logs(stdout=True,stderr=True,stream=True)):
            if self.verbose:
                print "%i: %s" % (i,line.strip())
                pass
            pass
        container.remove()
        pass
    pass # acousto

