// app.js

// Global Variables
const loggedInUser = {
    id: 1,
    role: 'driver' // Can be 'driver', 'officer', or 'transport_officer'
};

// Initialization
document.addEventListener('DOMContentLoaded', function () {
    initApp();
});

// App Initialization
function initApp() {
    showRolePanel();
    loadVehicles();
    addEventListeners();
}

// Display Role-Specific Panel
function showRolePanel() {
    document.querySelectorAll('.role-section').forEach(section => {
        section.style.display = 'none';
    });

    const roleSectionMap = {
        driver: 'driver-section',
        officer: 'officer-section',
        transport_officer: 'transport-officer-section'
    };

    const sectionId = roleSectionMap[loggedInUser.role];
    if (sectionId) {
        document.getElementById(sectionId).style.display = 'block';
    }
}

// Event Listeners Setup
function addEventListeners() {
    // Driver Actions
    const tripForm = document.getElementById('create-trip-form');
    if (tripForm) tripForm.addEventListener('submit', handleTripFormSubmit);

    const viewTripsBtn = document.getElementById('view-tickets');
    if (viewTripsBtn) viewTripsBtn.addEventListener('click', fetchTickets);

    // Officer Actions
    const viewPendingTripsBtn = document.getElementById('view-pending-trips');
    if (viewPendingTripsBtn) viewPendingTripsBtn.addEventListener('click', fetchPendingTrips);

    // Transport Officer Actions
    const fetchTicketsBtn = document.getElementById('fetch-tickets');
    if (fetchTicketsBtn) fetchTicketsBtn.addEventListener('click', fetchTickets);
}

// Load Vehicles into Dropdown
function loadVehicles() {
    fetch('/api/vehicles')
        .then(response => response.json())
        .then(data => {
            const vehicleSelect = document.getElementById('vehicle-id');
            if (vehicleSelect) {
                vehicleSelect.innerHTML = ''; // Clear existing options
                data.vehicles.forEach(vehicle => {
                    const option = document.createElement('option');
                    option.value = vehicle.id;
                    option.textContent = `${vehicle.registration} - ${vehicle.make}`;
                    vehicleSelect.appendChild(option);
                });
            }
        })
        .catch(error => console.error('Error loading vehicles:', error));
}

// Handle Trip Form Submission
async function handleTripFormSubmit(event) {
    event.preventDefault();

    const data = {
        driver_id: document.getElementById('driver-id').value,
        vehicle_id: document.getElementById('vehicle-id').value,
        date: document.getElementById('trip-date').value,
        from_location: document.getElementById('from-location').value,
        to_location: document.getElementById('to-location').value,
        odometer_start: parseFloat(document.getElementById('odometer-start').value),
        time_out: new Date().toISOString(),
        authorizing_officer: 1 // Example officer ID
    };

    try {
        const response = await fetch('/driver/create_trip', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        alert(result.message);
        if (result.success) {
            loadTrips(); // Reload trips after successful submission
        }
    } catch (error) {
        console.error('Error submitting trip:', error);
    }
}

// Fetch and Display Tickets
async function fetchTickets() {
    try {
        const vehicleId = prompt('Enter Vehicle ID');
        if (!vehicleId) return;

        const response = await fetch(`/transport_officer/tickets/${vehicleId}`);
        const result = await response.json();

        const display = document.getElementById('tickets-display');
        if (display) {
            display.innerHTML = result.tickets
                .map(ticket => `<p>Ticket No: ${ticket.ticket_no}</p>`)
                .join('');
        }
    } catch (error) {
        console.error('Error fetching tickets:', error);
    }
}

// Fetch and Display Pending Trips
async function fetchPendingTrips() {
    try {
        const response = await fetch('/officer/pending_trips');
        const trips = await response.json();

        const display = document.getElementById('pending-trips-display');
        if (display) {
            display.innerHTML = trips
                .map(trip => `<p>Trip ID: ${trip.id}, Driver: ${trip.driver_id}</p>`)
                .join('');
        }
    } catch (error) {
        console.error('Error fetching pending trips:', error);
    }
}

// Load and Display Driver Trips
function loadTrips() {
    fetch('/api/trips')
        .then(response => response.json())
        .then(data => {
            const tripsList = document.getElementById('trips-list');
            if (tripsList) {
                tripsList.innerHTML = data.trips
                    .map(trip => `<li>${trip.date} - ${trip.from_location} to ${trip.to_location}</li>`)
                    .join('');
            }
        })
        .catch(error => console.error('Error loading trips:', error));
}
