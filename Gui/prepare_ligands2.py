import os
from Gui.ligandsPreparation2 import prepareLigands, selectLigands, sdf2pdb
from Utilities.utils import checkFilesInFolder, removeFiles
from config import Config
from pathlib import Path
from tkinter import messagebox


def prepare_ligands(
    verbose, 
    input_file, 
    default_file, 
    excel_folder, 
    sdf_folder,  
    pdb_folder, 
    pdbqt_folder,
    keep_ligands
):
        
    print("------------------------------------------")
    print("######### INITIALIZE ENVIRONMENT #########")
    print("------------------------------------------")

    print(input_file)

    if input_file != default_file:
        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Specify a valid input file!")
            exit(1)
        if not os.access(input_file, os.R_OK):
            messagebox.showerror("Error", "Modify file permission!")
            exit(1)
        print("set input filepath to ", input_file)

    if excel_folder != Config.EXCEL_FOLDER:
        if not os.path.exists(excel_folder):
            messagebox.showerror("Error", "Specify a valid directory or modify dir permission for excel folder!")
            exit(1)
        print("set excel folder to ", excel_folder)

    if sdf_folder != Config.LIGANDS_SDF_FOLDER:
        if not os.path.exists(sdf_folder):
            messagebox.showerror("Error", "Specify a valid directory or modify dir permission for sdf folder!")
            exit(1)
        print("set sdf folder to ", sdf_folder)

    if pdb_folder != Config.LIGANDS_PDB_FOLDER:
        if not os.path.exists(pdb_folder):
            messagebox.showerror("Error", "Specify a valid directory or modify dir permission for pdb folder!")
            exit(1)
        print("set pdb folder to ", pdb_folder)

    if pdbqt_folder != Config.LIGANDS_PDBQT_FOLDER:
        if not os.path.exists(pdbqt_folder):
            messagebox.showerror("Error", "Specify a valid directory or modify dir permission for pdbqt folder!")
            exit(1)
        print("set pdbqt folder to ", pdbqt_folder)

    print("set keep-ligands option to ", keep_ligands)

    # initialize folders
    if sdf_folder == Config.LIGANDS_SDF_FOLDER:
        Path(Config.LIGANDS_SDF_FOLDER).mkdir(parents=True, exist_ok=True)
    if pdb_folder == Config.LIGANDS_PDB_FOLDER:
        Path(Config.LIGANDS_PDB_FOLDER).mkdir(parents=True, exist_ok=True)
    if pdbqt_folder == Config.LIGANDS_PDBQT_FOLDER:
        Path(Config.LIGANDS_PDBQT_FOLDER).mkdir(parents=True, exist_ok=True)
    if excel_folder == Config.EXCEL_FOLDER:
        Path(Config.EXCEL_FOLDER).mkdir(parents=True, exist_ok=True)
    
    with open(input_file) as f:
        contents = f.readlines()
        number_contents = len(contents)

    if not keep_ligands:
        removeFiles(sdf_folder, ".sdf")
        if verbose:
            print("---------------- LIGANDS -----------------")
            print("################# STEP 1 #################")
            print("------------------------------------------")

        selectLigands(
            sdf_folder=sdf_folder,
            excel_folder=excel_folder,
            verbose=verbose,
            contents=contents,
            number_contents=number_contents
        )

    else: 
        # check if there is at least a sdf file
        if not checkFilesInFolder(folder=sdf_folder, docted_extension=".sdf"):
            messagebox.showerror("Error", "There's no sdf file into sdf folder")
            exit(2)
        if verbose:
            print("\n--------------- LIGANDS ------------------")
            print("############# SKIPPED STEP 1.1 #############")
            print("--------------------------------------------")
    
    if verbose:
        print("---------------- LIGANDS -----------------")
        print("################# STEP 2 #################")
        print("------------------------------------------")
            

    sdf2pdb(
        sdf_folder=sdf_folder, 
        pdb_folder=pdb_folder, 
        verbose=verbose,
        number_contents=number_contents
    )
    
    if verbose:
        print("---------------- LIGANDS -----------------")
        print("################# STEP 3 #################")
        print("------------------------------------------")
    
    prepareLigands(
        pdb_folder=pdb_folder,
        pdbqt_folder=pdbqt_folder,
        verbose=verbose,
        number_contents=number_contents
    )

    if verbose:
        print("----------- LIGANDS: COMPLETED -----------")