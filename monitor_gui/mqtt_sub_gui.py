# run by cpython3
import paho.mqtt.client as mqtt
import queue
import json
import time
from dearpygui.core import *
from dearpygui.simple import *

q = queue.Queue(maxsize=0)


def _on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))


def _on_message(client, userdata, msg):
    datastr = msg.payload.decode()
    #  print(msg.topic + " " + datastr)
    data = json.loads(datastr)
    q.put(data)


client = mqtt.Client()
client.on_connect = _on_connect
client.on_message = _on_message

client.connect('127.0.0.1')
client.subscribe('measured', qos=0)
client.loop_start()
starttime = time.time()


def _render(sender, data):
    try:
        tdata = q.get_nowait()
    except queue.Empty:
        return

    tcount_data = get_data('tcount')
    temp_data = get_data('temps')
    humi_data = get_data('humis')
    co2eq_data = get_data('co2eqs')
    tvoc_data = get_data('tvocs')

    if len(temp_data) > 100:
        tcount_data[:] = tcount_data[50:] 
        temp_data[:] = temp_data[50:]
        humi_data[:] = humi_data[50:]
        co2eq_data[:] = co2eq_data[50:]
        tvoc_data[:] = tvoc_data[50:]

    t = time.time() - starttime
    tcount_data.append(t)
    temp_data.append(tdata['temp'])
    humi_data.append(tdata['humi'])
    co2eq_data.append(tdata['co2'])
    tvoc_data.append(tdata['tvoc'])
    # print(temp_data,humi_data,co2eq_data,tvoc_data)
    log_info(tdata)
    clear_plot('plot_temp')
    clear_plot('plot_humi')
    clear_plot('plot_co2eq')
    clear_plot('plot_tvoc')

    add_line_series('plot_temp', 'temp', tcount_data,temp_data, weight=2)
    add_line_series('plot_humi', 'humi', tcount_data,humi_data, weight=2)
    add_line_series('plot_co2eq', 'co2eq',tcount_data,co2eq_data, weight=2)
    add_line_series('plot_tvoc', 'tvoc', tcount_data,tvoc_data, weight=2)


show_logger()
with window('realtime plot'):
    set_main_window_size(700, 900)
    set_main_window_title('Realtime Monitor')
    add_plot('plot_temp', height=180)
    add_spacing()
    add_separator()
    add_spacing()
    add_plot('plot_humi', height=180)
    add_spacing()
    add_separator()
    add_spacing()
    add_plot('plot_co2eq', height=180)
    add_spacing()
    add_separator()
    add_spacing()
    add_plot('plot_tvoc', height=180)
    set_plot_ylimits('plot_temp', 0, 50)
    set_plot_ylimits('plot_humi', 20, 70)
    set_plot_ylimits('plot_co2eq', 350, 800)
    set_plot_ylimits('plot_tvoc', -20, 200)

    add_data('tcount', [])
    add_data('temps', [])
    add_data('humis', [])
    add_data('co2eqs', [])
    add_data('tvocs', [])
    set_render_callback(_render)

start_dearpygui()