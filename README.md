# Safely Buoy 
### A Low Cost, Small Scale Autonomous Robotic Buoy for Watersports

One of my favourite hobbies is sailing. Having discovered my love for sailing at the age of 13, I had limited access to training programs to advance my sailing skills from 0 - yet my passion for sailing stayed. Hence, I resorted to taking courses at different local clubs, and practicing at government funded sailing centers. However, practicing independently meant I had no access to anchored buoys to set race courses for training (as these are quite large and heavy and are usually set by powerboats).

While working as an assistant sailing coach, I had the chance to set many training courses with buoys from the powerboat, and realised that they take a long time to setup, which takes away valubale training time, and also takes the coaches' attention off the sailors, who, especially if they just strated learning sailing, can get in unsafe situations. 

While there are large scale robotic buoys on the market, these are the size of a van, cost around $5000USD each and are designed for large scale international regattas - not exactly practical for individual sailors and coahces. Hence, I set out to build my very own low cost, small scale robotic buoy.

The code for the ESP-32 microcontroller on the robotic buoy is written in C on top of ESP-IDF, and communicates with GPS (UBlox M10) and IMU (LSM303) modules. A 3D compass (magnetometer) algorithm was implemented based on the Madgwick Orientation Filter to obtain a accurate heading even when the buoy rolls in waves, and I designed my own PCB extension board to eliminate loose wire connections between the modules.

While the code currently remains closed source, some snippets will be released shortly. 

# What is this repository?
This is the Remote Debugging Dashboard for the buoy. V1 was developed using Python on top of the Streamlit library, and V2 was developed as a mobile app using Flutter

Telemetry data is obtained by connecting to the ESP32 via WiFI (the ESP32 acts as an Access Point) and calling the REST API. The server is written in C on the ESP32 with ESP-IDF. Functionalities like updating the home point and emergency motor stop will be added to the dashboard in the future.
