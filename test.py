types = {}
class A:
    def other_thing(name_type):
        
        def decorator(func):
            
            def wrapper(self, *args, **kwargs):
                print(1)
                res = func(self, *args, **kwargs)
                print(2)
            if lst := types.get(name_type):
                lst.append(wrapper)
            else:
                types[name_type] = [wrapper]
            return wrapper
        return decorator
    @other_thing(0)
    def funct(self):
        print(-1)

    @other_thing(1)
    def funct2(self):
        print(-1)
    @other_thing(1)
    def funct3(self):
        print(-2)

a = A()
for i in types[1]:
    i(a)

