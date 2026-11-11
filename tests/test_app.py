from streamlit.testing.v1 import AppTest

app = AppTest.from_file("../app.py").run()

def test_calculator_displays_total():

    assert not app.exception
    assert any(
        element.value == "Total: $20.00"
        for element in app.markdown
    )


def test_calculator_updates_total():

    app.number_input[0].set_value(5.0).run()

    assert any(
        element.value == "Total: $10.00"
        for element in app.markdown
    )
