class Neo4jConnection:
    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_interaction(self, data):
        with self.driver.session() as session:
            query = """
            MERGE (d1:Device {id: $device1_id})
            ON CREATE SET
                d1.name = $device1_name,
                d1.brand = $device1_brand,
                d1.model = $device1_model,
                d1.os = $device1_os
            MERGE (d2:Device {id: $device2_id})
            ON CREATE SET
                d2.name = $device2_name,
                d2.brand = $device2_brand,
                d2.model = $device2_model,
                d2.os = $device2_os
            CREATE (d1)-[r:CONNECTED {
                method: $method,
                bluetooth_version: $bluetooth_version,
                signal_strength_dbm: $signal_strength,
                distance_meters: $distance,
                duration_seconds: $duration,
                timestamp: datetime($timestamp),
                from_latitude: $from_latitude,
                from_longitude: $from_longitude,
                from_altitude: $from_altitude,
                from_accuracy: $from_accuracy,
                to_latitude: $to_latitude,
                to_longitude: $to_longitude,
                to_altitude: $to_altitude,
                to_accuracy: $to_accuracy
            }]->(d2)
            RETURN id(r) as interaction_id
            """
            device1, device2 = data['devices']
            interaction = data['interaction']
            result = session.run(query, {
                'device1_id': device1['id'],
                'device1_name': device1['name'],
                'device1_brand': device1['brand'],
                'device1_model': device1['model'],
                'device1_os': device1['os'],
                'device2_id': device2['id'],
                'device2_name': device2['name'],
                'device2_brand': device2['brand'],
                'device2_model': device2['model'],
                'device2_os': device2['os'],
                'method': interaction['method'],
                'bluetooth_version': interaction.get('bluetooth_version'),
                'signal_strength': interaction.get('signal_strength_dbm'),
                'distance': interaction.get('distance_meters'),
                'duration': interaction.get('duration_seconds'),
                'timestamp': interaction['timestamp'],
                'from_latitude': device1['location']['latitude'],
                'from_longitude': device1['location']['longitude'],
                'from_altitude': device1['location']['altitude_meters'],
                'from_accuracy': device1['location']['accuracy_meters'],
                'to_latitude': device2['location']['latitude'],
                'to_longitude': device2['location']['longitude'],
                'to_altitude': device2['location']['altitude_meters'],
                'to_accuracy': device2['location']['accuracy_meters']

            })
            return result.single()['interaction_id']

    def get_bluetooth_connections (self):
        with self.driver.session() as session:
            query = """
                    MATCH path = (d1:Device)-[r:CONNECTED*]-(d2:Device)
                    WHERE all(rel IN r WHERE rel.method = 'Bluetooth')
                    AND id(d1) < id(d2) 
                    RETURN d1.id as device1, d2.id as device2, length(path) as path_length
                    """
            result = session.run(query)
            return result.single()

    def get_strong_connections(self):
        with self.driver.session() as session:
            query = """
                    MATCH (d1:Device)-[r:CONNECTED]-(d2:Device)
                    WHERE r.signal_strength_dbm > -60
                    RETURN d1.id as device1, d2.id as device2, r.signal_strength_dbm as signal_strength
                    """
            result = session.run(query)
            return result.data()

