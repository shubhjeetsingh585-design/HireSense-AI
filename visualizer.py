import matplotlib.pyplot as plt
import os
import uuid


def save_plot(fig):
    filename = f"static/{uuid.uuid4().hex}.png"
    os.makedirs("static", exist_ok=True)
    fig.savefig(filename, bbox_inches="tight")
    plt.close(fig)
    return filename


# Bar Chart (ATS)
def create_ats_bar_chart(before, after):
    fig = plt.figure()
    plt.bar(["Before", "After"], [before, after])
    plt.title("ATS Score Comparison")
    plt.ylabel("Score")

    return save_plot(fig)


# Pie Chart (Generic - JD / Resume Skills)
def create_pie_chart(title, labels):
    fig = plt.figure()

    if not labels:
        labels = ["No Data"]

    sizes = [1] * len(labels)

    plt.pie(
        sizes,
        labels=labels,
        startangle=90  # better visual alignment
    )

    plt.title(title)

    return save_plot(fig)