from ..api import APIClient
from .resource import Model, Collection


class Volume(Model):

    id_attribute = 'Name'

    @property
    def name(self):
        return self.attrs['Name']

    def remove(self, force=False):
        return self.client.api.remove_volume(self.id, force=force)


class VolumeCollection(Collection):

    model = Volume

    def create(self, name=None, **kwargs):
        obj = self.client.api.create_volume(name, **kwargs)
        return self.prepare_model(obj)

    def get(self, volume_id):

        return self.prepare_model(self.client.api.inspect_volume(volume_id))

    def list(self, **kwargs):
        resp = self.client.api.volumes(**kwargs)
        if not resp.get('Volumes'):
            return []
        return [self.prepare_model(obj) for obj in resp['Volumes']]

    def prune(self, filters=None):
        return self.client.api.prune_volumes(filters=filters)
    prune.__doc__ = APIClient.prune_volumes.__doc__
