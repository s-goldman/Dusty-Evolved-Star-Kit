def grams_fit():
    def make_output_files_grams():
        with open("fitting_results.csv", "w") as f:
            f.write("source,L,rin,teff,tinner,odep,mdot\n")
            f.close()
        with open("fitting_plotting_outputs.csv", "w") as f:
            f.write("target_name,data_file,norm,index,grid_name,teff,tinner,odep\n")
            f.close()

    make_output_files_grams()
    # pdb.set_trace()
    luminosity = grid_outputs[model_index]["lum"] * ((distance_value / 50) ** 2)
    teff = grid_outputs[model_index]["teff"]
    tinner = grid_outputs[model_index]["tinner"]
    odep = grid_outputs[model_index]["odep"]
    mdot = grid_outputs[model_index]["mdot"] * (distance_value / 50)
    rin = grid_outputs[model_index]["rin"] * (distance_value / 50)
    # creates output file
    latex_array = [
        target_name,
        luminosity,
        rin,
        teff,
        tinner,
        odep,
        "%.3E" % float(mdot),
    ]

    plotting_array = [
        target_name,
        target,
        trials[trial_index],
        model_index,
        model_grid,
        teff,
        odep,
    ]
    if config.output["printed_output"] == "True":
        print()
        print()
        print(
            (
                "             Target: "
                + target_name
                + "        "
                + str(counter.value + 1)
                + "/"
                + str(number_of_targets)
            )
        )
        print("-------------------------------------------------")
        print(("Luminosity\t\t\t|\t" + str(round(luminosity))))
        print(
            (
                "Optical depth\t\t\t|\t"
                + str(round(grid_outputs[model_index]["odep"], 3))
            )
        )
        print(("Inner Radius\t\t\t|\t" + str(rin)))
        print(("Dust production rate \t\t|\t" + str("%.2E" % float(mdot))))
        print("-------------------------------------------------")
    with open("fitting_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(np.array(latex_array))
        f.close()

    with open("fitting_plotting_outputs.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(np.array(plotting_array))
        f.close()
    counter.value += 1
