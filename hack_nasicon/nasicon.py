import pandas as pd
from discomat.cuds.cuds import Cuds
from rdflib import Graph, Namespace, Literal
from discomat.ontology.namespaces import CUDS
from Chemical_formula_Parser import ChemicalFormulaParser
from mnemonic import Mnemonic
from discomat.visualisation.cuds_vis import gvis

CE = Namespace('http://materials-discovery.org/chemical-elements#')
MIO = Namespace('http://www.ddmd.io/mio/')

# Reading the csv file
csv_file = 'nasicon.csv'  # Change it if you want to run
data = pd.read_csv(csv_file)
print(data.head())


gall = Graph()
cuds_objects = set()

# Iterate through each row to extract material and relevant properties
for index,row in data.iterrows():
    material = row['Materials']
    name_value = row['name']
    doi_value = row['doi_reference']
    work = row['worktype']
    exp_method = row['experiment_method']
    sin_temperature = row['sintering_temperature']
    sin_time = row['sintering_time']
    sim_method = row['simulation_method']
    sim_software = row['simulation_software']
    force_field = row['force_field']
    time_step = row['time_step']
    sim_temperature = row['simulation_temperature']
    approx_method = row['approximation_method']
    cutoff_energy = row['cutoff_energy']
    kpoints = row['Kpoints']
    total_atoms = row['total_atoms']
    lattice_a_value = row['Lattice_a']
    lattice_b_value = row['Lattice_b']
    lattice_c_value = row['Lattice_c']
    lattice_volume_value = row['Lattice_Volume']
    sec_phase = row['secondary_phase']
    sec_phase_weight =row['secondary_phase_weight']
    grain_size = row['grain_size']
    rela_density = row['relative_density']
    total_energy = row['Total_energy']
    band_gap_energy = row['band_gap_energy']
    activation_energy = row['activation_energy']
    li_conductivity = row['Li_ion_conductivity']


    # Creating CUDs for the material
    if pd.notna(material):
        m = Cuds(ontology_type=MIO.Material, description=f'{material}')
        gall += m.graph
        cuds_objects.add(m)


    # Create CUDS for name, doi, and add them to material's Cuds
    if pd.notna(name_value):
        mn = Cuds(ontology_type=MIO.Material_Name, description=f'material name: {name_value}')
        mn.add(MIO.name,Literal(name_value))
        m.add(CUDS.has, mn)
        gall +=  m.graph + mn.graph
        cuds_objects.add(mn)

    if pd.notna(doi_value):
        doi = Cuds(ontology_type=MIO.DoiReference,description=f'The cuds about doi reference of {material}')
        doi.add(MIO.Doi, Literal(doi_value))
        m.add(CUDS.has, doi)
        gall +=  m.graph + doi.graph
        cuds_objects.add(doi)

    # Creating Cuds for chemical composition and formula
    cc = Cuds(ontology_type=MIO.ChemicalComposition,description=f'The cuds of chemical composition of {material}')
    f = Cuds(ontology_type=MIO.ChemicalFormula,description=f'The cuds of chemical formula of {material}')
    cc.add(CUDS.has, f)
    print(f"Added chemical formula to chemical composition.")
    m.add(CUDS.has, cc)
    print(f"Added chemical composition to material.")
    gall += m.graph + cc.graph + f.graph

    cuds_objects.add(cc)
    cuds_objects.add(f)

    # Parsing Chemical Formulas to 3 lists using chemical parser (in another py file)
    parser = ChemicalFormulaParser(material)
    fu_list = parser.fu_list
    e_list = parser.elements
    s_list = parser.stoichiometry

    print(f"Formula Units: {fu_list}")
    print(f"Elements List: {e_list}")
    print(f"Stoichiometry List: {s_list}")

    # Iterate over the formula units, elements, and stoichiometry lists
    for i, fu_item in enumerate(fu_list):
        # create a new formula unit for each iteration
        fu = Cuds(ontology_type=MIO.ChemicalFormulaUnit,description=f'The cuds of formula unit {fu_item}')
        fu.add(MIO.value, Literal(fu_item))
        # Add the formula unit to the larger structure (f)
        f.add(CUDS.has, fu)
        cuds_objects.add(fu)
        gall += f.graph + fu.graph


        element_symbol = e_list[i]
        stoichiometry_value = s_list[i]

        # Dynamically create a CUDS instance for the element and store it in the dictionary
        es = Cuds(ontology_type=CE[element_symbol],description=f'The cuds of the {element_symbol} element')  # Dynamically get the ontology type for the element
        fu.add(CUDS.has, es)  # Add the element CUDS instance to the formula unit
        cuds_objects.add(es)

        # Create and add the stoichiometry value to the element
        st = Cuds(ontology_type=MIO.Stoichiometry,description=f'The cuds of the stoichiometry for {element_symbol}')
        st.add(MIO.Value, Literal(stoichiometry_value))
        fu.add(CUDS.has, st)
        cuds_objects.add(st)

        gall +=  fu.graph + st.graph + es.graph

    # Define the work of each material
    w = Cuds(ontology_type=MIO.Work,description=f'the cuds of work for {material}')
    m.add(CUDS.has,w)
    cuds_objects.add(w)

    gall +=  m.graph + w.graph



    if work == 'simulation':
        sm = Cuds(ontology_type=MIO.Simulation,description=f'simulation for {material}')
        w.add(CUDS.has, sm)
        cuds_objects.add(sm)


        smm = Cuds(ontology_type=MIO.Simulation_method,description=f'{sim_method} simulation for {material}')
        smm.add(MIO.Value, Literal(sim_method))
        sm.add(CUDS.has, smm)
        cuds_objects.add(smm)


        sms = Cuds(ontology_type=MIO.Simulation_Software,description=f'{sim_software} for {material} simulation')
        sms.add(MIO.Value, Literal(sim_software))
        sm.add(CUDS.has, sms)
        cuds_objects.add(sms)

        sims = Cuds(ontology_type=MIO.Simulation_Setting,description=f'simulation setting for {material}')
        sm.add(CUDS.has, sims)
        cuds_objects.add(sims)


        smr = Cuds(ontology_type=MIO.simulation_result,description=f'{sim_method} simulation result for {material}')
        sm.add(CUDS.has, smr)
        cuds_objects.add(smr)

        gall += w.graph + sm.graph + smm.graph + sms.graph +sims.graph + smr.graph


        if pd.notna(approx_method):
            am = Cuds(ontology_type=MIO.Approximation_Method,description=f'approximation method of simulation for {material}')
            am.add(MIO.Value, Literal(approx_method))
            sims.add(CUDS.has, am)
            cuds_objects.add(am)
            gall += sims.graph + am.graph

        if pd.notna(cutoff_energy):
            ce = Cuds(ontology_type=MIO.cutoff_energy, description=f'cutoff energy of simulation for {material}')
            ce.add(MIO.Value, Literal(cutoff_energy))
            ce.add(MIO.Unit, Literal('eV'))
            sims.add(CUDS.has, ce)
            cuds_objects.add(ce)
            gall += sims.graph + ce.graph

        if pd.notna(kpoints):
            kp = Cuds(ontology_type=MIO.Kpoints, description=f'kpoints of dft simulation for {material}')
            kp.add(MIO.Value, Literal(kpoints))
            sims.add(CUDS.has, kp)
            cuds_objects.add(kp)
            gall += sims.graph + kp.graph

        if pd.notna(total_atoms):
            ta = Cuds(ontology_type=MIO.Total_atoms, description=f'total atoms of simulation for {material}')
            ta.add(MIO.Value, Literal(total_atoms))
            sims.add(CUDS.has, ta)
            cuds_objects.add(ta)
            gall += sims.graph + ta.graph


        if pd.notna(force_field):
            ff = Cuds(ontology_type=MIO.ForceField, description=f'force field of simulation for {material}')
            ff.add(MIO.Value, Literal(force_field))
            sims.add(CUDS.has, ff)
            cuds_objects.add(ff)
            gall += sims.graph + ff.graph

        if pd.notna(time_step):
            ts = Cuds(ontology_type=MIO.Timestep, description=f'time step of simulation for {material}')
            ts.add(MIO.Value, Literal(time_step))
            ts.add(MIO.Unit, Literal('fs'))
            sims.add(CUDS.has, ts)
            cuds_objects.add(ts)
            gall += sims.graph + ts.graph

        if pd.notna(sim_temperature):
            simt = Cuds(ontology_type=MIO.Simulation_temperature, description=f'simulation temperature for {material}')
            simt.add(MIO.Value, Literal(sim_temperature))
            simt.add(MIO.Unit, Literal('K'))
            sims.add(CUDS.has, simt)
            cuds_objects.add(simt)
            gall += sims.graph + simt.graph


        # simulation result
        if pd.notna(total_energy):
            te = Cuds(ontology_type=MIO.total_energy, description=f'total energy for {material}')
            te.add(MIO.Value, Literal(total_energy))
            te.add(MIO.Unit, Literal('eV'))
            smr.add(CUDS.has, te)
            cuds_objects.add(te)
            gall += smr.graph + te.graph

        if pd.notna(band_gap_energy):
            bge = Cuds(ontology_type=MIO.band_gap_energy, description=f'band gap energy for {material} in the simulation')
            bge.add(MIO.Value, Literal(band_gap_energy))
            bge.add(MIO.Unit, Literal('eV'))
            smr.add(CUDS.has, bge)
            cuds_objects.add(bge)
            gall += smr.graph + bge.graph

        if pd.notna(activation_energy):
            ae = Cuds(ontology_type=MIO.activation_energy, description=f'activation energy for {material} in the simulation')
            ae.add(MIO.Value, Literal(activation_energy))
            ae.add(MIO.Unit, Literal('eV'))
            smr.add(CUDS.has, ae)
            cuds_objects.add(ae)
            gall += smr.graph + ae.graph

        if pd.notna(li_conductivity):
            lic = Cuds(ontology_type=MIO.Li_ion_conductivity, description=f'Li ion conductivity for {material} in the simulation')
            lic.add(MIO.Value, Literal(li_conductivity))
            lic.add(MIO.Unit, Literal('S/cm'))
            smr.add(CUDS.has, lic)
            cuds_objects.add(lic)
            gall += smr.graph + lic.graph

        # Add lattice parameters
        if lattice_a_value or lattice_b_value or lattice_c_value or lattice_volume_value:
            Lp = Cuds(ontology_type=MIO.Lattice_parameter, description=f'lattice parameter for {material} in the simulation')
            smr.add(CUDS.has, Lp)
            cuds_objects.add(Lp)
            gall += smr.graph + Lp.graph

            lattice_cuds_dict = {}
            lattice_parameters = [
                (MIO.Lattice_a, lattice_a_value, "angstrom", 'Lattice a', 'La'),
                (MIO.Lattice_b, lattice_b_value, "angstrom", 'Lattice_b', 'Lb'),
                (MIO.Lattice_c, lattice_c_value, "angstrom", 'Lattice_c', 'Lc'),
                (MIO.Lattice_volume, lattice_volume_value, "angstrom^3", 'Lattice Volume', 'Lv'),
            ]

            for lattice_type, value, unit, lattice_name, var_name in lattice_parameters:
                if pd.notna(value):
                    # Add a specific description for each lattice parameter CUDS
                    lattice_cuds_dict[var_name] = Cuds(ontology_type=lattice_type,description=f'{lattice_name} in the simulation for {material}')
                    lattice_cuds_dict[var_name].add(MIO.Value, Literal(value))
                    lattice_cuds_dict[var_name].add(MIO.Unit, Literal(unit))
                    Lp.add(CUDS.has, lattice_cuds_dict[var_name])
                    cuds_objects.add(lattice_cuds_dict[var_name])
                    gall += Lp.graph + lattice_cuds_dict[var_name].graph

    elif work == 'experiment':
        exp = Cuds(ontology_type=MIO.Experiment, description=f'Experiments of {material}')
        w.add(CUDS.has, exp)
        cuds_objects.add(exp)


        expm = Cuds(ontology_type=MIO.Experiment_method, description=f'Experiments method of {material}')
        expm.add(MIO.Value, Literal(exp_method))
        exp.add(CUDS.has, expm)
        cuds_objects.add(expm)


        expc= Cuds(ontology_type=MIO.Experiment_condition, description=f'Experiments condition of {material}')
        exp.add(CUDS.has, expc)
        cuds_objects.add(expc)

        expr =Cuds(ontology_type=MIO.Experiment_result, description=f'Experiments result of {material}')
        exp.add(CUDS.has, expr)
        cuds_objects.add(expr)

        gall += w.graph + exp.graph+ expm.graph + expr.graph +expc.graph

        if pd.notna(sin_time):
            sint = Cuds(ontology_type=MIO.Sin_time, description=f'Sintering time of {material}')
            sint.add(MIO.Value, Literal(sin_time))
            sint.add(MIO.Unit, Literal('h'))
            expc.add(CUDS.has, sint)
            cuds_objects.add(sint)

        if pd.notna(sin_temperature):
            sinT = Cuds(ontology_type=MIO.Sin_temperature, description=f'Sintering temperature of {material}')
            sinT.add(MIO.Value, Literal(sin_temperature))
            sinT.add(MIO.Unit, Literal('K'))
            expc.add(CUDS.has, sinT)
            cuds_objects.add(sinT)

        gall += expc.graph + sint.graph +sinT.graph


        # add experiment result
        if sec_phase is not None:
            sp = Cuds(ontology_type=MIO.Sec_phase, description=f'Second phase of {material}')
            sp.add(MIO.Value, Literal(sec_phase))
            expr.add(CUDS.has, sp)
            cuds_objects.add(sp)

        if sec_phase_weight is not None:
            spw = Cuds(ontology_type=MIO.Sec_phase_weight, description=f'Second phase weight of {material}')
            spw.add(MIO.Value, Literal(sec_phase_weight))
            spw.add(MIO.Unit, Literal('%'))
            expr.add(CUDS.has, spw)
            cuds_objects.add(spw)

        if grain_size is not None:
            gs = Cuds(ontology_type=MIO.Grain_size, description=f'Grainsize of {material}')
            gs.add(MIO.Value, Literal(grain_size))
            gs.add(MIO.Unit, Literal('µm'))
            expr.add(CUDS.has, gs)
            cuds_objects.add(gs)

        if rela_density is not None:
            rd = Cuds(ontology_type=MIO.RelaDensity, description=f'Relative density of {material}')
            rd.add(MIO.Value, Literal(rela_density))
            rd.add(MIO.Unit, Literal('%'))
            expr.add(CUDS.has, rd)
            cuds_objects.add(rd)

        if activation_energy is not None:
            ae =Cuds(ontology_type=MIO.Activation_energy, description=f'Activation energy of {material} in the experiment')
            ae.add(MIO.Value, Literal(activation_energy))
            ae.add(MIO.Unit, Literal('eV'))
            expr.add(CUDS.has, ae)
            cuds_objects.add(ae)

        if li_conductivity is not None:
            lic = Cuds(ontology_type=MIO.Li_ion_conductivity, description=f'Conductivity of {material} in the experiment')
            lic.add(MIO.Value, Literal(li_conductivity))
            lic.add(MIO.Unit, Literal('S/cm'))
            expr.add(CUDS.has, lic)
            cuds_objects.add(lic)

        gall += expr.graph + ae.graph + lic.graph +sp.graph + spw.graph + gs.graph + rd.graph

        # Add lattice parameters
        if lattice_a_value or lattice_b_value or lattice_c_value or lattice_volume_value:
            Lp = Cuds(ontology_type=MIO.Lattice_parameter, description='The cuds of lattice parameter')
            expr.add(CUDS.has, Lp)
            cuds_objects.add(Lp)
            gall += expr.graph + Lp.graph

            lattice_cuds_dict = {}
            lattice_parameters = [
                (MIO.Lattice_a, lattice_a_value, "angstrom", 'Lattice a', 'La'),
                (MIO.Lattice_b, lattice_b_value, "angstrom", 'Lattice_b', 'Lb'),
                (MIO.Lattice_c, lattice_c_value, "angstrom", 'Lattice_c', 'Lc'),
                (MIO.Lattice_volume, lattice_volume_value, "angstrom^3", 'Lattice Volume', 'Lv'),
            ]

            for lattice_type, value, unit, lattice_name, var_name in lattice_parameters:
                if pd.notna(value):
                    # Add a specific description for each lattice parameter CUDS
                    lattice_cuds_dict[var_name] = Cuds(ontology_type=lattice_type,description=f'{lattice_name} in the simulation for {material}')
                    lattice_cuds_dict[var_name].add(MIO.Value, Literal(value))
                    lattice_cuds_dict[var_name].add(MIO.Unit, Literal(unit))
                    Lp.add(CUDS.has, lattice_cuds_dict[var_name])
                    cuds_objects.add(lattice_cuds_dict[var_name])
                    gall += Lp.graph + lattice_cuds_dict[var_name].graph

# print the number of cuds
print(f"Total number of unique CUDS objects in the graph: {len(cuds_objects)}")


gvis(gall,'nasicon.html')

gall.serialize('nasicon.ttl',format='ttl')


