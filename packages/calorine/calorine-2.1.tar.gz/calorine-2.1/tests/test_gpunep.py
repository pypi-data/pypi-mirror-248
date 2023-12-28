import os
from typing import List, Tuple

import numpy as np
import pytest
from ase import Atoms
from ase.build import bulk
from calorine.calculators import GPUNEP


nep2_fname = 'tests/nep_models/PbTe_NEP2_dummy.txt'
nep3_fname = 'tests/nep_models/nep3_v3.3.1_PbTe_Fan22.txt'


@pytest.fixture
def single_point_parameters() -> List[Tuple]:
    """MD parameters to calculate single point potential energy."""
    return [('dump_thermo', 1),
            ('dump_force', 1),
            ('dump_position', 1),
            ('velocity', 1e-24),
            ('time_step', 1e-6),
            ('ensemble', 'nve'),
            ('run', 1)]


@pytest.fixture
def custom_parameters() -> List[Tuple]:
    """Custom MD parameters."""
    return [('dump_thermo', 10),
            ('dump_position', 10),
            ('dump_force', 10),
            ('time_step', 1),
            ('ensemble', ['nvt_ber', 300, 300, 100]),
            ('run', 30)]


@pytest.fixture
def calculator(request, tmpdir) -> GPUNEP:
    """
    Calculator with either a specified directory (tmpdir) or
    automatically created with GPUMD.
    """
    nep_version, specified_dir = request.param
    if nep_version == 3:
        fname = nep3_fname
    elif nep_version == 2:
        fname = nep2_fname
    else:
        raise NotImplementedError('Only NEP2 and NEP3 are currently tested.')
    if specified_dir:
        return GPUNEP(fname,
                      directory=tmpdir)
    else:
        return GPUNEP(fname)


@pytest.fixture
def PbTe() -> Atoms:
    """ASE Atoms object compatible with calculator."""
    structure = bulk('PbTe', crystalstructure='rocksalt', a=4)
    structure[0].position += np.array([0.03, 0.02, 0])
    return structure


def runfile_matches_parameters(fname, parameters, model_filename):
    """Checks whether content of runfile matches parameters list."""
    with open(fname, 'r') as f:
        for line in f:
            row = line.split()
            found_match = False
            for param in parameters:
                if row[0] == 'potential':
                    if model_filename not in line:
                        return False
                    found_match = True
                elif row[0] == param[0]:
                    # Convert parameters to iterable
                    if isinstance(param[1], str):
                        param_iter = [param[1]]
                    else:
                        try:
                            iter(param[1])
                            param_iter = param[1]
                        except TypeError:
                            param_iter = [param[1]]

                    # Compare all parameters
                    if len(row[1:]) == len(param_iter):
                        for i, j in zip(row[1:], param_iter):
                            try:
                                i = float(i)
                                if abs(i - j) > 1e-6:
                                    break
                            except ValueError:
                                if i != j:
                                    break
                        else:
                            found_match = True
                            break

            if not found_match:
                return False
    return True


@pytest.mark.parametrize('fname, species',
                         [(nep3_fname, ('Te', 'Pb')),
                          (nep2_fname, ('Te', 'Pb'))])
def test_init(fname, species):
    """Test initialization of calculator."""
    calc = GPUNEP(fname)
    assert isinstance(calc, GPUNEP)
    assert calc.command == 'gpumd > /dev/null'
    assert calc.model_filename == fname
    assert calc._use_temporary_directory
    assert tuple(calc.species) == species


@pytest.mark.parametrize('fname, directory, label, command',
                         [(nep3_fname, 'tmp',
                           'custom_label', 'custom_command'),
                          (nep2_fname, 'tmp',
                           'custom_label', 'custom_command'),
                          (nep3_fname, 'tmp',
                           'custom_label', 'custom_command > out')])
def test_init_with_custom_settings(fname, directory, label, command):
    """Test initialization with custom settings."""
    calc = GPUNEP(fname,
                  directory=directory,
                  label=label,
                  command=command,
                  )
    if '>' in command:
        assert calc.command == command
    else:
        assert calc.command == command + ' > stdout'
    assert calc.model_filename == fname
    assert not calc._use_temporary_directory


def test_init_with_nonexistent_model():
    """Test initialization when model file does not exist."""
    with pytest.raises(FileNotFoundError) as e:
        GPUNEP('no-such-model.txt')
    assert 'does not exist' in str(e)


@pytest.mark.parametrize('calculator',
                         [(3, True),
                          (2, True),
                          (3, False)], indirect=['calculator'],
                         )
def test_run_custom_md(PbTe, calculator, custom_parameters):
    """Tests run custom MD function in temporary directory."""
    PbTe.calc = calculator
    atoms = calculator.run_custom_md(custom_parameters, return_last_atoms=True)
    assert isinstance(atoms, Atoms)
    assert not np.allclose(atoms.get_positions(), PbTe.get_positions())

    if not calculator._use_temporary_directory:
        # Check that run file was properly written
        assert runfile_matches_parameters(os.path.join(calculator.directory, 'run.in'),
                                          custom_parameters,
                                          calculator.model_filename)
    else:
        assert not os.path.exists(calculator.directory)


@pytest.mark.parametrize('calculator',
                         [(3, True)], indirect=['calculator'],
                         )
def test_run_custom_md_only_prepare(PbTe, calculator, custom_parameters):
    """Tests run custom MD function in temporary directory."""
    PbTe.calc = calculator
    retval = calculator.run_custom_md(custom_parameters, only_prepare=True)
    assert retval is None

    # Check that run file was properly written
    assert runfile_matches_parameters(os.path.join(calculator.directory, 'run.in'),
                                      custom_parameters,
                                      calculator.model_filename)


@pytest.mark.parametrize('calculator',
                         [(3, False)], indirect=['calculator'],
                         )
def test_run_custom_md_only_prepare_in_temporary_dir(PbTe, calculator, custom_parameters):
    PbTe.calc = calculator
    with pytest.raises(ValueError) as e:
        calculator.run_custom_md(custom_parameters, return_last_atoms=True, only_prepare=True)
    assert 'Refusing to only prepare' in str(e)


@pytest.mark.parametrize('calculator',
                         [(3, False)], indirect=['calculator'],
                         )
def test_run_custom_md_with_discarded_result(PbTe, calculator, custom_parameters):
    """
    Tests that running without returning last atoms
    is prevented (because all results would be gone).
    """
    PbTe.calc = calculator
    with pytest.raises(ValueError) as e:
        calculator.run_custom_md(custom_parameters, return_last_atoms=False)
    assert 'Refusing to run in temporary directory' in str(e)


@pytest.mark.parametrize('calculator',
                         [(3, False)], indirect=['calculator'],
                         )
def test_run_custom_md_with_bad_input(PbTe, calculator, custom_parameters):
    """
    Tests that running without returning last atoms
    is prevented (because all results would be gone).
    """
    PbTe.calc = calculator
    custom_parameters[0] = ('bad', 'input')
    with pytest.raises(RuntimeError) as e:
        calculator.run_custom_md(custom_parameters, return_last_atoms=True)
    assert 'Calculator "gpunep" failed with command' in str(e)


@pytest.mark.parametrize('calculator',
                         [(3, True),
                          (3, False)], indirect=['calculator'],
                         )
def test_write_input_tmpdir(PbTe, calculator, single_point_parameters):
    """Tests that function controlling writing of input files works."""
    calculator.write_input(PbTe)
    dirs = os.listdir(calculator.directory)
    assert 'model.xyz' in dirs
    assert 'run.in' in dirs

    # Check that content of run.in is proper single point calculation parameters
    assert runfile_matches_parameters(os.path.join(calculator.directory, 'run.in'),
                                      single_point_parameters,
                                      calculator.model_filename)


@pytest.mark.parametrize('calculator',
                         [(3, True),
                          (3, False),
                          (2, False)], indirect=['calculator'],
                         )
def test_write_runfile(calculator, custom_parameters):
    """Tests that single point parameters input file is properly written."""
    calculator._write_runfile(custom_parameters)
    assert runfile_matches_parameters(os.path.join(calculator.directory, 'run.in'),
                                      custom_parameters,
                                      calculator.model_filename)


@pytest.mark.parametrize('calculator',
                         [(3, True)], indirect=['calculator'],
                         )
def test_write_runfile_with_specified_potential(calculator, custom_parameters):
    """Tests that single point parameters input file is properly written."""
    custom_parameters = [('potential', 'nep.txt')] + custom_parameters
    calculator._write_runfile(custom_parameters)
    assert runfile_matches_parameters(os.path.join(calculator.directory, 'run.in'),
                                      custom_parameters,
                                      'nep.txt')


@pytest.mark.parametrize('calculator, target_energy, target_stress',
                         [((3, True), -4.8747868538,
                           [-1.75264518e-01, -1.74415774e-01, -1.73915106e-01,
                            -8.22096822e-08, -6.34192454e-08, -5.78386724e-03])],
                         indirect=['calculator'],
                         )
def test_get_potential_energy_and_stresses_from_file(PbTe, custom_parameters, calculator,
                                                     target_energy, target_stress):
    """Tests reading of potential energy and stresses."""
    PbTe.calc = calculator
    calculator.run_custom_md(custom_parameters, return_last_atoms=False)
    energy, stress = calculator.get_potential_energy_and_stresses_from_file()
    assert abs(energy - target_energy) < 1e-5
    assert np.allclose(stress, target_stress)


@pytest.mark.parametrize('calculator',
                         [(3, True)],
                         indirect=['calculator'],
                         )
def test_fail_to_get_potential_energy_and_stresses_from_file(PbTe, calculator, tmpdir):
    """Tests failure when reading potential energy and stresses."""
    PbTe.calc = calculator
    p = tmpdir.join('thermo.out')
    p.write('NaN NaN NaN NaN NaN NaN\n')
    with pytest.raises(ValueError) as e:
        calculator.get_potential_energy_and_stresses_from_file()
    assert 'Failed to extract energy and/or stresses:' in str(e)


@pytest.mark.parametrize('calculator, target_forces',
                         [((3, True), [[3.97592e-01, 2.74049e-01, 6.09441e-06],
                                       [-3.97592e-01, -2.74049e-01, -6.09441e-06]])],
                         indirect=['calculator'],
                         )
def test_get_forces_from_file(PbTe, custom_parameters, calculator, target_forces):
    """Tests reading of potential energy and stresses."""
    PbTe.calc = calculator
    calculator.run_custom_md(custom_parameters, return_last_atoms=False)
    forces = calculator.get_forces_from_file()
    assert np.allclose(forces, target_forces, atol=1e-6)


@pytest.mark.parametrize('calculator, expected_energy',
                         [((3, True), -4.8564407825),
                          ((3, False), -4.8564407825),
                          ((2, False), 58.0)],
                         indirect=['calculator'],
                         )
def test_get_potential_energy(PbTe, calculator, expected_energy):
    """Tests standard way of calculating potential energy."""
    PbTe.calc = calculator
    e = PbTe.get_potential_energy()
    assert abs(e - expected_energy) < 1e-5


@pytest.mark.parametrize('calculator, expected_forces',
                         [((3, True), [[1.61652e-01, 1.08260e-01, 1.67526e-06],
                                       [-1.61652e-01, -1.08260e-01, -1.67526e-06]]),
                          ((3, False), [[1.61652e-01, 1.08260e-01, 1.67526e-06],
                                        [-1.61652e-01, -1.08260e-01, -1.67526e-06]]),
                          ((2, False), [[0, 0, 0], [0, 0, 0]])],
                         indirect=['calculator'],
                         )
def test_get_forces(PbTe, calculator, expected_forces):
    """Tests standard way of calculating forces."""
    PbTe.calc = calculator
    forces = PbTe.get_forces()
    assert np.allclose(forces, expected_forces, atol=1e-6)


@pytest.mark.parametrize('calculator, expected_stress',
                         [((3, True), [-0.15837644, -0.15825044, -0.15815363,
                                       -1.95632527e-08, 5.19175762e-08, -9.06732487e-04]),
                          ((3, False), [-0.15837644, -0.15825044, -0.15815363,
                                        -1.95632527e-08, 5.19175762e-08, -9.06732487e-04]),
                          ((2, False), [0, 0, 0, 0, 0, 0])],
                         indirect=['calculator'],
                         )
def test_get_stress(PbTe, calculator, expected_stress):
    """Tests standard way of calculating forces."""
    PbTe.calc = calculator
    stress = PbTe.get_stress()
    assert np.allclose(stress, expected_stress, atol=1e-6)


@pytest.mark.parametrize('calculator',
                         [(3, True)], indirect=['calculator'],
                         )
def test_read_results(PbTe, calculator, custom_parameters):
    """Tests read_results function."""
    PbTe.calc = calculator
    calculator.run_custom_md(custom_parameters, return_last_atoms=False)
    assert len(calculator.results) == 0
    calculator.read_results()
    assert 'energy' in calculator.results
    assert 'forces' in calculator.results
    assert 'stress' in calculator.results


@pytest.mark.parametrize('calculator',
                         [(3, True)], indirect=['calculator'],
                         )
def test_clean(PbTe, calculator, custom_parameters):
    """Tests that directories are properly deleted."""
    PbTe.calc = calculator
    calculator.run_custom_md(custom_parameters, return_last_atoms=True)
    assert os.path.exists(calculator.directory)
    calculator._clean()
    assert not os.path.exists(calculator.directory)


@pytest.mark.parametrize('calculator',
                         [(3, False)], indirect=['calculator'],
                         )
def test_make_new_tmp_directory(PbTe, calculator):
    """Tests creation of new tmp directory"""
    PbTe.calc = calculator
    assert os.path.exists(os.path.join(os.path.abspath(calculator.directory),
                                       calculator._potential_path))
    assert os.path.exists(calculator.directory)
    current_tempdir = calculator.directory
    calculator._make_new_tmp_directory()
    assert os.path.exists(os.path.join(os.path.abspath(calculator.directory),
                                       calculator._potential_path))
    assert calculator.directory == current_tempdir
    calculator._directory = None
    calculator._make_new_tmp_directory()
    assert calculator.directory != current_tempdir
    assert os.path.exists(os.path.join(os.path.abspath(calculator.directory),
                                       calculator._potential_path))


@pytest.mark.parametrize('calculator',
                         [(3, False)], indirect=['calculator'],
                         )
def test_set_atoms(PbTe, calculator):
    """Tests set_atoms function"""
    assert calculator.atoms is None
    calculator.set_atoms(PbTe)
    assert isinstance(calculator.atoms, Atoms)


@pytest.mark.parametrize('calculator',
                         [(3, False)], indirect=['calculator'],
                         )
def test_set_directory(calculator, tmpdir):
    """Tests set_directory function"""
    assert calculator._use_temporary_directory
    calculator.set_directory(tmpdir)
    assert calculator.directory == tmpdir
    assert not calculator._use_temporary_directory
    assert os.path.exists(os.path.join(os.path.abspath(tmpdir), calculator._potential_path))


@pytest.mark.parametrize('calculator, expected_energy',
                         [((3, True), -4.8564407825),
                          ((3, False), -4.8564407825),
                          ((2, False), 58)],
                         indirect=['calculator'],
                         )
def test_calculator_reuse(PbTe, calculator, expected_energy):
    """Test that calculator can be reused with different atoms object."""
    PbTe.calc = calculator
    e = PbTe.get_potential_energy()
    assert abs(e - expected_energy) < 1e-5
    new_structure = PbTe.repeat(2)
    new_structure.calc = calculator
    e = new_structure.get_potential_energy()
    assert abs(e - 8 * expected_energy) < 1e-5
