# En __init__.py del paquete que contiene AtomPositionManager
try:
    from sage_lib.partition.PartitionManager import PartitionManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del syss

try:
    from sage_lib.input.structure_handling_tools.AtomPosition import AtomPosition
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing AtomPosition: {str(e)}\n")
    del sys
    
try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

class MoleculeCluster_builder(PartitionManager):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        super().__init__(name=name, file_location=file_location)

        self._molecule_template = {}
        self._density = None
        self._cluster_lattice_vectors = None

    def get_cluster_volume(self, shape:str='box', cluster_lattice_vectors:np.array=None ):
        '''
        '''
        cluster_lattice_vectors = cluster_lattice_vectors if cluster_lattice_vectors is not None else self.cluster_lattice_vectors 
        
        if shape.lower() == 'box':
            return np.abs(np.linalg.det(cluster_lattice_vectors)) * 10**-24
        else:
            print('Undefine shape')

        return volume

    def get_molecules_number_for_target_density(self, density:float=1.0, cluster_volume:float=None, molecules:dict={'H2O':1.0} ) -> dict:
        '''
        '''
        mass_suma = np.sum( [ self._molecule_template[m_name].mass * m_fraction for m_name, m_fraction in molecules.items()] ) 
        factor = density * self.NA * cluster_volume / mass_suma
        return { m_name: int(np.round(factor*m_fraction)) for m_name, m_fraction in molecules.items() }

    def add_molecule_template(self, name:str, atoms:object, ) -> bool:
        self._molecule_template[name] = atoms
        return True

    def add_molecule(self, container, molecule, 
                        shape:str='box', cluster_lattice_vectors:np.array=np.array([[10, 0, 0], [0,10, 0], [0, 0, 10]]), translation:np.array=None, distribution:str='random', 
                        tolerance:float=1.6, max_iteration:int=2000):

        translation = translation if translation is not None else np.array([0,0,0], dtype=np.float64)
        iteration = 0

        while True:
    
            if shape.lower() == 'box':
                if distribution.lower() == 'random':
                    displacement = translation + molecule.generate_uniform_translation_from_fractional(latticeVectors=cluster_lattice_vectors )

            atomPosition = np.dot(molecule.atomPositions, molecule.generate_random_rotation_matrix().T) + displacement

            distance_min, index_min = np.inf, -1
            for p in atomPosition:
                if container.AtomPositionManager.atomCount > 0: 
                    distance, index = container.AtomPositionManager.find_closest_neighbors(p) 

                    if distance < distance_min:
                        distance_min, index_min = distance, index

            if distance_min > tolerance:
                container.AtomPositionManager.add_atom( atomLabels=molecule.atomLabelsList, atomPosition=atomPosition, atomicConstraints=molecule.atomicConstraints )
                return True
            else:
                iteration += 1

            if iteration > max_iteration:
                print('Can not set cluster, try lower density')
                return False

    def add_solvent(self, container, 
                        shape:str='box', cluster_lattice_vectors:np.array=np.array([[10, 0, 0], [0,10, 0], [0, 0, 10]]), translation:np.array=np.array([0,0,0]), distribution:str='random', 
                        molecules:dict={'H2O':1.0}, density:float=1.0, max_iteration:int=2000):

        cluster_volume = self.get_cluster_volume(shape=shape, cluster_lattice_vectors=cluster_lattice_vectors)
        molecules_number = self.get_molecules_number_for_target_density(density=density, cluster_volume=cluster_volume, molecules=molecules)

        for molecule_name, molecule_number in molecules_number.items():
            for mn in range(molecule_number):

                if not self.add_molecule( container=container, molecule=self.molecule_template[molecule_name], translation=translation,
                                        shape=shape, cluster_lattice_vectors=cluster_lattice_vectors, distribution=distribution, max_iteration=max_iteration ):
                    print('Can not set cluster, try lower density. ')
                    break

        
    def handleCLUSTER(self, container:object, values:list, container_index:int,  file_location:str=None):
        """

        """
        sub_directories, containers = [], []
 
        for v in values:
            # Copy and update container for each set of k-point values
            container_copy = self.copy_and_update_container(container, f'/solvent/', file_location)
            
            for s in v['solvent']:
                molecule = AtomPosition()
                molecule.build(s)
                self.add_molecule_template(s, molecule)
            
            if v['slab']:
                vacuum_box, vacuum_start = container_copy.AtomPositionManager.get_vacuum_box(tolerance=v['vacuum_tolerance']) 
                shape = 'box'
                distribution = 'random'
            else:
                vacuum_box, vacuum_start = v['size'], v['translation']
                shape = v['shape']
                distribution = v['distribution']

            density = v['density']

            self.add_solvent(container=container_copy, shape=shape, cluster_lattice_vectors=vacuum_box, 
                        translation=vacuum_start, distribution=distribution, density=density, )

            if v['wrap']:
                container_copy.AtomPositionManager.pack_to_unit_cell()

            concatenate_solvent = '-'.join(v['solvent'])
            sub_directories.append(f'{density}_{concatenate_solvent}')
            containers.append(container_copy)

        # Generate execution script for each updated container
        #self.generate_execution_script_for_each_container(sub_directories, container.file_location + '/solvent')
        return containers

'''
try:
    from sage_lib.partition.partition_builder.Molecule_builder import Molecule_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Molecule_builder: {str(e)}\n")
    del sys



molecule.atomPositions[2,2] *= -1
print(molecule.atomPositions)

try:
    from sage_lib.single_run.SingleRun import SingleRun
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing SingleRun: {str(e)}\n")
    del sys
container = SingleRun()
container.AtomPositionManager = AtomPosition()
container.AtomPositionManager.read_POSCAR('/home/akaris/Documents/code/Physics/VASP/v6.2/files/dataset/CoFeNiOOH_jingzhu/surf_CoFe_4H_4OH_v2/water/CONTCAR')
vacuum_box, vacuum_start = container.AtomPositionManager.get_vacuum_box(tolerance=-2) 

print(1111, vacuum_box, vacuum_start)

a = MoleculeCluster_builder()
a.add_molecule_template('H2O', molecule)
a.add_solvent(container=container, shape='box', cluster_lattice_vectors=vacuum_box, translation=vacuum_start, distribution='random',
            density=1.0, )

#container.AtomPositionManager._latticeVectors = np.array([ [10,0,0], [0,10,0], [0,0,10], ])
container.AtomPositionManager.pack_to_unit_cell()
container.AtomPositionManager.export_as_POSCAR('POSCAR')
'''