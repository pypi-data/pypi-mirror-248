from collections import deque
from json import loads
from os import mkdir
from os.path import exists

from dearpygui import dearpygui as dpg
from numpy import trapz, concatenate, array

from leads.comm import *
from leads.utils import *
from leads_dashboard import *
from leads_vec.config import Config


def render():
    dpg.bind_item_font(dpg.add_text(tag="speed"), H2)
    dpg.bind_item_font(dpg.add_text(tag="displacement"), H2)
    dpg.add_simple_plot(label="Speed Trend", tag="speed_seq", height=300)


def integrate_speed2displacement(x: DataPersistence, y: DataPersistence) -> float:
    return 0 if len(x) < 2 else trapz(y.to_list() + y.get_chunk(),
                                      concatenate((array(a := x.to_list()) - a[0], array(x.get_chunk()) - a[0])) / 3600,
                                      dx=.001)


def remote(config: Config) -> int:
    if not exists(config.data_dir):
        mkdir(config.data_dir)
        print(f"Data dir \"{config.data_dir}\" created")

    class CustomCallback(Callback):
        speed_seq: deque = deque(maxlen=512)
        speed_record: DataPersistence = DataPersistence(config.data_dir + "/speed.csv", max_size=256)
        time_stamp_record: DataPersistence = DataPersistence(config.data_dir + "/time_stamp.csv", max_size=256)

        def on_initialize(self, service: Service) -> None:
            print(f"Comm server started on port {service.port()}")

        def on_fail(self, service: Service, error: Exception) -> None:
            print(error)

        def on_receive(self, service: Service, msg: bytes) -> None:
            data = loads(msg.decode())
            self.time_stamp_record.append(data["t"])
            front_wheel_speed = data["front_wheel_speed"]
            self.speed_seq.append(front_wheel_speed)
            self.speed_record.append(front_wheel_speed)
            dpg.set_value("speed", f"FWS: {int(front_wheel_speed)} KM / H")
            dpg.set_value("displacement",
                          f"{int(integrate_speed2displacement(self.time_stamp_record, self.speed_record))} M")
            dpg.set_value("speed_seq", list(self.speed_seq))

        def on_disconnect(self, service: Service) -> None:
            self.speed_record.close()

    start_comm_server(render, create_server(config.comm_port, CustomCallback()))
    return 0
