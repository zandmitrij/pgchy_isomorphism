import datetime
import typing as tp

import matplotlib.pyplot as plt
import seaborn as sns
from typing_extensions import Self


def read_data_file(path: str):
    with open(path, 'r') as f:
        return map(float, f.readlines())


def get_label(filename: str) -> str:
    return ' '.join(filename.strip('.txt').title().split('_'))


class Data(tp.NamedTuple):
    filename: str
    label: str
    data: tp.List[float]

    @classmethod
    def create(cls, filepath: str) -> Self:
        filename = filepath.split('/')[-1]
        data = list(read_data_file(filepath))
        label = get_label(filename)
        return cls(filename=filename, data_label=label, data=data)


def main():
    files = [
        'bencmark_compressed.txt',
        'bencmark_not_compressed.txt',
    ]
    datafiles = [Data.create(filename) for filename in files]

    plt.figure(figsize=(10, 6))

    plt.legend()
    plt.title("Dist")
    plt.xlabel("Seconds")
    plt.ylabel("Density")

    for datafile in datafiles:
        sns.histplot(datafile.data, label=datafile.label, kde=True, stat="density", alpha=0.6)

    figname = datetime.datetime.now()

    plt.savefig(f"{figname}.png", format='png')


if __name__ == "__main__":
    main()
