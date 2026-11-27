---
title: Ultrasonic Arduino theremin
summary: Built a touchless musical instrument that uses two ultrasonic sensors in place of a theremin's antennas, one for pitch and one for volume.
problem: A classic theremin relies on tuned RLC oscillators that are fiddly to build and calibrate. We wanted the same play-without-touching feel from cheap, reliable parts.
timeline: 2015-12 to 2016-04
skills: [Arduino, Embedded Systems, Microcontrollers, Sensors, C, Circuit Design, PCB Design]

venue: B.E. Electronics mini project, K.C. College of Engineering, University of Mumbai
authors: [Rohit Patke, Ajay Bhadane]
role: Team member

decisions:
  - id: ultrasound-not-antennas
    question: How should hand position be sensed?
    options: [Heterodyne RLC antennas, HC-SR04 ultrasonic sensors]
    chose: HC-SR04 ultrasonic sensors
    why: Ultrasonic modules give a distance reading directly to an ATmega328 with no analog tuning, so mapping hand distance to pitch and gain became a software problem.
---

## Build

An ATmega328 with a 16 MHz crystal on a custom PCB, two HC-SR04 sensors, status LEDs and a power source. The reflected-wave readings are sampled into amplitude levels that set the note and its volume.
