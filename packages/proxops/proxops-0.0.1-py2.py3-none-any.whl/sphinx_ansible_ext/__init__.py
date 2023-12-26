from sphinx_ansible_ext.directives import setup_directives


def setup(app):
    """
    Initializer for Sphinx extension API.
    See http://www.sphinx-doc.org/en/stable/extdev/index.html#dev-extensions.
    """
    setup_directives(app)

    return {
        "parallel_read_safe": False,
        "parallel_write_safe": False,
        "version": "0.1.3",
    }
