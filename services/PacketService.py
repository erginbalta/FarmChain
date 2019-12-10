
class Packet:
    packetType=[
        "SRC","SRSL","TRN","PRW","CNS","WIN","ENT","ERSL"
    ]

    def packetRouter(self, packetHeader):
        packetHeader = str(packetHeader).upper()
        if packetHeader not in self.packetType:
            print("there is no packet type " +packetHeader)
        else:
            if packetHeader == self.packetType[0]:
                pass
            elif packetHeader == self.packetType[1]:
                pass
            elif packetHeader == self.packetType[2]:
                pass
            elif packetHeader == self.packetType[3]:
                pass
            elif packetHeader == self.packetType[4]:
                pass
            elif packetHeader == self.packetType[5]:
                pass
            elif packetHeader == self.packetType[6]:
                pass
            elif packetHeader == self.packetType[7]:
                pass
