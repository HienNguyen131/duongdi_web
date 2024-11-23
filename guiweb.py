import streamlit as st
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Rectangle
from search import *


romania_map = UndirectedGraph(dict(
    BinhPhuoc=dict(TayNinh=111, BinhDuong=79, DongNai=165),
    BinhDuong=dict(DongNai=92, TayNinh=74),
    HCM=dict(TayNinh=92, BinhDuong=42, DongNai=91, VungTau=109, LongAn=60, TienGiang=66),
    VungTau=dict(DongNai=94),
    LongAn=dict(TienGiang=46, DongThap=46),
    TienGiang=dict(BenTre=25, DongThap=91),
    VinhLong=dict(BenTre=90, DongThap=50, TienGiang=71, TraVinh=65, HauGiang=60),
    TraVinh=dict(BenTre=46),
    AnGiang=dict(DongThap=99, KienGiang=104, CanTho=83),
    CanTho=dict(AnGiang=88, DongThap=68, VinhLong=76, HauGiang=72, KienGiang=83),
    SocTrang=dict(TraVinh=62, VinhLong=93, HauGiang=53, BacLieu=49),
    HauGiang=dict(KienGiang=82),
    CaMau=dict(KienGiang=106),
    BacLieu=dict(KienGiang=127, HauGiang=74, SocTrang=47, CaMau=68)
))


romania_map.locations = dict(
    HCM=(600, 300), BinhDuong=(550, 430), DongNai=(650, 350),
    VungTau=(730, 280), TayNinh=(500, 450),
    BinhPhuoc=(650, 550),
    LongAn=(500, 300),
    TienGiang=(500, 250),
    BenTre=(600, 180),
    DongThap=(400, 250),
    VinhLong=(460, 160),
    TraVinh=(550, 120),
    AnGiang=(300, 250),
    CanTho=(400, 160),
    HauGiang=(400, 110),
    SocTrang=(460, 80),
    KienGiang=(260, 80),
    BacLieu=(330, 20),
    CaMau=(300, -20)
)


city_name = dict(
    HCM=(10, -20), BinhDuong=(0, -10), DongNai=(15, -15),
    VungTau=(15, 15), TayNinh=(-15, -15),
    BinhPhuoc=(10, 20),
    LongAn=(0, -25),
    TienGiang=(15, 5),
    BenTre=(15, -15),
    DongThap=(-5, -15),
    VinhLong=(15, -25),
    TraVinh=(15, 5),
    AnGiang=(-20, -35),
    CanTho=(-15, -10),
    HauGiang=(-5, 25),
    SocTrang=(15, 5),
    KienGiang=(-50, 15),
    BacLieu=(20, 15),
    CaMau=(0, 15)
)


map_locations = romania_map.locations
graph_dict = romania_map.graph_dict
all_x = [coord[0] for coord in map_locations.values()]
all_y = [coord[1] for coord in map_locations.values()]
padding = 70
xmin, xmax = min(all_x) - padding, max(all_x) + padding
ymin, ymax = min(all_y) - padding, max(all_y) + padding


def draw_map(ax):
    for key in graph_dict:
        city = graph_dict[key]
        x0, y0 = map_locations[key]
        rectangle = Rectangle((x0 - 4, y0 - 4), 8, 8, edgecolor='black', color='r', linewidth=1.0)
        ax.add_patch(rectangle)
        dx, dy = city_name[key]
        ax.text(x0 + dx, y0 - dy, key, fontsize=6)

        for neighbor in city:
            x1, y1 = map_locations[neighbor]
            ax.plot([x0, x1], [y0, y1], 'blue', linewidth=1)


st.title("A* Search Path Visualization")

lst_city = list(city_name.keys())
start_city = st.selectbox('Chọn thành phố bắt đầu:', lst_city, key='start_city')
dest_city = st.selectbox('Chọn thành phố đích:', lst_city, key='dest_city')

if st.button('Tìm đường'):

    problem = GraphProblem(start_city, dest_city, romania_map)
    solution = astar_search(problem)
    lst_path = solution.path()
    

    path_locations = {data.state: map_locations[data.state] for data in lst_path}
    lst_path_location_x = [path_locations[city.state][0] for city in lst_path]
    lst_path_location_y = [path_locations[city.state][1] for city in lst_path]

 
    placeholder = st.empty()

    for i in range(len(lst_path_location_x)):
 
        fig, ax = plt.subplots()
        ax.axis([xmin, xmax, ymin, ymax])
        draw_map(ax)

      
        ax.plot(lst_path_location_x[:i+1], lst_path_location_y[:i+1], 'green', linewidth=2)

   
        if i < len(lst_path_location_x) - 1:
            ax.annotate('',
                        xy=(lst_path_location_x[i+1], lst_path_location_y[i+1]),
                        xytext=(lst_path_location_x[i], lst_path_location_y[i]),
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))

        placeholder.pyplot(fig)
        time.sleep(3.0) 
