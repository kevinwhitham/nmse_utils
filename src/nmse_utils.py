import pandas as pd
from os.path import splitext
import warnings
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.cif import CifParser
from ase.parallel import parprint

class nmse_database():

    def __init__(self, db_path):
        self.db_path = db_path
    
    def get_nmse_structure(self, structure_numbers):
        """
        Read cif files from NMSE database directory, return lists of ASE Atoms objects and names
        :param structure_numbers: list of NMSE database index numbers
        :return: tuple: list of Atoms objects, list of structure names
        """

        nmse_data = pd.read_json(self.db_path+'nmse_data_frame.json')

        # Filter structures in NMSE database
        general_filters = ['Error==False', 'is_ordered==True', 'Layers==1.0']
        compound_filters = dict(include=['Pb\d*I'],  # include only lead iodide compounds
                                exclude=['Pb\d*I\d*\D'])  # exclude any lead iodide mixed halide compounds
        dft_database = filter_structures(database=nmse_data, general_filters=general_filters,
                                         compound_filters=compound_filters)
        atoms_list = []
        structure_base_name_list = []

        for structure_number in structure_numbers:
            structure_info = dft_database.query(f'Index=={structure_number}')
            structure_file_name = structure_info.loc[structure_info.index[0], 'CIF']
            structure_base_name, _ = splitext(structure_file_name)
            structure_base_name_list.append(structure_base_name)
            parprint('Loading file: ', structure_file_name)
            # display(structure_info)

            atoms_list.append(load_atoms_from_cif(structure_file_name))

        return atoms_list, structure_base_name_list

    def load_atoms_from_cif(self, structure_file_name):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            parsed_cif = CifParser('nmse_database/structures/' + structure_file_name)
            structure = parsed_cif.get_structures(primitive=False)[0]

        # Convert pymatgen structure to ASE atoms
        return AseAtomsAdaptor.get_atoms(structure)

    def filter_structures(self, database, general_filters, compound_filters):
        """
        Filter a dataframe describing a database to select desired structures.

        :param database: pandas dataframe with database columns:
                Error, is_ordered, Layers, Compound
        :param general_filters: list of strings e.g. ['Error==False', 'is_ordered==True', Layers==1.0']
        :param compound_filters: dict with keys include and exclude. Each is a list of regex patterns
                                 e.g. include=['Pb\d*I'], exclude=['Pb\d*I\d*\D'] includes PbI4 but not PbI2Br2
        :return:
        """

        # Select structures for DFT
        filtered_database = database.query(' & '.join(general_filters))

        # filter by compound
        mask = [True] * filtered_database.shape[0]
        for e in compound_filters['include']:
            mask = mask & filtered_database['Compound'].str.contains(e)

        for e in compound_filters['exclude']:
            mask = mask & ~filtered_database['Compound'].str.contains(e)

        filtered_database = filtered_database[mask==True]

        return filtered_database

