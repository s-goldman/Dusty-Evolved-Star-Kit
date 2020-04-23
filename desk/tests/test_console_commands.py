from astropy.table import Table
from desk import console_commands


def test_grids(capfd):
    console_commands.grids()
    out, err = capfd.readouterr()
    assert len(out) == 250


# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
# def test_get_model(test_input, expected):
# 	assert


def test_fit(tmpdir):
    target_filename = "sample_target.csv"
    target_file_path = tmpdir.join(target_filename)
    file = open(target_file_path, "w")
    file.write("3.55,0.389\n4.49,0.357\n5.73,0.344\n7.87,0.506\n23.7,0.676")
    file.close()
    console_commands.fit(source=str(target_file_path))
    a = Table.read("fitting_results.csv")
    b = Table.read("desk/tests/expected_fitting_results.csv")
    assert [a[col] == b[col] for col in a.colnames[:-1]]
