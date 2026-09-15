import heapq



def dijkstra(graph,start,destination):


    distance = {
        node : float('inf')
        for node in graph
    }

    distance[start] = 0

    previus_nodes = {
        node : None
        for node in graph
    }

    priority_queue = []

    heapq.heappush(
        priority_queue,
        (0,start)
    )

    while priority_queue:

        current_distance, current_node = heapq.heappop(

            priority_queue
        )
        if current_node == destination:
            break

        for nighbord , weight in graph[current_node]:

            new_distance = current_distance + weight

            if new_distance < distance[nighbord]:

                distance[nighbord] = new_distance

                previus_nodes[nighbord] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance,nighbord)
                )

    path = []

    current = destination

    while current is not None:

        path.append(current)

        current = previus_nodes[current]
    path.reverse()
    return path , distance[destination] 


