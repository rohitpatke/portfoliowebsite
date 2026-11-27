---
title: "Tiny Bytes: physical programming blocks for rural kids"
summary: Built an educational game where children snap together microcontroller-powered blocks to program a character on a TFT screen. It teaches programming logic without a computer.
problem: Schools in rural India lack computers and connectivity, and screen-only e-learning doesn't build hands-on, constructive skills. Children aged nine and up needed a cheap, tactile way to learn computational thinking.
timeline: 2016-07 to 2017-05
skills: [Embedded Systems, Arduino, Microcontrollers, C, Circuit Design, PCB Design, Educational Technology]

venue: B.E. Electronics final-year project, K.C. College of Engineering, University of Mumbai
authors: [Rohit Patke, Ajay Bhadane, Raveena Mehta]
role: Team member (guide, Prof. Srinivasa Battu)

decisions:
  - id: physical-blocks
    question: Should the programming interface be on a screen or in the hands?
    options: [A tablet app with visual blocks, Physical blocks that connect together]
    chose: Physical blocks that connect together
    why: Tablets cost more than rural schools can afford and add to screen time. Physical blocks (each with an ATmega328P) teach sequencing and logic through building and touch, while a single display shows the result.
    bubble: Made code something kids can hold.

outcomes:
  - metric: Recommended age
    value: 9+
featured: true
order: 20
---

## How it works

- **Blocks:** each command block carries an ATmega328P and connects to its neighbours, so the chain of blocks is the program.
- **Base and brain boards:** an Arduino Mega reads the block chain and drives an ILI9488 TFT display.
- **Game:** the child's sequence moves a character through a level. The screen also shows the equivalent code, so the link to real syntax is visible, and an end-of-game screen gives feedback.

## Report

Covers the literature survey (block-based and visual programming, electronic blocks, e-learning), hardware and software implementation, circuit, block and flow diagrams, results, applications and future scope.
