


def displacement(initial_position, final_position):
    """Hareketin başlangıç ve bitiş konumları arasındaki deplasman."""
    return final_position - initial_position

def velocity(initial_velocity, acceleration, time):
    """Hız hesaplaması."""
    return initial_velocity + acceleration * time

def acceleration(force, mass):
    """Hızlanma hesaplaması (Newton'un İkinci Hareket Yasası)."""
    return force / mass

def force(mass, acceleration):
    """Kuvvet hesaplaması."""
    return mass * acceleration

def kinetic_energy(mass, velocity):
    """Kinetik enerji hesaplaması."""
    return 0.5 * mass * velocity**2

def gravitational_potential_energy(mass, height, g=9.8):
    """Gravitasyonel potansiyel enerji hesaplaması."""
    return mass * g * height

