from pprint import pformat
from xml.dom.minidom import Element
import PySimpleGUI as sg
from demo_utils.latexrender import latex_to_base64
from parsing.parser import parse
from pp.PP import format_node


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
    [sg.Text("Hello")],
    [sg.InputText(key="In", enable_events=True, size=(10, 1))],
]


def start():
    windows = {
        "main": sg.Window("Pyisson Demo", layout, finalize=True),
        "tree": text_window("Parse Tree", "tree"),
        "latex": text_window("Latex", "latex"),
        "rendered": img_window("Latex Rendered", "latex"),
    }

    start_event_loop(windows)
    for win in windows.values():
        win.close()


def start_event_loop(windows: dict[str, sg.Window]):
    while True:
        window, event, values = sg.read_all_windows()  # type: ignore
        # print(event)
        # print(values)
        if "In" == event:
            text = values["In"]  # type: ignore
            if text is not None and text != "":
                display = ""

                try:
                    parsed = parse(text)
                    display = pformat(parsed)
                    latex = format_node(parsed)
                    windows["latex"]["latex"].update(latex)
                    windows["rendered"]["latex"].update(data=latex_to_base64(latex))
                except ValueError as e:
                    display = format_exeption(e)

                windows["tree"]["tree"].update(display)  # type: ignore
            else:
                windows["tree"]["tree"].update("")  # type: ignore

        if event == sg.WINDOW_CLOSED:
            break


def format_exeption(e):
    return repr(e)
