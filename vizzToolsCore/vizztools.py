class Metadata:
    """
    This is the main Metadata class.
    Parameters
    ----------
    attributes: dic
        A dictionary holding the attributes of a metadata (which are attached to a Dataset).
    """
    def __init__(self, attributes=None):
        if attributes.get('type') != 'metadata':
            raise ValueError(f"Non metadata attributes passed to Metadata class ({attributes.get('type')})")
        self.type = 'Metadata'
        self.attributes = attributes.get('attributes')