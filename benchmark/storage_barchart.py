import matplotlib.pyplot as plt
import numpy as np

KB = 1024
MB = KB * 1024
GB = MB * 1024


def storage_barchart():
    plt.title('Storage capacity in PostgreSQL (for 7.450.965 molecules), GB')
    x = np.array(["Not compressed", "LZ4-compressed"])
    y = np.array([1_952_152_830 / GB, 1_624_066_168 / GB])


    plt.bar(x, y)
    plt.xlabel('fingerprints', loc='right')
    plt.ylabel('GB')

    plt.savefig("storage.png", format='png')
