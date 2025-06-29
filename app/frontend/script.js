let buses = [];

document.addEventListener('DOMContentLoaded', async function () {
  const busSelect = document.getElementById('busSelect');

  try {
    const res = await fetch('/buses/');
    buses = await res.json();

    buses.forEach(bus => {
      const option = document.createElement('option');
      option.value = bus.id;
      option.textContent = `${bus.bus_number} — ${bus.origin} → ${bus.destination}`;
      busSelect.appendChild(option);
    });

    busSelect.addEventListener('change', updateBusDetails);
  } catch (error) {
    busSelect.innerHTML = '<option disabled>Error loading buses</option>';
  }
});

function updateBusDetails() {
  const selectedId = parseInt(document.getElementById('busSelect').value);
  const selectedBus = buses.find(b => b.id === selectedId);

  if (selectedBus) {
    document.getElementById('origin').value = selectedBus.origin;
    document.getElementById('destination').value = selectedBus.destination;
    document.getElementById('price').value = selectedBus.price;
  }
}

document.getElementById('bookingForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const name = document.getElementById('passengerName').value;
  const busId = parseInt(document.getElementById('busSelect').value);
  const seat = document.getElementById('seatNumber').value;
  const responseDiv = document.getElementById('response');

  responseDiv.innerHTML = "Booking...";

  const bookingData = {
    passenger_name: name,
    seat_number: parseInt(seat),
    bus_id: busId
  };

  try {
    const res = await fetch('/bookings/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(bookingData)
    });

    if (!res.ok) {
      const error = await res.json();
      responseDiv.innerHTML = `<p style="color:red;">${error.detail}</p>`;
      return;
    }

    const data = await res.json();
    responseDiv.innerHTML = `
      <p style="color:green;">Ticket Booked!</p>
      <p>Ticket Code: ${data.ticket_code}</p>
      <p>Bus ID: ${data.bus_id}</p>
      <p>Seat: ${data.seat_number}</p>
    `;
  } catch (error) {
    responseDiv.innerHTML = `<p style="color:red;">Could not connect to server.</p>`;
  }
});
