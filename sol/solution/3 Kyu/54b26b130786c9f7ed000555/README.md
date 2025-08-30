# [**Metaclasses - Simple Django Models**](https://www.codewars.com/kata/54b26b130786c9f7ed000555)

## **Description:**
Django is a famous back-end framework written in Python. It has a vast list of features including the creation of database tables through "models". You can see an example of such model below:

```py
class Person(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
```

Apart from creating a table it can perform validation, generate HTML forms, and so on. This is possible thanks to metaclasses. Normally there are better solutions than using metaclasses, but they can be of great help in creating powerful framework interfaces. This goal of this kata is to learn and understand how such frameworks works.

Your task is to implement a class `Model` and classes for its fields to support functionality like in the following example:

```py
class User(Model):
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=50)
    email = EmailField()
    is_verified = BooleanField(default=False)
    date_joined = DateTimeField(auto_now=True)
    age = IntegerField(min_value=5, max_value=120, blank=True)


user1 = User(first_name='Liam', last_name='Smith', email='liam@example.com')
user1.validate()

print(user1.date_joined)  # prints date and time when the instance was created
print(user1.is_verified)  # prints False (default value)

user1.age = 256
user1.validate()  # raises ValidationError - age is out of range

user2 = User()
user2.validate()  # raises ValidationError - first three fields are missing and mandatory
```

The classes which inherit from `Model` should:
- support creation of fields using class-attribute syntax
- have a `validate` method which checks whether all fields are valid

The field types you should implement are described below. Each of them also has parameters `blank` (default `False`), which determines whether `None` is allowed as a value, and `default` (default `None`) which determines the value to be used if nothing was provided at instantiation time of the Model.
- `CharField` - a string with `min_length` (default `0`) and `max_length` (default `None`) parameters, both inclusive if defined
- `IntegerField` - an integer with `min_value` (default `None`) and `max_value` (default `None`) parameters, both inclusive if defined
- `BooleanField` - a boolean
- `DateTimeField` - a datetime with an extra parameter `auto_now` (default `False`). If `auto_now` is `True` and no default value has been provided, the current datetime should be used automatically at Model instantion time.
- `EmailField` - a string in the format of `address@subdomain.domain` where `address`, `subdomain`, and domain are sequences of alphabetical characters with `min_length` (default `0`) and `max_length` (default `None`) parameters
Each field type should have its own `validate` method which checks whether the provided value has the correct type and satisfies the length/value constraints.

## **Solutions:**

#### **Python**
```py
from datetime import datetime
import r
class ValidationError(Exception):
    pass
class CharField:
    def __init__(self, min_length=0, max_length=None, blank=False, default=None):
        self.min_length = min_length
        self.max_length = max_length
        self.blank = blank
        self.default = default
    def validate(self, value, name):
        if value is None:
            if self.blank:
                return
            raise ValidationError(f"{name.capitalize()} cannot be blank")
        if not isinstance(value, str):
            raise ValidationError(f"{name.capitalize()} must be a string")
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f"{name.capitalize()} is too short")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"{name.capitalize()} is too long")
class IntegerField:
    def __init__(self, min_value=None, max_value=None, blank=False, default=None):
        self.min_value = min_value
        self.max_value = max_value
        self.blank = blank
        self.default = default
    def validate(self, value, name):
        if value is None:
            if self.blank:
                return
            raise ValidationError(f"{name.capitalize()} cannot be blank")
        if not isinstance(value, int):
            raise ValidationError(f"{name.capitalize()} must be an integer")
        if (self.min_value is not None and value < self.min_value) or (self.max_value is not None and value > self.max_value):
            raise ValidationError(f"{name.capitalize()} is out of range")
class BooleanField:
    def __init__(self, blank=False, default=None):
        self.blank = blank
        self.default = default
    def validate(self, value, name):
        if value is None:
            if self.blank:
                return
            raise ValidationError(f"{name.capitalize()} cannot be blank")
        if not isinstance(value, bool):
            raise ValidationError(f"{name.capitalize()} must be a boolean")
class DateTimeField:
    def __init__(self, auto_now=False, blank=False, default=None):
        self.auto_now = auto_now
        self.blank = blank
        self.default = default
    def validate(self, value, name):
        if value is None:
            if self.blank:
                return
            raise ValidationError(f"{name.capitalize()} cannot be blank")
        if not isinstance(value, datetime):
            raise ValidationError(f"{name.capitalize()} must be a datetime")
class EmailField:
    def __init__(self, min_length=0, max_length=None, blank=False, default=None):
        self.min_length = min_length
        self.max_length = max_length
        self.blank = blank
        self.default = default
    def validate(self, value, name):
        if value is None:
            if self.blank:
                return
            raise ValidationError(f"{name.capitalize()} cannot be blank")
        if not isinstance(value, str):
            raise ValidationError(f"{name.capitalize()} must be a string")
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f"{name.capitalize()} is too short")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"{name.capitalize()} is too long")
        if not re.match(r'^[a-zA-Z]+@[a-zA-Z]+\.[a-zA-Z]+$', value):
            raise ValidationError(f"Invalid email format for {name.capitalize()}")
class ModelBase(type):
    def __new__(mcls, name, bases, attrs):
        if name == 'Model':
            return super().__new__(mcls, name, bases, attrs)
        fields = {}
        for attr_name, value in list(attrs.items()):
            if isinstance(value, (CharField, IntegerField, BooleanField, DateTimeField, EmailField)):
                fields[attr_name] = value
                del attrs[attr_name]
        attrs['_fields'] = fields
        return super().__new__(mcls, name, bases, attrs)
class Model(metaclass=ModelBase):
    def __init__(self, **kwargs):
        for name, field in self._fields.items():
            if name in kwargs:
                setattr(self, name, kwargs.pop(name))
            elif field.default is not None:
                setattr(self, name, field.default)
            elif isinstance(field, DateTimeField) and field.auto_now:
                setattr(self, name, datetime.now())
            else:
                setattr(self, name, None)
        if kwargs:
            raise TypeError(f"Unknown field(s): {', '.join(kwargs)}")
    def validate(self):
        for name, field in self._fields.items():
            value = getattr(self, name)
            field.validate(value, name)
```