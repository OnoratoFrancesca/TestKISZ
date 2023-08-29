import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def create_horizontal_bar_chart(value):
    plt.figure(figsize=(10, 1))
    colors = ['green', 'yellow', 'red']
    cmap = mcolors.LinearSegmentedColormap.from_list('custom_colormap', colors, N=100)
    normalized_value = int((value - 0) / (100 - 0) * 100)
    plt.barh(['Schwierigkeit:'], [value], color=cmap(normalized_value))
    plt.yticks(['Schwierigkeit:'])
    plt.xticks(range(0, 101, 10), [''] * 11)
    plt.axis('on')
    return plt.gcf()

def test():
    value = 20
    fig = create_horizontal_bar_chart(value)
    plt.show()

if __name__ == "__main__":
    test()
