    def Move(self):
        
        Px, Py = self.getPos()
        self.getScanResults()
        
        MaxMove = 3
        
        SumVec = np.array([0,0])
        
        ZombieIDs = [data.getID() for data in self.getScanResults()] # Is this only zombie IDs?
        
        for ID in ZombieIDs:
            # Grab zombie information from last scan
            Zx, Zy = ZombieIDs.getPos()
            
            # Determine Manhattan distance
            Magnitude = abs(Px - Zx) + abs(Py - Zy)
            
            # Determine vector from zombie to player
            Vector = np.array([Px - Zx, Py - Zy])
            Vector = Vector/np.linalg.norm(Vector)
            Vector = Vector*Magnitude
            
            # Sum all vectors from all zombies
            SumVec = np.add(SumVec, Vector)
        
        # Determine unit vector with optimal movement
        SumVec = SumVec/np.linalg.norm(SumVec)
        
        # Convert vector into nearest, legal Manhattan distance
        x_off = round(SumVec[0]*MaxMove)
        y_off = round(SumVec[1]*MaxMove)        
        
        # Check the map bounds and move player as close as possible
        map_view = self.getMapView()
        size_x, size_y = map_view.getMapSize()
        PxNew = Px + x_off
        PyNew = Py + y_off
        
        while True:
            if PxNew < 0:
                PxNew = PxNew + 1
            elif PxNew >= size_x:
                PxNew = PxNew - 1
            else:
                break
 
        while True:
            if PyNew < 0:
                PyNew = PyNew + 1
            elif PxNew >= size_x:
                PyNew = PyNew - 1
            else:
                break
        
        # Set trapped flag if player is trapped
        PTrapped = False
        if PxNew == Px and PyNew == Py:
            PTrapped = True
            
        return MoveEvent(self, PxNew, PyNew)