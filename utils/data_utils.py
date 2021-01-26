from numpy import histogram,hsplit,vsplit,average
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import zscore




def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    #ax.set_xticks(np.arange(data.shape[1]))
    #ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Let the horizontal axes labeling appear on top.
    #ax.tick_params(top=True, bottom=False,
    #               labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

def get_histogram(areas,scale,ignore=20):
    new_areas = [area * (scale*scale) for area in areas]
    filtered = list(filter(lambda x: x>ignore,new_areas))
    hist,bins = histogram(filtered,30)
    print(hist)
    return hist,bins


def get_porosity_heatmap(img_name,img_grid,pore_grid,path):
    #plt.clf()
    plt.title("Porosity of " + img_name)

    #cols = range(0,800,int(800/len(img_grid[1])))
    #rows = range(0, 800, int(800 / len(img_grid)))
    #fmt = matplotlib.ticker.FuncFormatter(lambda x, pos: qrates[::-1][norm(x)])
    x_axis = np.array([i for i in range(0,800,int(len(pore_grid)))])
    y_axis = np.array([i for i in range(0,700,int(700/len(pore_grid)))])

    pore_im,pore_ax= heatmap(np.array(pore_grid), y_axis, x_axis,
                    cmap="magma_r", #norm=norm,
                    cbar_kw=dict(ticks=np.arange(0, 1),),
                    cbarlabel="Porosity")
    text = annotate_heatmap(pore_im,valfmt="{x:.2f}")
    plt.savefig('.'+path + '/' + img_name[:-4] + "_pore_heatmap.png")
    plt.close()
    #plt.show()
    #plt.clf()
    return path + '/' + img_name[:-4] + "_pore_heatmap.png"


def split_up_image(image,num = 8):
    img_grid = []
    pore_grid = []
    h_img = vsplit(image,num)
    for row in h_img:
        cols = hsplit(row,num)
        pore_row=[]
        for cell in cols:
            print("Average is:", average(cell))
            pore_row.append(average(cell))
        pore_grid.append(pore_row)
        img_grid.append(cols)
    z_pore_grid = zscore(pore_grid)
    return img_grid,pore_grid,z_pore_grid

