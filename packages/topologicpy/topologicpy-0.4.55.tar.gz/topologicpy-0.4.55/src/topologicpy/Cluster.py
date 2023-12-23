import topologicpy
import topologic
class Cluster(topologic.Cluster):
    @staticmethod
    def ByFormula(formula, xRange=None, yRange=None, xString="X", yString="Y"):
        """
        Creates a cluster of vertices by vvaluating the input formula for a range of x and, optionally, a range of y values.

        Parameters
        ----------
        formula : str
            A string representing the formula to be evaluated.
            For 2D formulas, use 'X' for the independent variable. For 3D formulas, use 'X' and 'Y' for the independent variables.
            You can use standard math functions like 'sin', 'cos', 'tan', 'sqrt', etc.
            For example, 'X**2 + 2*X - sqrt(X)' or 'cos(abs(X)+abs(Y))'
            xRange : tuple , optional
                A tuple (start, end, step) representing the range of X values
                for which the formula should be evaluated.
                For example, to evaluate for X values from -5 to 5 with a step of 0.1: (-5, 5, 0.1)
                If the xRange is set to None or not specified:
                    The method assumes that the formula uses the yString (e.g. 'Y' as in 'Y**2 + 2*Y - sqrt(Y)')
                    The method will attempt to use the YRange instead for the independent variable.
            yRange : tuple , optional
                A tuple (start, end, step) representing the range of Y values
                for which the formula should be evaluated.
                            For example, to evaluate for x values from -5 to 5 with a step of 0.1:
                            (-5, 5, 0.1)

        Returns:
            topologic.Cluster
                The created cluster of vertices.
        """
        from topologicpy.Vertex import Vertex
        import math
        if xRange == None and yRange == None:
            print("Wire.ByFormula - Error: Both ranges cannot be None at the same time. Returning None.")
            return None
        if xString.islower():
            print("Wire.ByFormula - Error: the input xString cannot lowercase. Please consider using uppercase (e.g. X). Returning None.")
            return None
        if yString == 'y':
            print("Wire.ByFormula - Error: the input yString cannot be lowercase. Please consider using uppercase (e.g. Y). Returning None.")
            return None
        
        x_values = []
        y_values = []
        if not xRange == None:
            x_start, x_end, x_step = xRange
            x = x_start
            while x < x_end:
                x_values.append(x)
                x = x + x_step
            x_values.append(x_end)
        
        if not yRange == None:
            y_start, y_end, y_step = yRange
            y = y_start
            while y < y_end:
                y_values.append(y)
                y = y + y_step
            y_values.append(y_end)

        # Evaluate the formula for each x and y value
        x_return = []
        y_return = []
        z_return = []
        if len(x_values) > 0 and len(y_values) > 0: # Both X and Y exist, compute Z.
            for x in x_values:
                for y in y_values:
                    x_return.append(x)
                    y_return.append(y)
                    formula1 = formula.replace(xString, str(x)).replace(yString, str(y)).replace('sqrt', 'math.sqrt').replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan').replace('radians', 'math.radians').replace('pi', 'math.pi')
                    z_return.append(eval(formula1))
        elif len(x_values) == 0 and len(y_values) > 0: # Only Y exists, compute X, Z is always 0.
            for y in y_values:
                y_return.append(y)
                formula1 = formula.replace(xString, str(y)).replace('sqrt', 'math.sqrt').replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan').replace('radians', 'math.radians').replace('pi', 'math.pi')
                x_return.append(eval(formula1))
                z_return.append(0)
        else: # Only X exists, compute Y, Z is always 0.
            for x in x_values:
                x_return.append(x)
                formula1 = formula.replace(xString, str(x)).replace('sqrt', 'math.sqrt').replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan').replace('radians', 'math.radians').replace('pi', 'math.pi')
                y_return.append(eval(formula1))
                z_return.append(0)
        vertices = []
        for i in range(len(x_return)):
            vertices.append(Vertex.ByCoordinates(x_return[i], y_return[i], z_return[i]))
        return Cluster.ByTopologies(vertices)
    
    @staticmethod
    def ByTopologies(*args) -> topologic.Cluster:
        """
        Creates a topologic Cluster from the input list of topologies. The input can be individual topologies each as an input argument or a list of topologies stored in one input argument.

        Parameters
        ----------
        topologies : list
            The list of topologies.

        Returns
        -------
        topologic.Cluster
            The created topologic Cluster.

        """
        from topologicpy.Helper import Helper
        #assert isinstance(topologies, list), "Cluster.ByTopologies - Error: Input is not a list"
        if len(args) == 0:
            print("Cluster.ByTopologies - Error: The input topologies parameter is an empty list. Returning None.")
            return None
        if len(args) == 1:
            topologies = args[0]
            if isinstance(topologies, list):
                if len(topologies) == 0:
                    print("Cluster.ByTopologies - Error: The input topologies parameter is an empty list. Returning None.")
                    return None
                else:
                    topologyList = [x for x in topologies if isinstance(x, topologic.Topology)]
                    if len(topologies) == 0:
                        print("Cluster.ByTopologies - Error: The input topologies parameter does not contain any valid topologies. Returning None.")
                        return None
            else:
                print("Cluster.ByTopologies - Warning: The input topologies parameter contains only one topology. Returning the same topology.")
                return topologies
        else:
            topologyList = Helper.Flatten(list(args))
            topologyList = [x for x in topologyList if isinstance(x, topologic.Topology)]
        if len(topologyList) == 0:
            print("Cluster.ByTopologies - Error: The input parameters do not contain any valid topologies. Returning None.")
            return None
        return topologic.Cluster.ByTopologies(topologyList, False)

    @staticmethod
    def CellComplexes(cluster: topologic.Cluster) -> list:
        """
        Returns the cellComplexes of the input cluster.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.

        Returns
        -------
        list
            The list of cellComplexes.

        """
        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.CellComplexes - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        cellComplexes = []
        _ = cluster.CellComplexes(None, cellComplexes)
        return cellComplexes

    @staticmethod
    def Cells(cluster: topologic.Cluster) -> list:
        """
        Returns the cells of the input cluster.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.

        Returns
        -------
        list
            The list of cells.

        """
        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.Cells - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        cells = []
        _ = cluster.Cells(None, cells)
        return cells

    @staticmethod
    def Edges(cluster: topologic.Cluster) -> list:
        """
        Returns the edges of the input cluster.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.

        Returns
        -------
        list
            The list of edges.

        """ 
        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.Edges - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        edges = []
        _ = cluster.Edges(None, edges)
        return edges

    @staticmethod
    def Faces(cluster: topologic.Cluster) -> list:
        """
        Returns the faces of the input cluster.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.

        Returns
        -------
        list
            The list of faces.

        """
        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.Faces - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        faces = []
        _ = cluster.Faces(None, faces)
        return faces

    @staticmethod
    def FreeCells(cluster: topologic.Cluster, tolerance: float = 0.0001) -> list:
        """
        Returns the free cells of the input cluster that are not part of a higher topology.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.
        tolerance : float , optional
            The desired tolerance. The default is 0.0001.

        Returns
        -------
        list
            The list of free cells.

        """
        from topologicpy.CellComplex import CellComplex
        from topologicpy.Topology import Topology

        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.FreeCells - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        allCells = []
        _ = cluster.Cells(None, allCells)
        allCellsCluster = Cluster.ByTopologies(allCells)
        freeCells = []
        cellComplexes = []
        _ = cluster.CellComplexes(None, cellComplexes)
        cellComplexesCells = []
        for cellComplex in cellComplexes:
            tempCells = CellComplex.Cells(cellComplex)
            cellComplexesCells += tempCells
        if len(cellComplexesCells) == 0:
            return allCells
        cellComplexesCluster = Cluster.ByTopologies(cellComplexesCells)
        resultingCluster = Topology.Boolean(allCellsCluster, cellComplexesCluster, operation="difference", tolerance=tolerance)
        if resultingCluster == None:
            return []
        if isinstance(resultingCluster, topologic.Cell):
            return [resultingCluster]
        result = Topology.SubTopologies(resultingCluster, subTopologyType="cell")
        if result == None:
            return [] #Make sure you return an empty list instead of None
        return result
    
    @staticmethod
    def FreeShells(cluster: topologic.Cluster, tolerance: float = 0.0001) -> list:
        """
        Returns the free shells of the input cluster that are not part of a higher topology.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.
        tolerance : float, optional
            The desired tolerance. The default is 0.0001.

        Returns
        -------
        list
            The list of free shells.

        """
        from topologicpy.Cell import Cell
        from topologicpy.Topology import Topology

        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.FreeShells - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        allShells = []
        _ = cluster.Shells(None, allShells)
        if len(allShells) < 1:
            return []
        allShellsCluster = Cluster.ByTopologies(allShells)
        cells = []
        _ = cluster.Cells(None, cells)
        cellsShells = []
        for cell in cells:
            tempShells = Cell.Shells(cell)
            cellsShells += tempShells
        if len(cellsShells) == 0:
            return allShells
        cellsCluster = Cluster.ByTopologies(cellsShells)
        resultingCluster = Topology.Boolean(allShellsCluster, cellsCluster, operation="difference", tolerance=tolerance)
        if resultingCluster == None:
            return []
        if isinstance(resultingCluster, topologic.Shell):
            return [resultingCluster]
        result = Topology.SubTopologies(resultingCluster, subTopologyType="shell")
        if result == None:
            return [] #Make sure you return an empty list instead of None
        return result
    
    @staticmethod
    def FreeFaces(cluster: topologic.Cluster, tolerance: float = 0.0001) -> list:
        """
        Returns the free faces of the input cluster that are not part of a higher topology.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.
        tolerance : float , optional
            The desired tolerance. The default is 0.0001.

        Returns
        -------
        list
            The list of free faces.

        """
        from topologicpy.Shell import Shell
        from topologicpy.Topology import Topology

        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.FreeFaces - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        allFaces = []
        _ = cluster.Faces(None, allFaces)
        allFacesCluster = Cluster.ByTopologies(allFaces)
        shells = []
        _ = cluster.Shells(None, shells)
        shellFaces = []
        for shell in shells:
            tempFaces = Shell.Faces(shell)
            shellFaces += tempFaces
        if len(shellFaces) == 0:
            return allFaces
        shellCluster = Cluster.ByTopologies(shellFaces)
        resultingCluster = Topology.Boolean(allFacesCluster, shellCluster, operation="difference", tolerance=tolerance)
        if resultingCluster == None:
            return []
        if isinstance(resultingCluster, topologic.Face):
            return [resultingCluster]
        result = Topology.SubTopologies(resultingCluster, subTopologyType="face")
        if result == None:
            return [] #Make sure you return an empty list instead of None
        return result

    @staticmethod
    def FreeWires(cluster: topologic.Cluster, tolerance: float = 0.0001) -> list:
        """
        Returns the free wires of the input cluster that are not part of a higher topology.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.
        tolerance : float , optional
            The desired tolerance. The default is 0.0001.

        Returns
        -------
        list
            The list of free wires.

        """
        from topologicpy.Face import Face
        from topologicpy.Topology import Topology

        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.FreeWires - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        allWires = []
        _ = cluster.Wires(None, allWires)
        allWiresCluster = Cluster.ByTopologies(allWires)
        faces = []
        _ = cluster.Faces(None, faces)
        facesWires = []
        for face in faces:
            tempWires = Face.Wires(face)
            facesWires += tempWires
        if len(facesWires) == 0:
            return allWires
        facesCluster = Cluster.ByTopologies(facesWires)
        resultingCluster = Topology.Boolean(allWiresCluster, facesCluster, operation="difference", tolerance=tolerance)
        if resultingCluster == None:
            return []
        if isinstance(resultingCluster, topologic.Wire):
            return [resultingCluster]
        result = Topology.SubTopologies(resultingCluster, subTopologyType="wire")
        if not result:
            return [] #Make sure you return an empty list instead of None
        return result
    
    @staticmethod
    def FreeEdges(cluster: topologic.Cluster, tolerance: float = 0.0001) -> list:
        """
        Returns the free edges of the input cluster that are not part of a higher topology.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.
        tolerance : float, optional
            The desired tolerance. The default is 0.0001.

        Returns
        -------
        list
            The list of free edges.

        """
        from topologicpy.Wire import Wire
        from topologicpy.Topology import Topology

        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.FreeEdges - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        allEdges = []
        _ = cluster.Edges(None, allEdges)
        allEdgesCluster = Cluster.ByTopologies(allEdges)
        wires = []
        _ = cluster.Wires(None, wires)
        wireEdges = []
        for wire in wires:
            tempEdges = Wire.Edges(wire)
            wireEdges += tempEdges
        if len(wireEdges) == 0:
            return allEdges
        wireCluster = Cluster.ByTopologies(wireEdges)
        resultingCluster = Topology.Boolean(allEdgesCluster, wireCluster, operation="difference", tolerance=tolerance)
        if resultingCluster == None:
            return []
        if isinstance(resultingCluster, topologic.Edge):
            return [resultingCluster]
        result = Topology.SubTopologies(resultingCluster, subTopologyType="edge")
        if result == None:
            return [] #Make sure you return an empty list instead of None
        return result
    
    @staticmethod
    def FreeVertices(cluster: topologic.Cluster, tolerance: float = 0.0001) -> list:
        """
        Returns the free vertices of the input cluster that are not part of a higher topology.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.
        tolerance : float , optional
            The desired tolerance. The default is 0.0001.

        Returns
        -------
        list
            The list of free vertices.

        """
        from topologicpy.Edge import Edge
        from topologicpy.Topology import Topology

        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.FreeVertices - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        allVertices = []
        _ = cluster.Vertices(None, allVertices)
        allVerticesCluster = Cluster.ByTopologies(allVertices)
        edges = []
        _ = cluster.Edges(None, edges)
        edgesVertices = []
        for edge in edges:
            tempVertices = Edge.Vertices(edge)
            edgesVertices += tempVertices
        if len(edgesVertices) == 0:
            return allVertices
        edgesCluster = Cluster.ByTopologies(edgesVertices)
        resultingCluster = Topology.Boolean(allVerticesCluster, edgesCluster, operation="difference", tolerance=tolerance)
        if isinstance(resultingCluster, topologic.Vertex):
            return [resultingCluster]
        if resultingCluster == None:
            return []
        result = Topology.SubTopologies(resultingCluster, subTopologyType="vertex")
        if result == None:
            return [] #Make sure you return an empty list instead of None
        return result
    
    @staticmethod
    def HighestType(cluster: topologic.Cluster) -> int:
        """
        Returns the type of the highest dimension subtopology found in the input cluster.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.

        Returns
        -------
        int
            The type of the highest dimension subtopology found in the input cluster.

        """
        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.HighestType - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        cellComplexes = Cluster.CellComplexes(cluster)
        if len(cellComplexes) > 0:
            return topologic.CellComplex.Type()
        cells = Cluster.Cells(cluster)
        if len(cells) > 0:
            return topologic.Cell.Type()
        shells = Cluster.Shells(cluster)
        if len(shells) > 0:
            return topologic.Shell.Type()
        faces = Cluster.Faces(cluster)
        if len(faces) > 0:
            return topologic.Face.Type()
        wires = Cluster.Wires(cluster)
        if len(wires) > 0:
            return topologic.Wire.Type()
        edges = Cluster.Edges(cluster)
        if len(edges) > 0:
            return topologic.Edge.Type()
        vertices = Cluster.Vertices(cluster)
        if len(vertices) > 0:
            return topologic.Vertex.Type()
    
    @staticmethod
    def K_Means(topologies, selectors=None, keys=["x", "y", "z"], k=4, maxIterations=100, centroidKey="k_centroid"):
        """
        Clusters the input topologies using K-Means clustering. See https://en.wikipedia.org/wiki/K-means_clustering

        Parameters
        ----------
        topologies : list
            The input list of topologies. If this is not a list of topologic vertices then please provide a list of selectors
        selectors : list , optional
            If the list of topologies are not vertices then please provide a corresponding list of selectors (vertices) that represent the topologies for clustering. For example, these can be the centroids of the topologies.
            If set to None, the list of topologies is expected to be a list of vertices. The default is None.
        keys : list, optional
            The keys in the embedded dictionaries in the topologies. If specified, the values at these keys will be added to the dimensions to be clustered. The values must be numeric. If you wish the x, y, z location to be included,
            make sure the keys list includes "X", "Y", and/or "Z" (case insensitive). The default is ["x", "y", "z"]
        k : int , optional
            The desired number of clusters. The default is 4.
        maxIterations : int , optional
            The desired maximum number of iterations for the clustering algorithm
        centroidKey : str , optional
            The desired dictionary key under which to store the cluster's centroid (this is not to be confused with the actual geometric centroid of the cluster). The default is "k_centroid"

        Returns
        -------
        list
            The created list of clusters.

        """
        from topologicpy.Helper import Helper
        from topologicpy.Vertex import Vertex
        from topologicpy.Dictionary import Dictionary
        from topologicpy.Topology import Topology


        def k_means(data, vertices, k=4, maxIterations=100):
            import random
            def euclidean_distance(p, q):
                return sum((pi - qi) ** 2 for pi, qi in zip(p, q)) ** 0.5

            # Initialize k centroids randomly
            centroids = random.sample(data, k)

            for _ in range(maxIterations):
                # Assign each data point to the nearest centroid
                clusters = [[] for _ in range(k)]
                clusters_v = [[] for _ in range(k)]
                for i, point in enumerate(data):
                    distances = [euclidean_distance(point, centroid) for centroid in centroids]
                    nearest_centroid_index = distances.index(min(distances))
                    clusters[nearest_centroid_index].append(point)
                    clusters_v[nearest_centroid_index].append(vertices[i])

                # Compute the new centroids as the mean of the points in each cluster
                new_centroids = []
                for cluster in clusters:
                    if not cluster:
                        # If a cluster is empty, keep the previous centroid
                        new_centroids.append(centroids[clusters.index(cluster)])
                    else:
                        new_centroids.append([sum(dim) / len(cluster) for dim in zip(*cluster)])

                # Check if the centroids have converged
                if new_centroids == centroids:
                    break

                centroids = new_centroids

            return {'clusters': clusters, 'clusters_v': clusters_v, 'centroids': centroids}



        if not isinstance(topologies, list):
            print("Cluster.K_Means - Error: The input topologies parameter is not a valid list. Returning None.")
            return None
        topologies = [t for t in topologies if isinstance(t, topologic.Topology)]
        if len(topologies) < 1:
            print("Cluster.K_Means - Error: The input topologies parameter does not contain any valid topologies. Returning None.")
            return None
        if not isinstance(selectors, list):
            check_vertices = [v for v in topologies if not isinstance(v, topologic.Vertex)]
            if len(check_vertices) > 0:
                print("Cluster.K_Means - Error: The input selectors parameter is not a valid list and this is needed since the list of topologies contains objects of type other than a topologic.Vertex. Returning None.")
                return None
        selectors = [s for s in selectors if isinstance(s, topologic.Vertex)]
        if len(selectors) < 1:
            check_vertices = [v for v in topologies if not isinstance(v, topologic.Vertex)]
            if len(check_vertices) > 0:
                print("Cluster.K_Means - Error: The input selectors parameter does not contain any valid vertices and this is needed since the list of topologies contains objects of type other than a topologic.Vertex. Returning None.")
                return None
        if not len(selectors) == len(topologies):
            print("Cluster.K_Means - Error: The input topologies and selectors parameters do not have the same length. Returning None.")
            return None
        if not isinstance(keys, list):
            print("Cluster.K_Means - Error: The input keys parameter is not a valid list. Returning None.")
            return None
        if not isinstance(k , int):
            print("Cluster.K_Means - Error: The input k parameter is not a valid integer. Returning None.")
            return None
        if k < 1:
            print("Cluster.K_Means - Error: The input k parameter is less than one. Returning None.")
            return None
        if len(topologies) < k:
            print("Cluster.K_Means - Error: The input topologies parameter is less than the specified number of clusters. Returning None.")
            return None
        if len(topologies) == k:
            t_clusters = []
            for topology in topologies:
                t_cluster = Cluster.ByTopologies([topology])
                for key in keys:
                        if key.lower() == "x":
                            value = Vertex.X(t)
                        elif key.lower() == "y":
                            value = Vertex.Y(t)
                        elif key.lower() == "z":
                            value = Vertex.Z(t)
                        else:
                            value = Dictionary.ValueAtKey(d, key)
                        if value != None:
                            elements.append(value)
                d = Dictionary.ByKeysValues([centroidKey], [elements])
                t_cluster = Topology.SetDictionary(t_cluster, d)
                t_clusters.append(t_cluster)
            return t_clusters
        
        data = []
        if selectors == None:
            for t in topologies:
                elements = []
                if keys:
                    d = Topology.Dictionary(t)
                    for key in keys:
                        if key.lower() == "x":
                            value = Vertex.X(t)
                        elif key.lower() == "y":
                            value = Vertex.Y(t)
                        elif key.lower() == "z":
                            value = Vertex.Z(t)
                        else:
                            value = Dictionary.ValueAtKey(d, key)
                        if value != None:
                            elements.append(value)
                data.append(elements)
        else:
            for i, s in enumerate(selectors):
                elements = []
                if keys:
                    d = Topology.Dictionary(topologies[i])
                    for key in keys:
                        if key.lower() == "x":
                            value = Vertex.X(s)
                        elif key.lower() == "y":
                            value = Vertex.Y(s)
                        elif key.lower() == "z":
                            value = Vertex.Z(s)
                        else:
                            value = Dictionary.ValueAtKey(d, key)
                        if value != None:
                            elements.append(value)
                data.append(elements)
        if len(data) == 0:
            print("Cluster.K_Means - Error: Could not perform the operation. Returning None.")
            return None
        if selectors:
            dict = k_means(data, selectors, k=k, maxIterations=maxIterations)
        else:
            dict = k_means(data, topologies, k=k, maxIterations=maxIterations)
        clusters = dict['clusters_v']
        centroids = dict['centroids']
        t_clusters = []
        for i, cluster in enumerate(clusters):
            cluster_vertices = []
            for v in cluster:
                if selectors == None:
                    cluster_vertices.append(v)
                else:
                    index = selectors.index(v)
                    cluster_vertices.append(topologies[index])
            cluster = Cluster.ByTopologies(cluster_vertices)
            d = Dictionary.ByKeysValues([centroidKey], [centroids[i]])
            cluster = Topology.SetDictionary(cluster, d)
            t_clusters.append(cluster)
        return t_clusters

    @staticmethod
    def MysticRose(wire: topologic.Wire = None, origin: topologic.Vertex = None, radius: float = 0.5, sides: int = 16, perimeter: bool = True, direction: list = [0,0,1], placement:str = "center", tolerance: float = 0.0001) -> topologic.Cluster:
        """
        Creates a mystic rose.

        Parameters
        ----------
        wire : topologic.Wire , optional
            The input Wire. if set to None, a circle with the input parameters is created. Otherwise, the input parameters are ignored.
        origin : topologic.Vertex , optional
            The location of the origin of the circle. The default is None which results in the circle being placed at (0,0,0).
        radius : float , optional
            The radius of the mystic rose. The default is 1.
        sides : int , optional
            The number of sides of the mystic rose. The default is 16.
        perimeter : bool , optional
            If True, the perimeter edges are included in the output. The default is True.
        direction : list , optional
            The vector representing the up direction of the mystic rose. The default is [0,0,1].
        placement : str , optional
            The description of the placement of the origin of the mystic rose. This can be "center", or "lowerleft". It is case insensitive. The default is "center".
        tolerance : float , optional
            The desired tolerance. The default is 0.0001.

        Returns
        -------
        topologic.cluster
            The created mystic rose (cluster of edges).

        """
        import topologicpy
        from topologicpy.Vertex import Vertex
        from topologicpy.Edge import Edge
        from topologicpy.Wire import Wire
        from topologicpy.Cluster import Cluster
        from itertools import combinations

        if wire == None:
            wire = Wire.Circle(origin=origin, radius=radius, sides=sides, fromAngle=0, toAngle=360, close=True, direction=direction, placement=placement, tolerance=tolerance)
        if not Wire.IsClosed(wire):
            print("Cluster.MysticRose - Error: The input wire parameter is not a closed topologic wire. Returning None.")
            return None
        vertices = Wire.Vertices(wire)
        indices = list(range(len(vertices)))
        combs = [[comb[0],comb[1]] for comb in combinations(indices, 2) if not (abs(comb[0]-comb[1]) == 1) and not (abs(comb[0]-comb[1]) == len(indices)-1)]
        edges = []
        if perimeter:
            edges = Wire.Edges(wire)
        for comb in combs:
            edges.append(Edge.ByVertices([vertices[comb[0]], vertices[comb[1]]], tolerance=tolerance))
        return Cluster.ByTopologies(edges)
    
    @staticmethod
    def Shells(cluster: topologic.Cluster) -> list:
        """
        Returns the shells of the input cluster.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.

        Returns
        -------
        list
            The list of shells.

        """
        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.Shells - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        shells = []
        _ = cluster.Shells(None, shells)
        return shells

    @staticmethod
    def Simplify(cluster: topologic.Cluster):
        """
        Simplifies the input cluster if possible. For example, if the cluster contains only one cell, that cell is returned.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.

        Returns
        -------
        topologic.Topology or list
            The simplification of the cluster.

        """
        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.Simplify - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        resultingTopologies = []
        topCC = []
        _ = cluster.CellComplexes(None, topCC)
        topCells = []
        _ = cluster.Cells(None, topCells)
        topShells = []
        _ = cluster.Shells(None, topShells)
        topFaces = []
        _ = cluster.Faces(None, topFaces)
        topWires = []
        _ = cluster.Wires(None, topWires)
        topEdges = []
        _ = cluster.Edges(None, topEdges)
        topVertices = []
        _ = cluster.Vertices(None, topVertices)
        if len(topCC) == 1:
            cc = topCC[0]
            ccVertices = []
            _ = cc.Vertices(None, ccVertices)
            if len(topVertices) == len(ccVertices):
                resultingTopologies.append(cc)
        if len(topCC) == 0 and len(topCells) == 1:
            cell = topCells[0]
            ccVertices = []
            _ = cell.Vertices(None, ccVertices)
            if len(topVertices) == len(ccVertices):
                resultingTopologies.append(cell)
        if len(topCC) == 0 and len(topCells) == 0 and len(topShells) == 1:
            shell = topShells[0]
            ccVertices = []
            _ = shell.Vertices(None, ccVertices)
            if len(topVertices) == len(ccVertices):
                resultingTopologies.append(shell)
        if len(topCC) == 0 and len(topCells) == 0 and len(topShells) == 0 and len(topFaces) == 1:
            face = topFaces[0]
            ccVertices = []
            _ = face.Vertices(None, ccVertices)
            if len(topVertices) == len(ccVertices):
                resultingTopologies.append(face)
        if len(topCC) == 0 and len(topCells) == 0 and len(topShells) == 0 and len(topFaces) == 0 and len(topWires) == 1:
            wire = topWires[0]
            ccVertices = []
            _ = wire.Vertices(None, ccVertices)
            if len(topVertices) == len(ccVertices):
                resultingTopologies.append(wire)
        if len(topCC) == 0 and len(topCells) == 0 and len(topShells) == 0 and len(topFaces) == 0 and len(topWires) == 0 and len(topEdges) == 1:
            edge = topEdges[0]
            ccVertices = []
            _ = wire.Vertices(None, ccVertices)
            if len(topVertices) == len(ccVertices):
                resultingTopologies.append(edge)
        if len(topCC) == 0 and len(topCells) == 0 and len(topShells) == 0 and len(topFaces) == 0 and len(topWires) == 0 and len(topEdges) == 0 and len(topVertices) == 1:
            vertex = topVertices[0]
            resultingTopologies.append(vertex)
        if len(resultingTopologies) == 1:
            return resultingTopologies[0]
        return cluster

    @staticmethod
    def Vertices(cluster: topologic.Cluster) -> list:
        """
        Returns the vertices of the input cluster.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.

        Returns
        -------
        list
            The list of vertices.

        """
        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.Vertices - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        vertices = []
        _ = cluster.Vertices(None, vertices)
        return vertices

    @staticmethod
    def Wires(cluster: topologic.Cluster) -> list:
        """
        Returns the wires of the input cluster.

        Parameters
        ----------
        cluster : topologic.Cluster
            The input cluster.

        Returns
        -------
        list
            The list of wires.

        """
        if not isinstance(cluster, topologic.Cluster):
            print("Cluster.Wires - Error: The input cluster parameter is not a valid topologic cluster. Returning None.")
            return None
        wires = []
        _ = cluster.Wires(None, wires)
        return wires

    