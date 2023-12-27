import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time

import h5rdmtoolbox as h5tbx

datas = [np.ones(shape=(i, i)) * 1.5 for i in [11, 115, 1150, 5300, 11500]]
# datas = [np.ones(shape=(i, i)) * 1.5 for i in [11, 115, 1150]]#, 5300, 11500]]
Ni = 10

times_h5tbx_m = []
times_h5tbx_s = []
file_sizes = []
for data in datas:
    _tmp = []
    for i in range(Ni):
        filename_h5tbx = h5tbx.utils.generate_temporary_filename()
        t0 = time.perf_counter()
        with h5tbx.File(filename_h5tbx, 'w') as h5:
            h5.create_dataset('test', data=data)
        _tmp.append(time.perf_counter() - t0)
        if i == 0:
            with h5tbx.File(filename_h5tbx, 'r') as h5:
                print(h5.filesize.to('MB'))
                file_sizes.append(h5.filesize.to('MB').magnitude)
        filename_h5tbx.unlink()
    times_h5tbx_m.append(np.mean(_tmp))
    times_h5tbx_s.append(np.std(_tmp))

times_h5py_m = []
times_h5py_s = []
for data in datas:
    _tmp = []
    for i in range(Ni):
        filename_h5py = h5tbx.utils.generate_temporary_filename()
        t0 = time.perf_counter()
        with h5py.File(filename_h5py, 'w') as h5:
            h5.attrs['__h5rdmtoolbox_version__'] = '1.0.0'
            h5.create_dataset('test', data=data)
        _tmp.append(time.perf_counter() - t0)
        if i == 0:
            with h5tbx.File(filename_h5py, 'r') as h5:
                print(h5.filesize.to('MB'))
        filename_h5py.unlink()
    times_h5py_m.append(np.mean(_tmp))
    times_h5py_s.append(np.std(_tmp))

print(times_h5py_m, times_h5py_s)
print(times_h5tbx_m, times_h5tbx_s)

golden_ratio = (np.sqrt(5.0) - 1.0) / 2.0  # Aesthetic ratio (you could change this)
golden_mean = 9 / 16  # This is suited for widescreen ppt

LATEX_TEXTWIDTH_MM = 160  # mm
LATEX_TEXTWIDTH_IN = LATEX_TEXTWIDTH_MM / 25.4  # in


def goldenfigsize(scale, hscale=1, gr=True):
    """Set figure size to golden ratio

    Parameter
    ---------
    scale : float
        Scale factor for the figure size
    hscale : float
        Scale factor for the height of the figure
    gr : bool
        If True, use golden ratio, else use golden mean

    Returns
    -------
    fig_size : list[float]
        Figure size in inches
    """
    fig_width_inch = mpl.rcParams.get('figure.figsize')[0]
    if gr:
        ratio = golden_ratio  # Aesthetic ratio (you could change this)
    else:
        ratio = golden_mean  # This is suited for widescreen ppt
    fig_width = fig_width_inch * scale  # width in inches
    fig_height = fig_width * ratio * hscale  # height in inches
    fig_size = [fig_width, fig_height]
    return fig_size

x = [d.size for d in datas]
x = file_sizes
plt.figure()
plt.errorbar(x, y=times_h5tbx_m, yerr=times_h5tbx_s, label='h5tbx')
plt.errorbar(x, y=times_h5py_m, yerr=times_h5py_s, label='h5py')
plt.xlabel('array size')
plt.ylabel('creation time [s]')
plt.xscale('log')
plt.legend()
plt.draw()

plt.figure(figsize=goldenfigsize(1))
# plt.plot(x, np.asarray(times_h5tbx_m) / np.asarray(times_h5py_m))
plt.errorbar(x,
             y=np.asarray(times_h5tbx_m) / np.asarray(times_h5py_m),
             yerr=np.asarray(times_h5tbx_s) + np.asarray(times_h5py_s))
plt.xlabel('file size / MB')
plt.ylabel('h5tbx / h5py')
plt.xscale('log')
plt.tight_layout()
plt.draw()
plt.savefig('performance.png', dpi=300)
plt.savefig('performance.svg')
plt.show()
