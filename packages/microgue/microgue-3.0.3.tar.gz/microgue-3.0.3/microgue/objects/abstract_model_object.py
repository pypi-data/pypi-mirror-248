import uuid
from .attribute import Attribute
from ..models.abstract_model import *  # noqa
from .object import *  # noqa


class RequiredAttributes(Exception): pass  # noqa
class UniqueAttributes(Exception): pass  # noqa


class AbstractModelObject(Object):  # noqa
    """
    model: the instantiated model that AbstractModelObject will use to connect to the database
        two options:
        - instantiate an external model
        - define a class Model inside the object definition

    attributes: defines the attributes of the Object

    hidden_attributes: attributes to hide when calling Object.serialize() / Object.serialize(hide_attributes=True)

    required_attributes: attributes that must be included when creating a new object in the database

    unique_attributes: attributes that must be unique across all entries in the database

    default_attributes: defines the default values to use when creating a new object
    """
    # extension required
    model = None

    # extension optional
    class Model(AbstractModel): pass  # noqa
    attributes = []
    hidden_attributes = []
    required_attributes = []
    unique_attributes = []
    default_attributes = {}

    def __new__(cls, *args, **kwargs):
        cls._set_model()

        # get the pk from the Object definition
        try:
            pk = getattr(cls, cls.model.pk)
        except AttributeError:
            pk = None

        # check if the Object definition is using Attribute notation
        if isinstance(pk, Attribute):
            # for every attribute in the Object definition
            for attribute_name in dir(cls):
                # check if the attribute is an Attribute
                attribute_value = getattr(cls, attribute_name)
                if isinstance(attribute_value, Attribute):
                    # process the Attribute into the Object definition
                    cls.attributes.append(attribute_name)
                    if attribute_value.hidden:
                        cls.hidden_attributes.append(attribute_name)
                    if attribute_value.required:
                        cls.required_attributes.append(attribute_name)
                    if attribute_value.unique:
                        cls.unique_attributes.append(attribute_name)
                    if attribute_value.default:
                        cls.default_attributes[attribute_name] = attribute_value.default_value

                    # remove the Attribute from the Object definition after processing
                    setattr(cls, attribute_name, None)

        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set default values
        for key, value in self.default_attributes.items():
            if getattr(self, key) is None:
                self.__setattr__(key, value)

    @property
    def _pk(self):
        return self.model.pk

    @property
    def _pk_value(self):
        return self.__dict__.get(self._pk)

    @property
    def _sk(self):
        return self.model.sk

    @property
    def _sk_value(self):
        return self.__dict__.get(self._sk)

    @classmethod
    def _set_model(cls):
        # use the default model if one is not provided
        if cls.model is None:
            cls.model = cls.Model()

    @classmethod
    def get(cls, pk_value, sk_value=None):
        cls._set_model()

        return cls(
            cls.model.get(pk_value, sk_value),
            raise_errors=False
        )

    @classmethod
    def get_by_unique_attribute(cls, attribute, value):
        cls._set_model()

        unique_key = f"{attribute.upper()}#{value}"
        reference = cls.model.get(unique_key, "#UNIQUE")

        model_object = cls()
        model_object.deserialize(
            attributes=cls.model.get(reference.get("reference_pk"), reference.get("reference_sk")),
            raise_errors=False
        )

        return model_object

    def insert(self):
        # enforce required attributes
        missing_required_attributes = self._get_missing_required_attributes()
        if missing_required_attributes:
            raise RequiredAttributes("missing the following required attributes: " + ", ".join(missing_required_attributes))

        # auto generate pk if needed
        if self.model.auto_generate_pk and not self._pk_value:
            self.__setattr__(self._pk, str(uuid.uuid4()))

        # auto generate sk if needed
        if self.model.auto_generate_sk and self._sk and not self._sk_value:
            self.__setattr__(self._sk, str(uuid.uuid4()))

        # create a list of unique attributes to try and insert into the database
        insert_unique_attributes = []
        for attribute in self.unique_attributes:
            # check if the unique attribute has a value
            if self.__dict__.get(attribute):
                insert_unique_attributes.append(attribute)

        # attempt to insert all unique attributes
        self._insert_unique_attributes(insert_unique_attributes)

        try:
            # insert the object
            self.deserialize(
                attributes=self.model.insert(self.serialize(hide_attributes=False)),
                raise_errors=False
            )
        except Exception as e:
            # undo all unique inserts if the object insert fails
            self._undo_insert_unique_attributes(insert_unique_attributes)
            raise e

    def update(self):
        # only pull the previous state of the object if necessary for checking uniqueness
        previous_state = None
        insert_unique_attributes = []

        # create a list of unique attributes to try and insert into the database
        for attribute in self.unique_attributes:
            # check if the unique attribute has a value
            attribute_value = self.__dict__.get(attribute)

            # pull the previous state of the object for checking if the unique attribute has changed
            if attribute_value and previous_state is None:
                previous_state = self.model.get(self._pk_value, self._sk_value)

            # only insert the new unique attribute if the value is different than in the previous state
            if attribute_value and attribute_value != previous_state.get(attribute):
                insert_unique_attributes.append(attribute)

        # attempt to insert all unique attributes
        self._insert_unique_attributes(insert_unique_attributes)

        try:
            # update the object
            self.deserialize(
                attributes=self.model.update(self.serialize(hide_attributes=False)),
                raise_errors=False
            )
        except Exception as e:
            # undo all unique inserts if the object update fails
            self._undo_insert_unique_attributes(insert_unique_attributes)
            raise e
        else:
            # remove previous unique attribute values
            if previous_state:
                for old_attribute in insert_unique_attributes:
                    try:
                        self.model.delete(f"{old_attribute.upper()}#{previous_state.get(old_attribute)}", "#UNIQUE")
                    except:  # noqa
                        pass

    def save(self):
        # check if the record exists
        if self._pk_value:
            try:
                record_exists = bool(self.model.get(self._pk_value, self._sk_value))
            except:  # noqa
                record_exists = False

        # call update or insert accordingly
        if self._pk_value and record_exists:
            self.update()
        else:
            self.insert()

    def delete(self):
        # check if the object has unique attributes
        if self.unique_attributes:
            try:
                # undo all unique attributes before deleting the object
                self._undo_insert_unique_attributes(self.unique_attributes)
            except:  # noqa
                pass

        # delete the object
        return self.model.delete(self._pk_value, self._sk_value)

    def _get_missing_required_attributes(self):
        missing_required_attributes = []
        for required_attribute in self.required_attributes:
            if getattr(self, required_attribute) is None:
                missing_required_attributes.append(required_attribute)
        return missing_required_attributes

    def _insert_unique_attributes(self, unique_attributes):
        successes = []
        failures = []

        # attempt to insert each unique attribute as a special entry in the database ex EMAIL#test@test.com / #UNIQUE
        for attribute in unique_attributes:
            attribute_value = self.__dict__.get(attribute)

            unique_entry = self._build_unique_entry(
                attribute,
                attribute_value,
                self._pk_value,
                self._sk_value
            )

            try:
                # attempt to insert
                self.model.insert(unique_entry)
            except ItemAlreadyExists:  # noqa
                # track failures
                failures.append(attribute)
            else:
                # track successes
                successes.append(attribute)

        # undo all success if any failures occurred
        if failures:
            self._undo_insert_unique_attributes(successes)
            raise UniqueAttributes("the following unique attributes already exists: " + ", ".join(failures))

    def _build_unique_entry(self, unique_attribute, attribute_value, reference_pk, reference_sk=None):
        unique_entry = {}
        unique_entry[self._pk] = f"{unique_attribute.upper()}#{attribute_value}"
        unique_entry["reference_pk"] = reference_pk
        if reference_sk:
            unique_entry[self._sk] = "#UNIQUE"
            unique_entry["reference_sk"] = reference_sk
        return unique_entry

    def _undo_insert_unique_attributes(self, unique_attributes):
        for attribute in unique_attributes:
            try:
                delete_pk = f"{attribute.upper()}#{self.__dict__.get(attribute)}"
                delete_sk = "#UNIQUE"
                self.model.delete(delete_pk, delete_sk)
            except:  # noqa
                pass
