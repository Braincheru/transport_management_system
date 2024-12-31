import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Clock, Car, MapPin, Fuel, AlertTriangle } from 'lucide-react';

const VehicleStatus = ({ vehicleId }) => {
  const [vehicle, setVehicle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const statusColors = {
    active: 'bg-green-100 text-green-800',
    maintenance: 'bg-yellow-100 text-yellow-800',
    inactive: 'bg-red-100 text-red-800'
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-lg font-semibold">Vehicle Status</CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        ) : error ? (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        ) : vehicle ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Car className="h-5 w-5" />
                <span className="font-medium">{vehicle.reg_no}</span>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm ${statusColors[vehicle.status]}`}>
                {vehicle.status}
              </span>
            </div>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-500">Last Service:</span>
                <p>{vehicle.last_service_date}</p>
              </div>
              <div>
                <span className="text-gray-500">Next Service Due:</span>
                <p>{vehicle.next_service_due}</p>
              </div>
            </div>
          </div>
        ) : (
          <p>No vehicle data available</p>
        )}
      </CardContent>
    </Card>
  );
};

const TripForm = () => {
  const [formData, setFormData] = useState({
    vehicle_id: '',
    date: '',
    from_location: '',
    to_location: '',
    odometer_start: ''
  });
  const [submitStatus, setSubmitStatus] = useState({ type: '', message: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitStatus({ type: 'info', message: 'Submitting...' });

    try {
      const response = await fetch('/driver/create_trip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      
      if (response.ok) {
        setSubmitStatus({ type: 'success', message: 'Trip created successfully!' });
        setFormData({
          vehicle_id: '',
          date: '',
          from_location: '',
          to_location: '',
          odometer_start: ''
        });
      } else {
        throw new Error(data.error || 'Failed to create trip');
      }
    } catch (error) {
      setSubmitStatus({ type: 'error', message: error.message });
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Create New Trip</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Vehicle ID</label>
              <input
                type="text"
                className="w-full p-2 border rounded"
                value={formData.vehicle_id}
                onChange={(e) => setFormData({...formData, vehicle_id: e.target.value})}
                required
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Date</label>
              <input
                type="date"
                className="w-full p-2 border rounded"
                value={formData.date}
                onChange={(e) => setFormData({...formData, date: e.target.value})}
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">From Location</label>
            <div className="flex items-center space-x-2">
              <MapPin className="h-5 w-5 text-gray-400" />
              <input
                type="text"
                className="w-full p-2 border rounded"
                value={formData.from_location}
                onChange={(e) => setFormData({...formData, from_location: e.target.value})}
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">To Location</label>
            <div className="flex items-center space-x-2">
              <MapPin className="h-5 w-5 text-gray-400" />
              <input
                type="text"
                className="w-full p-2 border rounded"
                value={formData.to_location}
                onChange={(e) => setFormData({...formData, to_location: e.target.value})}
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Odometer Start</label>
            <input
              type="number"
              className="w-full p-2 border rounded"
              value={formData.odometer_start}
              onChange={(e) => setFormData({...formData, odometer_start: e.target.value})}
              required
            />
          </div>

          {submitStatus.message && (
            <Alert variant={submitStatus.type === 'error' ? 'destructive' : 'default'}>
              <AlertDescription>{submitStatus.message}</AlertDescription>
            </Alert>
          )}

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition-colors"
          >
            Create Trip
          </button>
        </form>
      </CardContent>
    </Card>
  );
};

const ActiveTrips = ({ driverId }) => {
  const [trips, setTrips] = useState([]);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Clock className="h-5 w-5" />
          <span>Active Trips</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {trips.map((trip) => (
            <div key={trip.id} className="border rounded p-4">
              <div className="flex justify-between items-center">
                <div className="space-y-1">
                  <div className="font-medium">{trip.vehicle_reg_no}</div>
                  <div className="text-sm text-gray-500">
                    {trip.from_location} → {trip.to_location}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-500">Started:</div>
                  <div>{new Date(trip.time_out).toLocaleTimeString()}</div>
                </div>
              </div>
              <div className="mt-4 flex items-center space-x-4">
                <button className="text-blue-600 hover:text-blue-800">
                  Complete Trip
                </button>
                <button className="text-red-600 hover:text-red-800">
                  Report Issue
                </button>
              </div>
            </div>
          ))}
          {trips.length === 0 && (
            <p className="text-gray-500 text-center py-4">No active trips</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default function DriverDashboard() {
  return (
    <div className="max-w-7xl mx-auto p-4 space-y-6">
      <div className="grid md:grid-cols-2 gap-6">
        <VehicleStatus vehicleId="1" />
        <ActiveTrips driverId="1" />
      </div>
      <TripForm />
    </div>
  );
}