from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
    ValidationError,
)
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSignupModelSerializer(ModelSerializer):
    """
    Serializer for user registration.

    Attributes:
    email (EmailField): Email field with uniqueness validation.
    password (CharField): Password field with write-only mode and password validation.
    password2 (CharField): Second password field for confirmation.
    model (Model): The User model.
    fields (tuple): The fields to include in the serialized data.
    """

    email = EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="The email you entered is already associated with another account. Please use a different email address.",
            )
        ],
    )
    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "name",
            "password",
            "password2",
        )

    def validate(self, attrs):
        """
        Validates the password fields for equality.

        Args:
        attrs (dict): The validated data.

        Raises:
        ValidationError: If the password fields don't match.

        Returns:
        dict: The validated data.
        """

        if attrs["password"] != attrs["password2"]:
            raise ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Creates a new user instance.

        Args:
        validated_data (dict): The validated data for user creation.

        Returns:
        User: The created user instance.
        """

        user = User.objects.create(
            email=validated_data["email"],
            name=validated_data.get(
                "name", ""
            ),  # Use an empty string as the default value as name is optional and allowed to be blank
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(Serializer):
    """
    Serializer for user login.

    Attributes:
    email (CharField): Required email field.
    password (CharField): Required write-only password field.
    """

    email = CharField(required=True)
    password = CharField(required=True, write_only=True)

    def validate(self, attrs):
        """
        Validates user credentials.

        Args:
        attrs (dict): The validated data.

        Raises:
        ValidationError: If credentials are invalid.

        Returns:
        dict: The validated data with the user object.
        """

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            raise ValidationError("Invalid credentials")

        attrs["user"] = user
        return attrs


class UserModelSerializer(ModelSerializer):
    """
    Serializer for User model data.

    Attributes:
    model (Model): The User model.
    fields (list): The fields to include in the serialized data.
    """

    class Meta:
        model = User
        fields = ["id", "email", "name"]
