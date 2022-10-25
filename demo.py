from ctypes import alignment
from pprint import pformat
from xml.dom.minidom import Element
import PySimpleGUI as sg
from demo_utils.latexrender import latex_to_base64
from dots_output import parse_tree_to_base64
from parsing.parser import parse
from pp.PP import format_node
from pp.tree_cleaner import remove_paren, tree_cleaner


def node_to_latex(node):
    return format_node(remove_paren(node))


def single_element_window(title, element) -> sg.Window:
    return sg.Window(title, [[element]], finalize=True)


def img_window(title, key):
    return single_element_window(title, sg.Image(key=key))


def text_window(title, key):

    return single_element_window(
        title,
        sg.Text(
            key=key,
            size=(40, 10),
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
            expand_x=True,
            pad=(20, 0),
            size=(40, 1),
            key="text",
            justification="center",
            text_color="black",
            background_color="white",
        )
    ],
    [sg.Text("Rendered Latex")],
    [sg.Image(key="rendered")],
]
tree_layout = [
    [sg.Text("Parse Tree")],
    [
        sg.Column(
            [
                [
                    sg.Text(
                        "",
                        expand_x=True,
                        expand_y=True,
                        size=(30, 5),
                        key="text",
                        text_color="black",
                        background_color="white",
                    )
                ],
            ]
        ),
        sg.Column(
            [
                [sg.Text("Rendered Tree")],
                [sg.Image(key="rendered")],
            ]
        ),
    ],
]


def start():
    windows = {
        "tree": sg.Window("Parse Tree", tree_layout, finalize=True),
        "latex": sg.Window("Latex", latex_layout, finalize=True),
        "main": sg.Window("Pyisson", layout, finalize=True),
    }

    start_event_loop(windows)
    for win in windows.values():
        win.close()


def start_event_loop(windows: dict[str, sg.Window]):

    while True:
        window, event, values = sg.read_all_windows()  # type: ignore
        # print(event)
        # print(values)
        print(event, values)

        if event in ["In", "cleanbox"]:
            text = values["In"]  # type: ignore
            if text is not None and text != "":
                display = ""

                try:
                    parsed = parse(text)
                    if values["cleanbox"]:  # type: ignore
                        parsed = tree_cleaner(parsed)
                    display = pformat(parsed)
                    latex = node_to_latex(parsed)
                    windows["latex"]["text"].update(latex)  # type: ignore
                    windows["latex"]["rendered"].update(data=latex_to_base64(latex))
                    windows["tree"]["rendered"].update(
                        data=parse_tree_to_base64(parsed)
                    )
                except ValueError as e:
                    display = format_exeption(e)

                windows["tree"]["text"].update(display)  # type: ignore
            else:
                windows["tree"]["text"].update("")  # type: ignore
                windows["tree"]["rendered"].update(data=sg.BLANK_BASE64)
                windows["latex"]["text"].update("")  # type: ignore
                windows["latex"]["rendered"].update(data=sg.BLANK_BASE64)

        if event == sg.WINDOW_CLOSED:
            break

        rerender = False


def format_exeption(e):
    return repr(e)
