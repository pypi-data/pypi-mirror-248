from browser import html as html_
from browser import document as document_


########################################################################
class class_(list):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, element, classes):
        """"""
        super().__init__(filter(None, classes.split(' ')))
        self.element = element

    # ----------------------------------------------------------------------
    def __setitem__(self, key, value):
        """"""
        ret = super().__setitem__(key, value)
        self.element.class_name = ' '.join(self)
        return ret

    # ----------------------------------------------------------------------
    def append(self, item):
        """"""
        ret = super().append(item.strip())
        self.element.class_name = ' '.join(self)
        return ret

    # ----------------------------------------------------------------------
    def extend(self, items):
        """"""
        ret = super().extend([item.strip() for item in items])
        self.element.class_name = ' '.join(self)
        return ret

    # ----------------------------------------------------------------------
    def insert(self, index, item):
        """"""
        ret = super().insert(index, item.strip())
        self.element.class_name = ' '.join(self)
        return ret


########################################################################
class select(list):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, selector):
        """Constructor"""
        super().__init__(document_.select(selector))

    # ----------------------------------------------------------------------
    def __getattr__(self, attr):
        """"""
        if attr == 'style':
            return self.style_()

        def inset(*args, **kwargs):
            return [getattr(element, attr)(*args, **kwargs) for element in self]

        return inset

    # ----------------------------------------------------------------------
    def __setattr__(self, attr, value):
        """"""
        for element in self:
            setattr(element, attr, value)

    # ----------------------------------------------------------------------
    def style_(self):
        """"""
        class Style:
            def __setattr__(cls, attr, value):
                """"""
                for element in self:
                    setattr(element.style, attr, value)
        return Style()

    # ----------------------------------------------------------------------
    def __le__(self, other):
        """"""
        for element in self:
            element <= other


########################################################################
class html_context:
    """"""
    _context = []

    # ----------------------------------------------------------------------
    def __init__(self, element):
        self._element = element
        self._parent = html_context._context[-1] if html_context._context else None

    # ----------------------------------------------------------------------
    def __enter__(self):
        if self._parent:
            self._parent <= self._element
        html_context._context.append(self._element)
        return self._element

    # ----------------------------------------------------------------------
    def __exit__(self, exc_type, exc_val, exc_tb):
        html_context._context.pop()

    # ----------------------------------------------------------------------
    def __setattr__(self, attr, value):
        """"""
        if attr.startswith('_'):
            return super().__setattr__(attr, value)
        if hasattr(self._element, attr):
            setattr(self._element, attr, value)
        else:
            super().__setattr__(attr, value)

    # ----------------------------------------------------------------------
    def __call__(self, parent):
        """"""
        self._parent = parent
        self._parent <= self._element
        return self


########################################################################
class HTML:
    """"""

    def __getattribute__(self, attr):
        """"""
        def inset(*args, **kwargs):
            html_e = getattr(html_, attr)(*args, **kwargs)
            html_e.classes = class_(html_e, kwargs.get('Class', ''))
            html_e.context = html_context(html_e)
            return html_e
        return inset


html = HTML()
