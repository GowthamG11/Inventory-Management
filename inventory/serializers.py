from rest_framework import serializers
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        exclude = ('status', )

    def __init__(self, *args, **kwargs):
        add_field = kwargs.pop('add_field', None)
        super(InventorySerializer, self).__init__(*args, **kwargs)
        print self.fields
        if add_field:
            # for multiple fields in a list
            self.fields.update({add_field: serializers.ChoiceField(choices=((u'approved', u'Approved'),
                                                                            (u'pending', u'Pending')))})

    def create(self, validated_data):
        print validated_data
        inventory_obj = Inventory(**validated_data)
        inventory_obj.status = self.context.get('status')
        inventory_obj.save()
        return inventory_obj
