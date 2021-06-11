import os
import pytest
import numpy as np
from desk import console_commands
from desk.set_up import config
from PIL import Image


def assert_images_equal(image_1: str, image_2: str):
    # Function care of Jennifer Helsby @redshiftzero
    img1 = Image.open(image_1)
    img2 = Image.open(image_2)

    # Convert to same mode and size for comparison
    img2 = img2.convert(img1.mode)
    img2 = img2.resize(img1.size)

    sum_sq_diff = np.sum(
        (np.asarray(img1).astype("float") - np.asarray(img2).astype("float")) ** 2
    )

    if sum_sq_diff == 0:
        # Images are exactly the same
        pass
    else:
        normalized_sum_sq_diff = sum_sq_diff / np.sqrt(sum_sq_diff)
        assert normalized_sum_sq_diff < 0.001


@pytest.fixture
def image_similarity(request, tmpdir):
    testname = request.node.name
    # filename = "{}.png".format(testname)
    generated_file = os.path.join(str(tmpdir), "{}.png".format(testname))

    yield {"filename": generated_file}

    assert_images_equal(
        "desk/tests/baseline_images/{}.png".format(testname), generated_file
    )


def test_grids(capfd):
    # checks if characters printed is what is expected (chars).
    chars = 291
    console_commands.grids()
    out, _ = capfd.readouterr()
    np.testing.assert_allclose(len(out), chars, err_msg=("Print grids error"))


def create_sample_data(directory, dataset):
    """Creates sample datasets for testing and saves it to a two column csv.

    Parameters
    ----------
    directory : str
        Directory to write csv file to.
    dataset : int
        The integer associated with each sample testing dataset.

    Returns
    -------
    type : csv file
        two column csv file with wavelength (um) and flux (Jy).

    """
    target_filename = "sample_target_" + str(dataset) + ".csv"
    target_file_path = str(directory.join(target_filename))
    file = open(target_file_path, "w")
    # simple dataset
    if dataset == 1:
        file.write("3.55,0.389\n4.49,0.357\n5.73,0.344\n7.87,0.506\n23.7,0.676")
    # longer dataset
    if dataset == 2:
        file.write("1.2,0.4\n1.5,0.1\n1.6,0.1\n1.7,0.2\n2,0.7\n5,1.0\n40,0.676")
    # out of order and bad fluxes
    if dataset == 3:
        file.write("1,0.389\n4,0.357\n3,0.344\n10,0\n40,-90")
    # # not enough sources (failure)
    # if dataset == 4:
    #     file.write("1,0.389\n4,0.357")
    file.close()
    return target_file_path


def create_fitting_results(directory):
    """Creates sample datasets for testing and saves it to a two column csv.

    Parameters
    ----------
    directory : str
        Directory to write csv file to.

    Returns
    -------
    type : csv file
        two column csv file with wavelength (um) and flux (Jy).

    """
    target_filename = "fitting_results.csv"
    target_file_path = str(directory.join(target_filename))
    file = open(target_file_path, "w")
    file.write(
        "source, grid, teff, tinner, model_id, odep, norm, L, vexp, mdot,file_name\n"
    )
    file.write(
        "sample_target_1,Oss-Orich-bb,1,1,17,1,-11.71113474978662,1,1,1,"
        + str(directory)
        + "/sample_target_1.csv\n"
    )
    file.write(
        "sample_target_2,Oss-Orich-bb,1,1,16,1,-11.71113474978662,1,1,1,"
        + str(directory)
        + "/sample_target_2.csv\n"
    )
    file.write(
        "sample_target_3,Oss-Orich-bb,1,1,36,1,-11.71113474978662,1,1,1,"
        + str(directory)
        + "/sample_target_3.csv\n"
    )
    # # not enough sources (failure)
    # if dataset == 4:
    #     file.write("1,0.389\n4,0.357")
    file.close()
    return target_file_path


@pytest.mark.parametrize("dataset", [1, 2, 3])
@pytest.mark.parametrize(
    "testing_grid",
    config.grids + config.external_grids + ["grams"] + ["oxygen"] + ["carbon"],
)
def test_single_fit(tmpdir, testing_grid, dataset):
    # tests single fit for each sample dataset and each grid
    example_filename = create_sample_data(tmpdir, dataset)
    console_commands.fit(
        source=str(example_filename),
        grid=testing_grid,
        n=2,
        multiprocessing=False,
        testing=True,
    )


def test_single_fit_options(tmpdir):
    # testing single fit user options
    example_filename = create_sample_data(tmpdir, 2)
    console_commands.fit(
        source=str(example_filename),
        distance=0.1,
        grid="oxygen",
        n=2,
        min_wavelength=1,
        max_wavelength=100,
        testing=True,
    )


# test working locally but not on github-actions
# def test_single_sed(tmpdir, image_similarity):
#     # test for single SED figure
#     create_sample_data(tmpdir, 1)
#     create_sample_data(tmpdir, 2)
#     create_sample_data(tmpdir, 3)
#     create_fitting_results(tmpdir)
#     console_commands.sed(
#         source_path=tmpdir.strpath,
#         source_filename="fitting_results.csv",
#         dest_path=tmpdir.strpath,
#         save_name="test_single_sed.png",
#     )


# def test_multiple_fit(tmpdir):
#     # test for multiple SED fit with SED figure
#     create_sample_data(tmpdir, 1)
#     create_sample_data(tmpdir, 2)
#     create_sample_data(tmpdir, 3)
#     example_fitting_results = create_fitting_results(tmpdir)
#     console_commands.sed_indiv(
#         source_path=tmpdir.strpath,
#         source_filename="fitting_results.csv",
#         dest_path=tmpdir.strpath,
#     )
