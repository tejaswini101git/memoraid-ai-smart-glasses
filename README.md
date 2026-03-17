# Memoraid: Smart Wearable Cognitive Assistance System

![Prototype](images/prototype_setup.jpg)

![Patent Published](https://img.shields.io/badge/Patent-Published%20(India)-brightgreen)
![AI Powered](https://img.shields.io/badge/AI-Computer%20Vision-blue)
![Embedded System](https://img.shields.io/badge/System-ESP32--CAM-orange)
![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)

---

## Overview

Memoraid is a wearable assistive system designed to support individuals with dementia and cognitive impairments. The system integrates computer vision, embedded systems, and human-centered design into a compact smart spectacle form factor.

The device provides real-time contextual assistance through facial recognition, personalized audio prompts, and emotion-aware feedback, enabling users to maintain independence and reducing caregiver burden.

---

## Problem Statement

Dementia affects over 55 million individuals globally, leading to:

- Memory loss and confusion  
- Difficulty recognizing familiar faces  
- Dependence on caregivers  
- Loss of independence  

Existing solutions lack real-time contextual awareness and are often not wearable or integrated into daily life.

---

## Solution

Memoraid introduces a **fully integrated smart wearable system embedded in eyeglasses**, providing:

- Real-time face recognition  
- Personalized voice reminders  
- Emotion/confusion detection  
- Voice-based interaction  
- Caregiver connectivity  

---

## System Architecture

The system consists of:

### Core Hardware Components

- ESP32-CAM (Image Processing + Connectivity)
- Bone Conduction Speaker (Audio Output)
- MEMS Microphone (Voice Input)
- Li-Po Battery (Power Supply)
- Type-C Magnetic Charging Port

### Software & AI

- Face Recognition Model (Computer Vision)
- Audio Processing (DSP)
- Embedded Firmware (Arduino C/C++)
- Mobile App (Flutter + Firebase)

---

## Working Principle

1. Camera captures real-time image  
2. Face detection & recognition performed  
3. Identified person mapped to stored data  
4. Audio prompt delivered via bone conduction  
5. Microphone captures user response  
6. Emotion detection triggered if needed  
7. Data synced to caregiver application  

---

## Prototype

![Prototype Setup](images/prototype_setup.jpg)

The working prototype demonstrates:

- ESP32-CAM based vision system  
- Audio output module  
- Microphone integration  
- Embedded wiring and control  

---

## Workflow

![Workflow](images/system_flow.png)

---

## Key Features

- Fully integrated wearable design  
- Real-time face recognition  
- Bone conduction audio system  
- Emotion detection capability  
- IoT-enabled caregiver monitoring  
- Lightweight and discreet form factor  

---

## Novelty

According to the invention disclosure :contentReference[oaicite:1]{index=1}:

- Integration of all components inside spectacles  
- Combined face recognition + audio prompting  
- Bone conduction for non-intrusive output  
- Emotion detection via voice analysis  
- Affordable embedded architecture  

---

## Patent Information

Patent Title:  
Smart Wearable for Memory Support in Dementia Patients  

Publication Date:  
22 August 2025  

Jurisdiction:  
Indian Patent Office  

Status:  
Patent Published – Awaiting Examination  

![Patent](images/patent_publication.jpg)

---

## Future Work

- Miniaturization of hardware  
- Advanced AI models (edge inference)  
- Companion mobile application expansion  
- 3D wearable design optimization  
- Real-world clinical testing  

---

## Contributors

Mandal Tejaswini  
Gadiraju Jashwanth Varma  
Kakumanu Harshith Subrahmanyam  
Srinithya Reddy Dyava  

---

## License

Apache 2.0 License
