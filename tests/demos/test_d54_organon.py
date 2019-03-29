import subprocess
import os
import math

def test_d54():
    ls_command = 'ls -p /demo-tests/d54'
    test_command = 'cd /demo-tests/d54 && bash import-dataset.sh ${PWD}/dataset ${PWD}/worker ${PWD}/invmat.yml'
    output_path = '/demo-tests/d54/{}commfile1.txt/OUTPUTS/output.out'
    folders_before = subprocess.check_output(ls_command, shell=True).split()
    subprocess.run([test_command], shell=True)
    folders_after = subprocess.check_output(ls_command, shell=True).split()
    new_job = list(set(folders_after).difference(set(folders_before)))[0]
    new_job = new_job.decode()

    with open(output_path.format(new_job)) as f:
        value1, value2 = [float(l.strip()) for l in f.readlines()]
        expected_result_1 = 1.583333333
        expected_result_2 = -0.83333333
        assert math.isclose(value1, expected_result_1, abs_tol=0.001)
        assert math.isclose(value2, expected_result_2, abs_tol=0.001)


def test_organon():
    ls_command = 'ls -p /demo-tests/organon'
    ctg_number = '1' #Paramater for the organon script
    output_path = '/demo-tests/organon/{}9bus-00.ntw-ctg1/OUTPUTS/STATIC.csv' #Output address without the job formatting
    expected_output_path = '/demo-tests/organon/expected_results.csv'
    test_command = 'cd /demo-tests/organon && bash import-dataset.sh ${PWD}/dataset ${PWD}/worker ${PWD}/organon.yml ' + ctg_number
    folders_before = subprocess.check_output(ls_command, shell=True).split()
    subprocess.run([test_command], shell=True)
    folders_after = subprocess.check_output(ls_command, shell=True).split()
    new_job = list(set(folders_after).difference(set(folders_before)))[0]
    new_job = new_job.decode()
    new_output = open(output_path.format(new_job)).read()
    expected_output = open(expected_output_path).read()
    assert new_output == expected_output
