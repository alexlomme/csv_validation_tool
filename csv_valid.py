import csv

# weight
# geom 
# was_one_way
# osm_way_from
# osm_way_to
# osm_way_from_source_node
# osm_way_from_target_node
# osm_way_to_source_node
# osm_way_to_target_node


def parse_geom(geom):
    cleaned_string = geom.replace("LINESTRING(", "").replace(")", "")
    
    # Split the string into individual coordinate pairs using semicolon as the delimiter
    coordinate_pairs = cleaned_string.split(";")
    
    # Convert the string pairs into tuples of floats
    tuple_list = []
    for pair in coordinate_pairs:
        lon, lat = map(float, pair.split())  # Split by space and convert to float
        tuple_list.append((round(lon, 8), round(lat, 8)))
    
    return tuple_list

def parse_edges(file_path):
    with open(file_path, 'r') as file:
        tuples = []
        csv_reader = csv.reader(file)
        headers = next(csv_reader)

        for row in csv_reader:
            weight = float(row[0])
            geom = tuple(parse_geom(row[1]))
            was_one_way = True if row[2] == "true" else False
            osm_way_from = int(row[3])
            osm_way_to = int(row[4])
            osm_way_from_source_node = int(row[5])
            osm_way_from_target_node = int(row[6])
            osm_way_to_source_node = int(row[7])
            osm_way_to_target_node = int(row[8])
            tuples.append((weight, (geom[0], geom[len(geom) - 1]), was_one_way, osm_way_from, osm_way_to, osm_way_from_source_node, 
                           osm_way_from_target_node, osm_way_to_source_node, osm_way_to_target_node))

    return tuples

def compare_files(file1, file2):
    edges1 = set(parse_edges(file1))
    edges2 = set(parse_edges(file2))

    only_in_file1 = edges1 - edges2
    only_in_file2 = edges2 - edges1

    i = 0
    j = 0

    e1 = []
    e2 = []

    if not only_in_file1 and not only_in_file2:
        print("The files are identical.")
    else:
        print("Differences found:")
        if only_in_file1:
            print("\nEdges only in file 1:")
            for edge in only_in_file1:
                i += 1
                e1.append(edge)
                # print(edge)
        if only_in_file2:
            print("\nEdges only in file 2:")
            for edge in only_in_file2:
                j += 1
                e2.append(edge)
                # print(edge)

    print(i, j)

    e1 = sorted(e1)
    e2 = sorted(e2)

    diffs = []

    maxdelta = 0

    prec = .00000001

    for i in range(len(e1)):
        pair1 = e1[i][1]
        pair2 = e2[i][1]

        lon1_d = pair1[0][0] - pair2[0][0]
        lon2_d = pair1[1][0] - pair2[1][0]

        lat1_d = pair1[0][1] - pair2[0][1]
        lat2_d = pair1[1][1] - pair2[1][1]

        if (abs(lon1_d) <= prec and abs(lon2_d) <= prec and abs(lat1_d) <= prec and abs(lat2_d) <= prec):
            continue

        if (abs(lon1_d) > maxdelta):
            maxdelta = abs(lon1_d)

        if (abs(lon2_d) > maxdelta):
            maxdelta = abs(lon2_d)

        if (abs(lat1_d) > maxdelta):
            maxdelta = abs(lat1_d)

        if (abs(lat2_d) > maxdelta):
            maxdelta = abs(lat2_d)            

        diffs.append(((lon1_d, lat1_d), (lon2_d, lat2_d)))

    # print(diffs)    
    print(maxdelta)
            

file1 = 'oberbayern_t_15.csv'
file2 = 'oberbayern_osm2ch_15.csv'
compare_files(file1, file2)
