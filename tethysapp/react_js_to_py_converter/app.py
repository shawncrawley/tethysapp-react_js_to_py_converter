from tethys_sdk.components import ReactPyBase


class App(ReactPyBase):
    """
    Tethys app class for ReactJS to ReactPy Converter.
    """

    name = 'ReactJS to ReactPy Converter'
    description = 'Converts ReactJS code to workable ReactPy code'
    package = 'react_js_to_py_converter'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/icon.png'
    root_url = 'react-js-to-py-converter'
    color = '#c0392b'
    tags = ''
    enable_feedback = False
    feedback_emails = []
    exit_url = '/apps/'
    default_layout = "NavHeader"
    nav_links = "auto"


@App.page
def home(lib):
    lib.register("@monaco-editor/react", "me", use_default=True)
    full_height = "70vh"
    half_width = "49vw"
    reactjs_code, set_reactjs_code = lib.hooks.use_state("")
    reactpy_code, set_reactpy_code = lib.hooks.use_state("")
    accessor, set_accessor = lib.hooks.use_state("")
    
    return lib.bs.Container(fluid=True, style=lib.Props(padding="1em"))(
        lib.bs.Row(
            lib.bs.Col(style=lib.Props(width=half_width))(
                lib.me.Editor(
                    height=full_height,
                    language="javascript",
                    theme="vs-dark",
                    value=reactjs_code,
                    onChange=lambda c, _: set_reactjs_code(c),
                    options=lib.Props(
                        inlineSuggest=True, fontSize="16px", formatOnType=True
                    ),
                )
            ),
            lib.bs.Col(style=lib.Props(width=half_width))(
                lib.me.Editor(
                    height=full_height,
                    language="python",
                    theme="vs-dark",
                    value=reactpy_code,
                    onChange=lambda c, _: set_reactpy_code(c),
                    options=lib.Props(
                        inlineSuggest=True, fontSize="16px", formatOnType=True
                    ),
                )
            )
        ),
        lib.bs.Row(style=lib.Props(margin_top="1em"))(
           lib.bs.Col(
                lib.bs.Form(
                    lib.bs.FormGroup(className="mb-3", controlId="formAccessor")(
                        lib.bs.FormLabel(htmlFor="accessor")("Library Accessor"),
                        lib.bs.FormControl(
                            type="text",
                            id="accessor",
                            aria_describedby="accessorHelpBlock",
                            value=accessor, 
                            onChange=lambda e: set_accessor(e['target']['value']),
                        ),
                        lib.bs.FormText(
                            id="accessorHelpBlock", 
                            muted=True, 
                            width="100px"
                        )("""
                            This is the the library accessor that should be used for
                            the package you got this example from. For example, type "bs"
                            if you're pasting in React Bootstrap code.
                        """),
                    ),
                    lib.bs.Button(on_click=lambda e: set_reactpy_code(do_py_to_js_conversion(reactjs_code, accessor)))("Convert"),
                )
           ),
           lib.bs.Col(
                lib.bs.Button(on_click=lambda e: copy_to_clipboard(reactpy_code))("Copy"),
           ),
        ),
    )
