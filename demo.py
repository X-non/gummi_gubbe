from pprint import PrettyPrinter, pformat, pprint
import PySimpleGUI as sg
from demo_utils.latexrender import latex_to_base64
from parsing.parser import parse

# main.parse()

left = [[sg.InputText(key="In", enable_events=True, size=(10, 1))]]
right = [
    [sg.Text("Test")],
    [
        sg.Text(
            "",
            key="Out",
            size=(40, 10),
            text_color="black",
            background_color="white",
            expand_x=True,
        )
    ],
]

layout = [
    [
        sg.Text("Hello"),
    ],
    [sg.Image(key="img", data=latex_to_base64("\\frac{1}{2}"))],
    [sg.Column(left), sg.Column(right)],
]


def start():
    window = sg.Window("Pyisson Demo", layout)
    start_event_loop(window)
    window.close()


def start_event_loop(window: sg.Window):
    while True:
        event, values = window.read()  # type: ignore
        print(event)
        print(values)
        if "In" == event:
            text = values["In"]
            if text is not None and text != "":
                display = ""

                try:
                    display = ""  # pformat(parse(text))
                except ValueError as e:
                    display = format_exeption(e)
                window["Out"].update(display)  # type: ignore

                try:
                    window["img"].update(data=latex_to_base64(text))
                except ValueError:
                    pass

            else:
                window["Out"].update("")  # type: ignore

        if event == sg.WINDOW_CLOSED:
            break


def format_exeption(e):
    return repr(e)
