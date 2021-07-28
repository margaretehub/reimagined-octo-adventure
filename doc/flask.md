## Discovering flask python web server


The default response type of flask is HTML. It's possible to build web services and websites with **GET** and **POST** methods.

For a web application it's important to work with the data a client sends to the server. In flask this is done by the **request object**.

An object that is **global** but also **threadsafe**

## The Context Locals Approach:


## [MarkupSafe:](https://markupsafe.palletsprojects.com/en/2.0.x/)

MarkupSafe escapes characters so text is safe to use in HTML and XML.
Characters that have special meanings are replaced so that they display as the actual characters.

A quote from a source code commit:

´´´
python
class Markup(str):
    """A string that is ready to be safely inserted into an HTML or XML
    document, either because it was escaped or because it was marked
    safe.
    Passing an object to the constructor converts it to text and wraps
    it to mark it safe without escaping. To escape the text, use the
    :meth:`escape` class method instead.
    >>> Markup("Hello, <em>World</em>!")
    Markup('Hello, <em>World</em>!')
    >>> Markup(42)
    Markup('42')
    >>> Markup.escape("Hello, <em>World</em>!")
    Markup('Hello &lt;em&gt;World&lt;/em&gt;!')
    This implements the ``__html__()`` interface that some frameworks
    use. Passing an object that implements ``__html__()`` will wrap the
    output of that method, marking it safe.
    >>> class Foo:
    ...     def __html__(self):
    ...         return '<a href="/foo">foo</a>'
    ...
    >>> Markup(Foo())
    Markup('<a href="/foo">foo</a>')
    This is a subclass of :class:`str`. It has the same methods, but
    escapes their arguments and returns a ``Markup`` instance.
    >>> Markup("<em>%s</em>") % ("foo & bar",)
    Markup('<em>foo &amp; bar</em>')
    >>> Markup("<em>Hello</em> ") + "<foo>"
    Markup('<em>Hello</em> &lt;foo&gt;')
    """

´´´

Pivotal methods are:



´´´
escape('any object')
# returns a Markupstring with the escaped text
Markup('any')
# creates an Markupobject
Markup('any').unescape()
# returns HTML in a string and replaces HTML entities
Markup('any').striptags()
# does even more: unescape() the markup and remove tags, and normalise whitespace to single spaces
Markup().escape('any')
# escapes..

´´´
