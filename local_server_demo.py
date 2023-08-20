class Router:
    buffer = []
    def __init__(self):
        self.connect = []

    def link(self, server):
        self.connect.append(server)

    def unlink(self, server):
        self.connect.remove(server)

    def send_data(self):
        if len(self.buffer) > 0:
            for a in self.buffer:
                for b in self.connect:
                    if a.ip == b.ip:
                        b.buffer.append(a)
            self.buffer = []




class Server:
    ip = 0
    def __new__(cls, *args, **kwargs):
        cls.ip += 1
        return super().__new__(cls)

    def __init__(self):
        self.ip = self.ip
        self.buffer = []

    def get_ip(self):
        return self.ip

    def get_data(self):
        ans_buffer = self.buffer.copy()
        self.buffer.clear()
        return ans_buffer


    def send_data(self, data):
        self.data = data
        Router.buffer.append(self.data)




class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip









router = Router()
sv1 = Server()
sv2 = Server()
sv3 = Server()

router.link(sv2)
router.link(sv1)
router.link(sv3)

router.unlink(sv3)

sv1.send_data(Data('testsdf', 2))
sv1.send_data(Data('tesdfst', 2))
sv1.send_data(Data('tessdft', 2))
sv2.send_data(Data('test2', 1))
sv2.send_data(Data('testsdf2', 1))
sv2.send_data(Data('testsdf2', 1))
sv2.send_data(Data('test3', 3))

router.send_data()

print(sv1.get_data())
print(sv2.get_data())
print(sv3.get_data())


print(sv1.buffer, sv2.buffer, router.buffer)
