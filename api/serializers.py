from rest_framework import serializers, validators

from api.models import ApiUser, Storage, Product, Order


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    email = serializers.EmailField(validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    # ожидается только от клиента. Клиенту не передается
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)
    type_user = serializers.CharField(max_length=128)

    def update(self, instance, validated_data):
        if email := validated_data.get('email'):
            instance.email = email
            instance.save(update_fields=['email'])

        if password := validated_data.get('password'):
            instance.set_password(validated_data["password"])
            instance.save(update_fields=['password'])

        return instance

    def create(self, validated_data):
        user = ApiUser.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            type_user=validated_data['type_user']
        )

        user.set_password(validated_data["password"])
        user.save(update_fields=['password'])

        return user

    # type_user in ['provider', 'consumer']
    def validate_type_user(self, type_user):
        if type_user not in ['provider', 'consumer']:
            raise serializers.ValidationError('Type user must be provider or consumer')
        return type_user


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = "__all__"
        # extra_kwargs = {'id': {'read_only': True}}


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        # extra_kwargs = {'id': {'read_only': True}}


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'date': {'read_only': True},
                        'type_order': {'read_only': True}}
