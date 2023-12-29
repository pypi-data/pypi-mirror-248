import itertools, copy, re
import rdkit
from rdkit.Chem import rdFMCS
from rdkit import Chem
from rdkit.Chem import AllChem, Draw, rdchem, Descriptors
from typing import Optional
import selfies as se
import numpy as np
import pandas as pd
import random
np.set_printoptions(linewidth=200)


class SR_generator() :
    def __init__(
        self,
                ) :
        self.SR = {0:Chem.ChiralType.CHI_TETRAHEDRAL_CW, 1:Chem.ChiralType.CHI_TETRAHEDRAL_CCW}
        self.CT = { -1:Chem.BondStereo.STEREOANY, 0:Chem.BondStereo.STEREOCIS, 1:Chem.BondStereo.STEREOTRANS }
        self.mol = None
    
    def get_mol( self, smiles, tag_on : ["atom", "bond"] = "atom" ) :
        mol = Chem.MolFromSmiles(smiles)
        # mol = self.set_atomN( mol )
        mol = self.set_bondN(mol) if tag_on == "bond" else self.set_atomN(mol)
        self.mol = mol
        return mol
    
    def if_SR ( self, mol ) :
        chiral_atoms = Chem.FindMolChiralCenters(mol, includeUnassigned = True)
        # chiral_atoms
        lens = len(chiral_atoms)
        
        return True if lens > 0 else False
    
    def if_CT ( self, mol ) :
        any_stereo = self.CT.keys()
        cistrans_bonds = [ bond for bond in mol.GetBonds() if bond.GetStereo() in any_stereo ]
        lens = len( cistrans_bonds )
        
        return True if lens > 0 else False
        
    def set_atomN( self, mol ) :
        for atom in mol.GetAtoms():
            # For each atom, set the property "atomNote" to a index+1 of the atom
            atom.SetProp("atomNote", str(atom.GetIdx()))
        return mol
    
    def set_bondN( self, mol ) :
        for bond in mol.GetBonds():
            # For each atom, set the property "atomNote" to a index+1 of the atom
            bond.SetProp("bondNote", str(bond.GetIdx()))
        return mol

    def clean_notes( self, mol ):
        for a, b in zip( mol.GetAtoms(), mol.GetBonds() ):
            a.ClearProp( "atomNote" )
            b.ClearProp( "bondNote" )
        return mol

    def SR_combination( self, smiles,
                        iso: bool = True,
                        can: bool = False,
                        kek: bool = True,
                        tosmile = True,
                      ) :
        # from rdkit import Chem

        mol = Chem.MolFromSmiles( smiles )
        if self.if_SR( mol ) :
            # remove all stereo information
            mol_f = Chem.MolFromSmiles(Chem.MolToSmiles(mol, isomericSmiles = False))
            # Add hydrogens and perceive the chiral information
            mol_f = Chem.AddHs(mol_f)
            Chem.FindPotentialStereoBonds(mol_f)
            Chem.AssignStereochemistry(mol_f, cleanIt=True, force=True, flagPossibleStereoCenters=True)
            
            # chiral_atoms
            chiral_atoms = Chem.FindMolChiralCenters(mol_f, includeUnassigned = True)
            # all possible stereo combination
            posi_SR = list(itertools.product([0,1], repeat = len(chiral_atoms)))
            mols = []
            
            for SRc in posi_SR :
                mol_t = copy.deepcopy(mol_f)
                for (atom_index, _), SR_bool in zip( chiral_atoms, SRc ) :
                    atom = mol_t.GetAtomWithIdx(atom_index)
                    atom.SetChiralTag( self.SR[SR_bool] )
                mol_t = Chem.RemoveHs(mol_t)
                mols.append(mol_t)
                
            if tosmile :
                mols = [ Chem.MolToSmiles(m, isomericSmiles=iso, kekuleSmiles=kek, canonical=can) for m in mols ]
            return mols#, chiral_atoms
        else :
            return smiles
        
        
        return mols, chiral_atoms
    
    def CT_combination( self, smiles,
                        iso: bool = True,
                        can: bool = False,
                        kek: bool = True,
                        tosmile = True,
                      ) :
        
        mol = Chem.MolFromSmiles( smiles )
        if self.if_CT( mol ):
            # remove all stereo information
            mol_f = Chem.MolFromSmiles(Chem.MolToSmiles(mol, isomericSmiles = True, kekuleSmiles=kek))
            # all potential cis/trans bonds
            Chem.rdmolops.FindPotentialStereoBonds(mol_f)
            any_stereo = self.CT.values() # [any, cis, trans]
            cistrans_bonds = [ bond.GetIdx() for bond in mol_f.GetBonds() if bond.GetStereo() in any_stereo ]
            # all possible cis/trans combination
            posi_CT = list(itertools.product([0,1], repeat = len(cistrans_bonds)))
            mols = []
            
            for CTc in posi_CT:
                mol_t = copy.deepcopy(mol_f)
                for bond_index, CT_bool in zip( cistrans_bonds, CTc ) :
                    bond = mol_t.GetBondWithIdx( bond_index )
                    bond.SetStereo( self.CT[CT_bool] )
                
                mols.append( mol_t )
                
            if tosmile :
                mols = [ Chem.MolToSmiles(m, isomericSmiles=iso, kekuleSmiles=kek, canonical=can) for m in mols ]

            return mols # , cistrans_bonds
        else :
            return smiles
    
    def all_stereo_combination( self, smiles,
                                iso: bool = True,
                                can: bool = False,
                                kek: bool = True,
                                tosmile = True,
                              ) :
        sr_smiles = []
        mol = Chem.MolFromSmiles( smiles )
        if self.if_SR( mol ) :
            srmols = self.SR_combination( smiles, iso=iso, can=can, kek=kek, tosmile = tosmile )
            sr_smiles = sr_smiles + srmols
        else :
            sr_smiles = [Chem.MolToSmiles(mol, isomericSmiles = False, kekuleSmiles=kek)]
        
        if self.if_CT( mol ) :
            all_ct = []
            for sm in sr_smiles :
                ctmols = self.CT_combination( sm, iso=iso, can=can, kek=kek, tosmile = tosmile )
                all_ct = all_ct + ctmols
            else:
                all_smiles = all_ct
        else:
            all_smiles = sr_smiles
            
        
        return all_smiles#, chiral_atoms, ct_bonds
    
     
    def test( self, smiles = "C[C@@H]1CCN(C[C@@H]1N(C)C2=NC=NC3=C2C=CN3)C(=O)CC#N" ) :
        print( smiles )
        mol = self.get_mol(smiles)
        display(mol)
        mols, chirals = self.SR_combination( smiles )
        display(mols)
        
    def batch_generate( self, smile_list ) :
        out_dict = {}
        for smile in smile_list :
            mols, chirals = self.SR_combination( smile )
            out_dict[smile] = [ chirals, chmols ]

        return out_dict
    
    def reorder_smiles( self, smiles : str = None , mol = None, end_atom_index : int = None ):
        
        mol = Chem.MolFromSmiles(smiles) if not mol else mol
        mol = self.set_atomN(mol)
        mol = Chem.MolFromSmiles(Chem.MolToSmiles(mol, rootedAtAtom = end_atom_index, canonical=False))
        current_end_atom_indices = [atom.GetIdx() for atom in mol.GetAtoms() ]
        current_end_atom_indices.reverse()
        new_mol = Chem.RenumberAtoms( mol, tuple(current_end_atom_indices) )
        new_smiles = Chem.MolToSmiles( new_mol, canonical = False, isomericSmiles=False, kekuleSmiles=True )

        return self.simple_check_selfies(new_smiles), new_smiles
    
    def simple_check_selfies( self, smiles : str ) :
        from_smile = re.sub( r"/|\d+|\[|\]", "", smiles )
        from_selfy = re.sub( r"/|\d+|\[|\]", "", 
                             se.decoder( se.encoder( smiles ) ) 
                           )
    
        return from_smile == from_selfy

    def cut_points( self, smiles : "mol object or smile string" ):
        
        mol = self.get_mol( smiles, tag_on="atom" ) if isinstance( smiles, str ) else smiles
        mol = self.set_bondN(mol)

        ### find the in-ring information for each atom, 0 for not-in-ring atoms.
        rings_dict = { i: [0] for i in range( mol.GetNumAtoms() ) }
        for i, atoms_in_ring in enumerate(mol.GetRingInfo().AtomRings()) :
            for a in atoms_in_ring :
                if rings_dict[a] == [0] :
                    rings_dict[a] = [i+1]
                else :
                    rings_dict[a].append(i+1)
                    
        ### find all the bonds that can be used to split the compound into half when the bond is erased.
        bonds_not_rings = []
        for bond in mol.GetBonds() :
            atom_begin, atom_end = bond.GetBeginAtom(), bond.GetEndAtom()
            ab, ae = atom_begin.GetIdx(), atom_end.GetIdx()
            ab_ae_invol = set( rings_dict[ab] ).intersection( set( rings_dict[ae] ) )
            
            if len( ab_ae_invol ) == 0 or ab_ae_invol == {0} :
                bonds_not_rings.append( bond.GetIdx() )
        
        
        return rings_dict, bonds_not_rings

    def is_endable( self, mol, end_index ) :
        pass
        
    
    def split( self, smiles : "mol object or smile string", bond_idx ) :
        mol = Chem.MolFromSmiles(smiles) if isinstance( smiles, str ) else smiles
        mol = self.set_atomN(mol)
        mol_f = Chem.FragmentOnBonds(mol, (bond_idx,), addDummies=False, )
        bond = mol.GetBondWithIdx(bond_idx)
        involved = [ bond.GetBeginAtom().GetIdx(), bond.GetEndAtom().GetIdx() ]
        mols = Chem.GetMolFrags(mol_f, asMols=True)
        
        inv_atoms = { i : { "split_site": a.GetIdx(), "left_degree": a.GetDegree() } for i, m in enumerate( mols ) for a in m.GetAtoms() if int(a.GetProp("atomNote")) in involved }
        
        
        return mols, inv_atoms

    def random_split( self, 
                      smiles : "mol object or smile string",
                      size_threshold : float = 0.2,
                      debug : bool = False,
                    ) -> "smiles" :
        mol = self.get_mol(smiles, tag_on="bond") if isinstance( smiles, str ) else smiles
        mol = self.set_atomN(mol)
        mol_w = Descriptors.ExactMolWt( mol )
        display( sr.draw(mol) ) if debug else False
        rings, cuts = self.cut_points( mol )
        
        random_dict = {}
        for bond_idx in cuts:
            mol_f = Chem.FragmentOnBonds(mol, (bond_idx,), addDummies=False, )
            bond = mol.GetBondWithIdx(bond_idx)
            ab, ae = bond.GetBeginAtom(), bond.GetEndAtom()
            involved = [ ab.GetIdx(), ae.GetIdx() ]
            mols = Chem.GetMolFrags(mol_f, asMols=True)
            inv_atoms = [ {"split_site": a.GetIdx(), "left_degree": a.GetDegree(), "mW": Descriptors.ExactMolWt(m) } for m in mols for a in m.GetAtoms() if int(a.GetProp("atomNote")) in involved ]
            mols_all = list( zip( mols, inv_atoms, [ab, ae] ) )
            for i in range(0, 2) :
                if mols_all[i][1]["mW"] / mol_w >= size_threshold :
                    if (rings[ involved[i] ] != [0] and mols_all[i][1]["left_degree"] <= 2 ) or mols_all[i][1]["left_degree"] == 1 :
                        if bond_idx not in random_dict :
                            random_dict[bond_idx] = { mols_all[i][1]["mW"] : [mols_all[i][0], mols_all[i][1]["split_site"]] } 
                        else :
                            random_dict[bond_idx][mols_all[i][1]["mW"]] = [ mols_all[i][0], mols_all[i][1]["split_site"] ] 

        
        choice = random.choice( list( random_dict.keys() ) )
        print( f"cutting point (bond) : {choice}" ) if debug else False
        frags = random_dict[ choice ]
        gets = sorted(frags.items(), reverse=True)[0] if len(frags) > 1 else list(frags.items())[0]
        mol_left, end_index = gets[1]
        # sizes = [ Descriptors.ExactMolWt(m) for m in mol_frags ]
        # used_index = sizes.index( max(sizes) )
        # mol_left = mol_frags[ used_index ]
        mol_left = self.set_atomN( mol_left )
        print( "the lefted compound: " ) if debug else False
        display( sr.draw(mol_left) ) if debug else False
        selfies_check, smile_left = sr.reorder_smiles( smiles = None, mol = mol_left, end_atom_index = end_index )
        print( f"should end at : {end_index}, reordered smiles : {smile_left}" ) if debug else False
        display( sr.draw(smile_left) ) if debug else False
        return smile_left
    
    def draw( self, smiles, tag_on : ["atom", "bond"] = "atom" ) :
        mol = Chem.MolFromSmiles(smiles) if isinstance( smiles, str ) else smiles
        mol = self.set_bondN(mol) if tag_on == "bond" else self.set_atomN(mol)
        img = Chem.Draw.MolToImage( mol, fitImage=True, size=(500,500))
        return img
    
    def kinase_type_similarity( self, name, in_smile ):
    
        mol = Chem.MolFromSmiles(in_smile)

        ref = pd.read_csv("/home/molalin/workspace/PKI/pkidb_230309.csv")
        ref = ref[~ref.Type.isna()]
        types = ref.Type.unique()
        types_datas = { t: ref[ref.Type == t][["ID", "Canonical_Smiles"]].values for t in types }
        cols = [ types_datas[t][...,0].tolist() for t in types ]
        cols = ["ID", "Smiles", "max"] + types.tolist() + sum(cols, []) # flatten the list
        types_MCSratio = {}
        types_MCSraw = {}
        types_MCSraw["ID"] = [name]
        types_MCSraw["Smiles"] = [in_smile]


        for type_, datas in types_datas.items() :
            names = datas[...,0]
            mols = [ Chem.MolFromSmiles(smile) for smile in datas[...,1] ]
            ratios = [ rdFMCS.FindMCS([mol, mol_t]).numAtoms / rdFMCS.FindMCS([mol, mol]).numAtoms for mol_t in mols ]
            for i, ratio in enumerate(ratios) :
                types_MCSraw[names[i]] = [ratio] 
            ratio = round( max(ratios), 4 )
            types_MCSraw[type_] = [ratio]
            types_MCSratio[type_] = [ratio]

        max_type = max(types_MCSratio, key=types_MCSratio.get)
        types_MCSraw["max"] = max_type
        df = pd.DataFrame.from_dict(types_MCSraw)

        return types_MCSratio, df

    def generate( self, 
                  file_path, 
                  name_col : Optional[str], 
                  smiles_col : Optional[str],
                  out_file : "/mnt/Medical/..."
                ) :

        infile = pd.read_csv( file_path )
        df_list = []
        for name, smile in infile[[name_col, smiles_col]].drop_duplicates().values :
            _, df_single = kinase_type_similarity( name, smile )
            df_list.append(df_single)

        df_all = pd.concat(df_list).reset_index(drop = True)
        df_all.to_csv(out_file, index=False)
        
    def compute3Dcoord( self, smiles ) :
        mol = Chem.MolFromSmiles( smiles )
        mol = Chem.AddHs( mol )
        AllChem.EmbedMolecule( mol )
        mol = Chem.RemoveHs( mol )
        # display( mol )
        # print( Chem.MolToMolBlock( mol ) )
        return mol
    
