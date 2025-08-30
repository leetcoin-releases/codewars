#
# Solution
#
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





#
# Sample Tests
#
@test.describe('Sample tests')
def sample_tests():
    class User(Model):
        first_name = CharField(max_length=30, default='Adam')
        last_name = CharField(max_length=50)
        email = EmailField()
        is_verified = BooleanField(default=False)
        date_joined = DateTimeField(auto_now=True)
        age = IntegerField(min_value=5, max_value=120, blank=True)
    
    @test.it('Model class has no field')
    def it_1():
        test.expect(not hasattr(User, 'first_name'))
    
    @test.it('Instance has default values')
    def it_2():
        user = User()
        test.assert_equals(user.first_name, 'Adam')
        test.assert_equals(user.last_name, None)
        test.assert_equals(user.is_verified, False)
    
    @test.it('Values can be changed')
    def it_3():
        user = User()
        user.email = 'adam@example.com'
        test.assert_equals(user.email, 'adam@example.com')
    
    @test.it('An instance can be created by passing arguments to it')
    def it_4():
        user = User(first_name='Liam', last_name='Smith', email='liam@example.com')
        test.assert_equals(user.first_name, 'Liam')
        test.assert_equals(user.last_name, 'Smith')
        test.assert_equals(user.email, 'liam@example.com')
    
    @test.it("Instance's fields can be validated")
    def it_5():
        user = User(first_name='Liam', last_name='Smith', email='liam@example.com')
        user.validate()
        user.age = 999
        test.expect_error('Age is out of range', user.validate, exception=ValidationError)
    
    @test.it("2 instances have different data")
    def it_6():
        user1 = User()
        user1.first_name = "John"
        user1.last_name = "Doe"
        
        user2 = User()
        user2.first_name = "Somebody"
        user2.last_name = "Else"
        
        test.assert_equals(user1.first_name, "John")
        test.assert_equals(user1.last_name, "Doe")
        
        user1.first_name = "John"
        user1.last_name = "Doe"
        
        test.assert_equals(user2.first_name, "Somebody")
        test.assert_equals(user2.last_name, "Else")