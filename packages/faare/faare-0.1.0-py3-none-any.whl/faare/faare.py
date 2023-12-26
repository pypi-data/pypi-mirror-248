import ase.io
import os
import numpy as np
import json

ROOT = os.path.dirname(__file__)

class Faare:
    def __init__(self):
        pass

    def build_render(self, 
                     filename:str,
                     manifestout:str,
                     manifestin:str=None,
                     verbose:bool=False):
        if not os.path.exists(filename):
            raise Exception('Invalid path: %s')
        
        # grab structure from file
        struc = ase.io.read(filename)

        # get atomic data from structure
        unitcell = np.array(struc.get_cell()[:])
        atoms = struc.get_chemical_symbols()
        positions = struc.get_positions()

        # start with default json files
        with open(os.path.join(ROOT, 'settings', 'settings.json'), 'r') as f:
            manifest = json.load(f)
        with open(os.path.join(ROOT, 'settings', 'atom_colors.json'), 'r') as f:
            manifest.update(json.load(f))
        with open(os.path.join(ROOT, 'settings', 'atom_radii.json'), 'r') as f:
            manifest.update(json.load(f))
        with open(os.path.join(ROOT, 'settings', 'bonds.json'), 'r') as f:
            manifest.update(json.load(f))

        # encode unit cell and atoms in dictionary
        manifest['unitcell'] = [[unitcell[i,j]  for j in range(0,3)] for i in range(0,3)]
        manifest['atoms'] = []
        for a,p in zip(atoms, positions):
            manifest['atoms'].append((a, (p[0], p[1], p[2])))
        
        # auto-orient camera
        rt = unitcell @ np.array([1.0, 1.0, 0.0])
        scale = max(rt[0], rt[1])
        camera_location = unitcell @ np.array([0.5, 0.5, 0])
        camera_location += np.array([0, 0, 100])
        manifest["camera_location"] = [camera_location[i] for i in range(3)]
        manifest["camera_scale"] = scale * 1.1

        # overwrite any items from a manifest in file
        if manifestin is not None:
            with open(manifestin, 'r') as f:
                manifest.update(json.load(f))

        # store as json file
        with open(manifestout, 'w') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=4)

    def execute_render(self, manifest:str):
        pass