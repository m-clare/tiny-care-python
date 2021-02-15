import re
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def horizontal_bar_labels(categories):
    """
    From https://dkane.net/2020/better-horizontal-bar-charts-with-plotly/
    """
    subplots = make_subplots(
        rows=len(categories),
        cols=1,
        subplot_titles=['<b>{0} - {1}</b>'.format(x["name"], x["value"])
                        for x in categories],
        shared_xaxes=True,
        print_grid=False,
        vertical_spacing=(0.70 / len(categories)),
    )
    subplots['layout'].update(
        width=400,
        plot_bgcolor='#fff',
    )
    subplots.update_layout(
        font_family="Dank Mono")

    # hide axes
    for axis in subplots['layout']:
        if axis.startswith('yaxis') or axis.startswith('xaxis'):
            subplots['layout'][axis]['visible'] = False

    # add bars for the categories
    for k, val in enumerate(categories):
        subplots.add_trace(dict(
            type='bar',
            orientation='h',
            y=[val["name"]],
            x=[val["value"]],
            marker=dict(
                color="#FF0000",
            ),
        ), k+1, 1)

    # update the layout
    subplots['layout'].update(
        showlegend=False,
    )
    for x in subplots["layout"]['annotations']:
        x['font'] = dict(
            size=20,
            color="black"
            # family="DankMono-Bold, monospace",
            # family="Consolas, monospace",
        )

    # update the margins and size
    subplots['layout']['margin'] = {
        'l': 0,
        'r': 0,
        't': 25,
        'b': 1,
    }
    height_calc = 60 * len(categories)
    print(height_calc)
    height_calc = max([height_calc, 350])
    subplots['layout']['height'] = height_calc
    subplots['layout']['width'] = 0.5 * height_calc

    return subplots

def read_file(org_file):
    date_bins = {6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
    now = datetime.date.today() 
    prev_line = ""
    with open(org_file) as fp:
        for line in fp:
            if "CLOSED" in line:
                m = re.search(r'(\d{4}-\d{2}-\d{2})', line).group(1)
                found_date = datetime.date.fromisoformat(m)
                difference = (now - found_date).days
                if difference < 7:
                    date_bins[difference] += 1
            else:
                prev_line = line
    return date_bins 

fp = "/Users/maryannewachter/dropbox/org/tiny-care-test.org"

dateFormatted = datetime.date.today().strftime("%a")
vals = read_file(fp)
x = list(vals.keys())
y = list(vals.values())
text = [(datetime.date.today() - datetime.timedelta(i)).strftime("%a").upper() for i in x]
categories = []
for i in range(len(text)):
    categories.append({'name': text[i], 'value': y[i]})
subplots = horizontal_bar_labels(categories)
subplots.show()
subplots.write_image("test.png", format="png", width=150, height=300)

if __name__ == " __main__":
    pass
