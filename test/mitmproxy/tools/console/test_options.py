def test_toggle_upstream_certs_without_upstream_cert_shows_error(console, monkeypatch):
    """Reject an invalid boolean toggle in the options UI instead of crashing.

    Regression test for https://github.com/mitmproxy/mitmproxy/issues/2876.
    """
    console.options.update(upstream_cert=False)
    assert console.options.add_upstream_certs_to_client_chain is False

    console.type("O")
    options = console.window.current("options")
    index = options.optionslist.walker.opts.index("add_upstream_certs_to_client_chain")
    options.optionslist.set_focus(index)
    # Status text is shortened to the current terminal width. Give the error room
    # so the assertion does not depend on the host terminal size.
    monkeypatch.setattr(console.ui, "get_cols_rows", lambda: (120, 40))

    console.type("<enter>")

    assert console.options.add_upstream_certs_to_client_chain is False
    assert console.options.upstream_cert is False
    status = console.window.statusbar.ab.top._w.get_text()[0]
    assert (
        status
        == "add_upstream_certs_to_client_chain requires the upstream_cert option to be enabled."
    )
    visible = " ".join(console.screen_contents().split())
    assert status in visible
    assert "add_upstream_certs_to_client_chain false" in visible


def test_toggle_boolean_option(console):
    assert console.options.showhost is False

    console.type("O")
    options = console.window.current("options")
    index = options.optionslist.walker.opts.index("showhost")
    options.optionslist.set_focus(index)

    console.type("<enter>")

    assert console.options.showhost is True
    visible = " ".join(console.screen_contents().split())
    assert "showhost true" in visible
