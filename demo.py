from ctypes import alignment
from pprint import pformat
from xml.dom.minidom import Element
import PySimpleGUI as sg
from demo_utils.latexrender import latex_to_base64
from parsing.parser import parse
from pp.PP import format_node
from pp.tree_cleaner import tree_cleaner


def node_to_latex(node, clean=True):
    n = node
    if clean:
        n = tree_cleaner(node)

    return format_node(n)


def single_element_window(title, element) -> sg.Window:
    return sg.Window(title, [[element]], finalize=True)


def img_window(title, key):
    return single_element_window(title, sg.Image(key=key))


def text_window(title, key):

    return single_element_window(
        title,
        sg.Text(
            key=key,
            size=(80, 10),
            expand_x=True,
        ),
    )


# main.parse()

left = [[sg.InputText(key="In", enable_events=True, size=(10, 1))]]
right = [
    [sg.Text("Test")],
    [
        sg.Text(
            "",
            key="Out",
            size=(40, 5),
            text_color="black",
            background_color="white",
            expand_x=True,
        )
    ],
]

layout = [
    [sg.Text("Math Expression")],
    [sg.Checkbox("Clean Latex", key="cleanbox", enable_events=True)],
    [sg.InputText(key="In", enable_events=True, size=(40, 1))],
]

latex_layout = [
    [sg.Text("Latex Code")],
    [
        sg.Text(
            "",
            size=(10, 1),
            expand_x=True,
            key="text",
            justification="center",
            text_color="black",
            background_color="white",
        )
    ],
    [sg.Text("Rendered Latex")],
    [sg.Image(key="rendered")],
]


def start():
    windows = {
        "main": sg.Window("Pyisson Demo", layout, finalize=True),
        "tree": text_window("Parse Tree", "tree"),
        "latex": sg.Window("Latex", latex_layout, finalize=True),
    }

    start_event_loop(windows)
    for win in windows.values():
        win.close()


def start_event_loop(windows: dict[str, sg.Window]):
    clean = (False,)
    rerender = (True,)
    while True:
        rerender = False
        window, event, values = sg.read_all_windows()  # type: ignore
        # print(event)
        # print(values)
        if "cleanbox" == event:
            clean = values["cleanbox"]  # type: ignore
            rerender = True

        if "In" == event:
            rerender = True

        if rerender:
            text = values["In"]  # type: ignore
            if text is not None and text != "":
                display = ""

                try:
                    parsed = parse(text)
                    display = pformat(parsed)
                    latex = node_to_latex(parsed, clean)
                    windows["latex"]["text"].update(latex)  # type: ignore
                    windows["latex"]["rendered"].update(data=latex_to_base64(latex))
                except ValueError as e:
                    display = format_exeption(e)

                windows["tree"]["tree"].update(display)  # type: ignore
            else:
                windows["tree"]["tree"].update("")  # type: ignore

        if event == sg.WINDOW_CLOSED:
            break


def format_exeption(e):
    return repr(e)
