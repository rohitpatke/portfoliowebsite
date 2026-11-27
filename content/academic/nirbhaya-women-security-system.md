---
# TODO: confirm this was Mini Project I and who was on the team.
title: "Nirbhaya: a GPS and GSM safety device for women"
summary: Built a push-button safety device on an 89C52 microcontroller that sends the wearer's GPS location by SMS to preset contacts.
problem: In an emergency, a woman may not have time to unlock a phone and call for help. A single button press needed to tell trusted contacts where she is.
timeline: 2015-07 to 2015-08
skills: [Embedded Systems, 8051 Microcontroller, GSM, GPS, AT Commands, C, Circuit Design]

venue: B.E. Electronics mini project, K.C. College of Engineering, University of Mumbai
authors: [Rohit Patke]
role: Team member
---

## Design

An Atmel 89C52 controls a GPS module, a GSM modem, an LCD, a camera sensor and a push button. When the button is pressed, the controller reads the GPS fix and sends it with AT commands to phone numbers stored in memory.
