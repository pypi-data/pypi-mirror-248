class Model:
    id_attribute = 'Id'

    def __init__(self, attrs=None, client=None, collection=None):
        self.client = client
        self.collection = collection
        self.attrs = attrs
        if self.attrs is None:
            self.attrs = {}

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.short_id}>"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        return hash(f"{self.__class__.__name__}:{self.id}")

    @property
    def id(self):
        return self.attrs.get(self.id_attribute)

    @property
    def short_id(self):
        return self.id[:12]

    def reload(self):

        new_model = self.collection.get(self.id)
        self.attrs = new_model.attrs


class Collection:
    model = None

    def __init__(self, client=None):
        self.client = client

    def __call__(self, *args, **kwargs):
        raise TypeError(
            f"'{self.__class__.__name__}' object is not callable. "
            "You might be trying to use the old (pre-2.0) API - "
            "use docker.APIClient if so."
        )

    def list(self):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def create(self, attrs=None):
        raise NotImplementedError

    def prepare_model(self, attrs):
        """
        Create a model from a set of attributes.
        """
        if isinstance(attrs, Model):
            attrs.client = self.client
            attrs.collection = self
            return attrs
        elif isinstance(attrs, dict):
            return self.model(attrs=attrs, client=self.client, collection=self)
        else:
            raise Exception(f"Can't create {self.model.__name__} from {attrs}")
