import numpy as np
import h5py
import matplotlib
import matplotlib.pyplot as plt

from core import plot_2d_array, make_colorbar
from pyx import math_tools
import core
filename = "/Users/abatten/PhD/test_gen_frb/interpolated_dm_map_z0.00.hdf5"

filename2 = "dm_z_pdf.npz"

data = np.load(filename2)["arr_0"]

rc_params = core.get_rcparam_settings()
matplotlib.rcParams.update(rc_params)

print(plt.rcParams)

fig, ax = plt.subplots(ncols=1, nrows=1)

data_redshifts = np.array(
      [0.        , 0.02271576, 0.04567908, 0.06890121, 0.09239378,
       0.1161688 , 0.1402387 , 0.16461634, 0.18931503, 0.21434853,
       0.23973108, 0.26547743, 0.29160285, 0.31812316, 0.34505475,
       0.37241459, 0.40022031, 0.42849013, 0.45724301, 0.48649858,
       0.51627725, 0.54660017, 0.57748936, 0.60896766, 0.64105881,
       0.67378753, 0.7071795 , 0.74126146, 0.77606125, 0.81160784,
       0.84793147, 0.88506357, 0.92303701, 0.96188603, 1.00164638,
       1.04235539, 1.08405204, 1.12677711, 1.1705732 , 1.21548489,
       1.26155887, 1.30884399, 1.35739143, 1.40725491, 1.45849065,
       1.51115776, 1.56531826, 1.62103729, 1.6783833 , 1.73742834,
       1.79824817, 1.86092257, 1.92553561, 1.99217588, 2.06093685,
       2.13191717, 2.20522104, 2.2809586 , 2.35924626, 2.44020723,
       2.52397206, 2.61067901, 2.70047481, 2.79351511, 2.88996519])








data_dm_values = np.linspace(-1, 5, 1000)

bin_centres = math_tools.calc_bin_centre(data_dm_values)
x = np.linspace(0, 2, 100)
y = x**2
plt.plot(x, y)

#extents = (0, 3.0, -1, 5)
#im = plot_2d_array(data, yvals=bin_centres, xvals=data_redshifts, cmap="magma", passed_ax=ax)
ax.set_ylim(1, 4)
ax.set_xlabel(r"$\rm{Redshift}$")
ax.set_ylabel(r"$\rm{DM}$")
plt.tight_layout()
plt.savefig("testing.png")
plt.show()


#with h5py.File(filename, "r") as f:
#    data = f["DM"][1000:7200, 1000:7200]
#
#    fig, ax = plt.subplots(ncols=1, nrows=1)
#    
#    extents = (0, 100, 0, 100)
#    im = plot_2d_array(data, extents=extents, cmap="magma", passed_ax=ax)
#    ax, cbar = make_colorbar(im, ax, label=r"$\rm{DM\ \left[pc\ cm^{-3}\right]}$", extend="max")
#    im.set_clim(vmin=0, vmax=300)
#    cbar.ax.tick_params(axis="y", direction="out")
    
#    ax.set_xlabel(r"$\rm{x\ \left[cMpc\right]}$")
#    ax.set_ylabel(r"$\rm{y\ \left[cMpc\right]}$")
 #   plt.tight_layout()

#    plt.savefig("this_is_a_test.png", dpi=300)
