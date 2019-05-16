import pycg_bonds as target
from pymol import cmd, stored, CmdException
import os

def test_get_chain_bb():
    cmd.reinitialize()
    selection = "cg_oligomer_nochains"
    cmd.load(selection+".pdb")
    chains = cmd.get_chains(selection)
    target.get_chain_bb(selection, chains)

test_list = [
        test_get_chain_bb
        ]

def run_tests(test_functions):
    # Fail count
    global fail_count
    fails = []

    # Move to testdir
    os.chdir("test")

    # Run all the tests, add exception to fails
    try:
        for test_func in test_functions:
            test_func()
    except Exception as e:
        fails.append(e)
    except CmdException as e:
        fails.append(e)
    
    # Report results
    print(str(len(fails))+" tests failed")
    if fails:
        for e in fails:
            print(e)
        exit(1)

run_tests(test_list)
