
import numpy as np
import matplotlib.pyplot as plt


def _invert(x, limits):
    '''
    inverts a value x on a scale from limits[0] to limits[1]
    '''
    return limits[1] - (x - limits[0])


def _scale_data(data, ranges):
    '''
    scales data[1:] to ranges[0],
    inverts if the scale is reversed
    '''
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    d = data[0]
    if x1 > x2:
        d = _invert(d, (x1, x2))
        x1, x2 = x2, x1
    sdata = [d]
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        sdata.append((d - y1) / (y2 - y1) * (x2 - x1) + x1)
    return sdata


class RadarGraph():
    def __init__(self, fig, variables, ranges, levels=6,title='Radar Graph'):
        angles = np.arange(0, 360, 360. / len(variables))
        axes = [fig.add_axes([0.1, 0.1, 0.9, 0.9], polar=True,
                             label='axes{}'.format(i))
                for i in range(len(variables))]

        l, text = axes[0].set_thetagrids(angles, labels=variables)

        [txt.set_rotation(angle - 90) for txt, angle
            in zip(text, angles)]

        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid('off')
            ax.xaxis.set_visible(False)
        for i, ax in enumerate(axes):
            grid = np.linspace(*ranges[i], num=levels)
            gridlabel = ['{}'.format(round(x,2)) for x in grid]
            if ranges[i][0] > ranges[i][1]:
                grid = grid[::-1]  # invert grid
            gridlabel[0] = ''  # clean up origin
            ax.set_rgrids(grid, labels=gridlabel,
                          angle=angles[i])
            ax.set_ylim(*ranges[i])

        #variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]
        self.title = title
    def plot(self, data, *args, **kw):
        sdata = _scale_data(data,self.ranges)
        self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
        self.ax.set_title(self.title,fontsize=20)
    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
    def circles(self, radii, colors, alpha=0.4):
        # Add reference colors
        for r, color in zip(radii, colors):
            self.ax.add_artist(plt.Circle((0.0, 0.0), r, transform=self.ax.transData._b, color=color,alpha=alpha))

















