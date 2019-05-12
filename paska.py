import math

debug = False
def p(msg):
    if debug:
        print(msg)

#get new vector from next point
def calculate_new_vector(point_index, previous_index):
    return (2*points_x[point_index] - points_x[previous_index], 2*points_y[point_index] - points_y[previous_index])

#get distance of two points
def get_length(index_A, index_B):
    p("delku pocitam z techto bodu: ")
    p(str(points_x[index_A]) + str(points_y[index_A]))
    p(str(points_x[index_B]) + str(points_y[index_B]))
    return math.sqrt(pow(points_x[index_A]-points_x[index_B],2) + pow(points_y[index_A]-points_y[index_B],2))

#get index of minimum from list of angles
def get_min_angle_index(angles):
    min_angle = angles[0]
    min_angle_index = 0
    for i in range(0, len(angles)):
        if(angles[i] < min_angle):
            min_angle = angles[i]
            min_angle_index = i
    return min_angle_index

#calculate angle of two vectors
def calculate_angle(point_vector, new_vector):
    angle_cos = ((point_vector[0]*new_vector[0]) + (point_vector[1]*new_vector[1])) / (math.sqrt((math.pow(point_vector[0],2) + math.pow(point_vector[1],2))) * math.sqrt((math.pow(new_vector[0],2) + math.pow(new_vector[1],2))))
    angle_cos = round(angle_cos, 4)
    #p("uhel je")
    #p(math.acos(angle_cos)*180/math.pi)
    #p("y ceho delam anticosiinus?")
    #p(angle_cos)
    return math.acos(angle_cos)

#find index of point creating a vector which forms smallest angle
def get_next_point(point_index, point_vector, prev_index):
    angles = []
    for i in range(0, len(points_x)):
        if (i != point_index and not (points_x[point_index] == points_x[i] and points_y[point_index] == points_y[i]) and (i != prev_index)): #nedelam uhel sama se sebou a stejne velkym uhlem
            new_vector = (points_x[i]-points_x[point_index], points_y[i]-points_y[point_index])
            new_angle = calculate_angle(point_vector, new_vector)
            angles.append(new_angle)
        else:
            angles.append(math.pi * 4 + 1) #potrebuju aby list  mel stejnou delku jak list se souradnicema, aby indexy odpovidaly, proto si za sama sebe pridam random uhel
    min_angle_index = get_min_angle_index(angles)
    return min_angle_index, point_index

#get max coordinate and its index
def get_max_x():
    max = points_x[0]
    index_max = 0
    for i in range(0, len(points_x)):
        if (points_x[i]>max):
            max = points_x[i]
            index_max = i
    return max, index_max

#store object coordinates into a list
def get_obj_xy():
  object = list(map(int,input().split()))
  p(object)
  for i in range(1, object[0]*2,2):
      p("object x is")
      p(object[i])
      points_x.append(object[i]);
      points_y.append(object[i+1]);

num_objects = int(input())
points_x = []
points_y = []
length = 0
closed = False
prev_index = -1
for i in range(0, num_objects):
  get_obj_xy()
p("print listu souradnic x a y")
p(points_x)
p(points_y)
max_x, index_max_x = get_max_x()
p("index max x je> ")
p(index_max_x)
max_x_vector = (0,1)
next_point_index, prev_index = get_next_point(index_max_x, max_x_vector, prev_index)
length += get_length(index_max_x, next_point_index)
p("delka prvni je")
p(length)

#repeats until next point is the same as the first one
while(not closed):
    p("vector je")
    p(calculate_new_vector(next_point_index, prev_index))
    next_point_index, prev_index = get_next_point(next_point_index, calculate_new_vector(next_point_index, prev_index), prev_index)
    length = length + get_length(prev_index, next_point_index)
    p("pridano " + str(get_length(prev_index, next_point_index)))
    p("delka je")
    p(length)
    if(next_point_index == index_max_x):
        closed = True
print("{:.2f}".format(round(length,2)))
