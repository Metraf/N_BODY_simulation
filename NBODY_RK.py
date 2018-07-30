import matplotlib.pyplot as plt
import math

nb_annees = 1000
nb_UA = 5
intervalle_nb_jours = 1
# excentricity
e = 0.02
e_pltl = 0
a_fois_pltl = 0.9
# constants :
constG = 6.67408 * 10 ** (-11)
nbiter = 31536000 * nb_annees
a = 149597900000.0 * nb_UA
a_pltl = a * a_fois_pltl
intervalle = 86400 * intervalle_nb_jours

# Working on NBODY_RK


class Planetesimal:
    """represents a planetimal"""

    plan_mass = 5.97e+24
    star_mass = 1.9884e+30
    mu = constG * star_mass

    def __init__(self):

        self.tolerance = 1e-14
        self.dt = intervalle

        # orbital param initialisation
        self.dE = self.tolerance + 1
        self.M = math.fmod(self.dt * math.sqrt(self.mu / a_pltl ** 3), 2 * math.pi)
        self.E = self.E0 = self.M
        while self.dE > self.tolerance:
            self.E = self.E - (self.E - e_pltl * math.sin(self.E) - self.M) / (1 - e_pltl * math.cos(self.E))
            self.dE = math.fabs(self.E - self.E0)
            self.E0 = self.E

        self.r = a_pltl * (1 - e_pltl * math.cos(self.E))
        self.nu = 2 * math.atan2(math.sqrt(1 + e_pltl) * math.sin(self.E / 2), math.sqrt(1 - e_pltl) * math.cos(self.E / 2))

        self.posx = a_pltl
        self.posy = 0
        self.vx = -math.sin(self.E) * math.sqrt(self.mu * a_pltl) / self.r
        self.vy = math.sqrt(1 - e_pltl ** 2) * math.cos(self.E) * math.sqrt(self.mu * a_pltl) / self.r
        # end of orbital initialisation param

    def __iter__(self):
        return self

    def accel_planetesimal(self, posx, posy):
        # acceleration of one planetesimal
        return [(-posx * constG * self.star_mass / (math.sqrt(posx ** 2 + posy ** 2) ** 3)) + ((
                    planete.posx - posx) * constG * self.plan_mass / (
                            math.sqrt((planete.posx - posx) ** 2 + (planete.posy - posy) ** 2) ** 3)),
                (-posy * constG * self.star_mass / (math.sqrt(posx ** 2 + posy ** 2) ** 3)) + ((
                            planete.posy - posy) * constG * self.plan_mass / (
                            math.sqrt((planete.posx - posx) ** 2 + (planete.posy - posy) ** 2) ** 3))]

    def __next__(self):
        # k1
        self.k1s = self.accel_planetesimal(self.posx, self.posy)

        self.k1px = self.vx
        self.k1py = self.vy

        # k2
        self.k2s = self.accel_planetesimal(self.posx + self.k1px * self.dt / 2, self.posy + self.k1py * self.dt / 2)

        self.k2px = self.vx + self.k1s[0] * self.dt / 2
        self.k2py = self.vy + self.k1s[1] * self.dt / 2

        # k3
        self.k3s = self.accel_planetesimal(self.posx + self.k2px * self.dt / 2, self.posy + self.k2py * self.dt / 2)

        self.k3px = self.vx + self.k2s[0] * self.dt / 2
        self.k3py = self.vy + self.k2s[1] * self.dt / 2

        # k4
        self.k4s = self.accel_planetesimal(self.posx + self.k3px * self.dt, self.posy + self.k3py * self.dt)

        self.k4px = self.vx + self.k3s[0] * self.dt
        self.k4py = self.vy + self.k3s[1] * self.dt

        # calculating speed at time + dt
        self.vx = self.vx + self.dt * (self.k1s[0] + 2 * self.k2s[0] + 2 * self.k3s[0] + self.k4s[0]) / 6
        self.vy = self.vy + self.dt * (self.k1s[1] + 2 * self.k2s[1] + 2 * self.k3s[1] + self.k4s[1]) / 6
        # calculating position at time + dt
        self.posx = self.posx + self.dt * (self.k1px + 2 * self.k2px + 2 * self.k3px + self.k4px) / 6
        self.posy = self.posy + self.dt * (self.k1py + 2 * self.k2py + 2 * self.k3py + self.k4py) / 6

        return self




class Planete:
    """représente une planète"""

    mass = 5.97e+24  # Earth mass
    star_mass = 1.9884e+30  # Sun mass
    mu = constG * star_mass

    def __init__(self, name):
        self.name = name
        self.t = 0
        self.tolerance = 1e-14
        self.dt = intervalle

        # orbital param initialisation
        self.dE = self.tolerance + 1
        self.M = math.fmod(self.dt * math.sqrt(self.mu / a ** 3), 2 * math.pi)
        self.E = self.E0 = self.M
        while self.dE > self.tolerance:
            self.E = self.E - (self.E - e * math.sin(self.E) - self.M) / (1 - e * math.cos(self.E))
            self.dE = math.fabs(self.E - self.E0)
            self.E0 = self.E

        self.r = a * (1 - e * math.cos(self.E))
        self.nu = 2 * math.atan2(math.sqrt(1 + e) * math.sin(self.E / 2), math.sqrt(1 - e) * math.cos(self.E / 2))

        self.posx = a
        self.posy = 0
        self.vx = -math.sin(self.E) * math.sqrt(self.mu * a) / self.r
        self.vy = math.sqrt(1 - e ** 2) * math.cos(self.E) * math.sqrt(self.mu * a) / self.r
        # end of orbital initialisation param

    def __iter__(self):
        return self

    def accel(self, posx, posy):
        # acceleration
        return [-posx * constG * self.star_mass / (math.sqrt(posx ** 2 + posy ** 2) ** 3),
                -posy * constG * self.star_mass / (math.sqrt(posx ** 2 + posy ** 2) ** 3)]

    def __next__(self):

        # k1
        self.k1s = self.accel(self.posx, self.posy)

        self.k1px = self.vx
        self.k1py = self.vy

        # k2
        self.k2s = self.accel(self.posx + self.k1px * self.dt / 2, self.posy + self.k1py * self.dt / 2)

        self.k2px = self.vx + self.k1s[0] * self.dt / 2
        self.k2py = self.vy + self.k1s[1] * self.dt / 2

        # k3
        self.k3s = self.accel(self.posx + self.k2px * self.dt / 2, self.posy + self.k2py * self.dt / 2)

        self.k3px = self.vx + self.k2s[0] * self.dt / 2
        self.k3py = self.vy + self.k2s[1] * self.dt / 2

        # k4
        self.k4s = self.accel(self.posx + self.k3px * self.dt, self.posy + self.k3py * self.dt)

        self.k4px = self.vx + self.k3s[0] * self.dt
        self.k4py = self.vy + self.k3s[1] * self.dt

        # calculating speed at time + dt
        self.vx = self.vx + self.dt * (self.k1s[0] + 2 * self.k2s[0] + 2 * self.k3s[0] + self.k4s[0]) / 6
        self.vy = self.vy + self.dt * (self.k1s[1] + 2 * self.k2s[1] + 2 * self.k3s[1] + self.k4s[1]) / 6
        # calculating position at time + dt
        self.posx = self.posx + self.dt * (self.k1px + 2 * self.k2px + 2 * self.k3px + self.k4px) / 6
        self.posy = self.posy + self.dt * (self.k1py + 2 * self.k2py + 2 * self.k3py + self.k4py) / 6

        self.t += self.dt

        return self

    """def error1(self):
        self.e_cin = 0.5 * self.mass * math.sqrt(self.vx ** 2 + self.vy ** 2)
        self.e_pot = 0.5 * constG * self.mass * self.star_mass / math.sqrt(self.posx ** 2 + self.posy ** 2)
        self.e_tot = -self.e_cin + self.e_pot
        return self

    def error2(self):
        self.e_cin = 0.5 * self.mass * math.sqrt(self.vx ** 2 + self.vy ** 2)
        self.e_pot = 0.5 * constG * self.mass * self.star_mass / math.sqrt(self.posx ** 2 + self.posy ** 2)
        self.e_tot2 = -self.e_cin + self.e_pot
        self.de_tot = (self.e_tot2 - self.e_tot) / self.e_tot
        return self """


planete = Planete('Terre')
print(planete.name)
coordx, coordy = [], []  # lists containing coordinates of the planet
# planete.error1()
mvt = iter(planete)  # iter launch

#planetesimal setting
coordx_pltl, coordy_pltl = [], [] #lists containing planetesimal's coordinates
planetesimal1 = Planetesimal()
mvt_pltl = iter(planetesimal1)

while True:

    coordx.append(planete.posx)
    coordy.append(planete.posy)
    coordx_pltl.append(planetesimal1.posx)
    coordy_pltl.append(planetesimal1.posy)


    next(mvt)
    next(planetesimal1)
    if math.sqrt(planete.posx ** 2 + planete.posy ** 2) < 1400000:
        break

    if planete.t > nbiter:
        break

# planete.error2()
# print("dE =", planete.de_tot)
plt.grid(True)
plt.plot(coordx, coordy, linestyle='-.')  # planet's coordinates
plt.plot(coordx_pltl, coordy_pltl, linestyle='-.', color='g')  # planetesimals coordinates
plt.plot([0], marker='o', color='r')  # star's coordinates
plt.show()
