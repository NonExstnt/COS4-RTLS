# Literature Review: Real-Time Location Systems (RTLS) and Their Impact on Industrial Efficiency

## Executive Summary

Real-Time Location Systems (RTLS) have emerged as critical technologies for improving operational efficiency in manufacturing and industrial environments. This literature review examines the current state of RTLS technology, focusing on Ultra-Wideband (UWB) implementations and their application to process monitoring in manufacturing. Specifically, this review addresses how RTLS enables precise measurement of work cell duration, inter-cell transfer times, and overall production cycle times—key performance indicators that drive operational excellence in Industry 4.0 environments.

## 1. Introduction and Background

### 1.1 Definition and Scope of RTLS

Real-Time Location Systems are wireless technologies that enable continuous tracking and localisation of objects, materials, and personnel within indoor environments [1]. Unlike Global Positioning System (GPS), which functions effectively in outdoor settings, RTLS operates within enclosed factory spaces where GPS signals are attenuated by building materials [1].

RTLS technology consists of two primary hardware components: tags (battery-powered transmitters attached to tracked objects) and anchors (fixed reference points deployed throughout the facility) [1]. The system uses radio frequency signals to determine the relative position of tags within a defined grid established by the anchors. Data from these systems is processed by a Location Engine (LE) and may be integrated with Manufacturing Execution Systems (MES) or Enterprise Resource Planning (ERP) systems [1].

### 1.2 Industry 4.0 Context

RTLS implementation aligns with Industry 4.0 objectives, which emphasise the digitalisation of manufacturing processes and the creation of interconnected, data-driven production environments [1]. The Industrial Internet of Things (IIoT) paradigm positions RTLS as a fundamental enabler of real-time visibility across all production levels—from enterprise planning to shop-floor operations [1].

The digital twin concept, which creates virtual replicas of physical production systems, relies heavily on real-time positional data from RTLS to enable accurate monitoring, analysis, and optimisation of production processes [2]. This integration capability makes RTLS indispensable for advanced industrial operation planning [2].

## 2. RTLS Technologies and Positioning Methods

### 2.1 Communication Protocols

Multiple RF-based technologies support RTLS implementations, each with distinct characteristics [1]:

**Ultra-Wideband (UWB):** UWB operates across frequency bands of 3.1–10.6 GHz with a bandwidth exceeding 500 MHz [1]. This technology provides the highest accuracy for indoor positioning (approximately 0.5 meters) [1]. UWB utilises short-duration RF pulses and is resistant to multipath interference, making it suitable for complex factory environments [3].

**Wi-Fi:** Wi-Fi-based RTLS can leverage existing building infrastructure but typically achieves lower accuracy (1–5 meters) [1]. While cost-effective, Wi-Fi RTLS is less suitable for applications requiring centimeter-level precision [1].

**Bluetooth Low Energy (BLE):** BLE supports RSSI-based positioning and newer directional features (Angle of Arrival) in Bluetooth 5.1 [1]. Typical accuracy ranges from 1–5 meters [1].

**RFID:** Radio Frequency Identification systems require close contact between scanner and tag (approximately 1 meter for passive tags) [1]. RFID enables location determination only at the moment of scanning, not continuous tracking [1].

**5G:** Fifth-generation wireless networks offer high data rates and low latency (<1 millisecond) [1]. 5G is proposed for future manufacturing applications due to reduced interference and superior data transmission capabilities compared to 2.4 GHz bands [1].

### 2.2 Positioning Algorithms

RTLS systems employ several fundamental algorithms to calculate object positions [1], [3], [4]:

**Time of Arrival (ToA):** Registers signal dispatch and arrival times; distance is calculated as (time difference) × (speed of light) [1]. Requires synchronised clocks among all system components.

**Time Difference of Arrival (TDoA):** Measures time differences between signal receptions at multiple anchors [1]. When implemented with UWB, this method achieves high accuracy [3].

**Angle of Arrival (AoA):** Calculates tag position based on signal incidence angles at receiver antennas [1]. Requires minimal synchronisation but necessitates many receivers for factory-wide coverage [1].

**Two-Way Ranging (TWR):** Implements bidirectional communication between tag and anchor to calculate distance [1], [3]. Symmetric Double-Sided Two-Way Ranging (SDS-TWR) provides high precision and stability [1].

**Received Signal Strength Indicator (RSSI):** Estimates distance from signal strength measurements [1]. Simple to implement but susceptible to electromagnetic noise and non-line-of-sight (NLOS) propagation errors [1].

Advanced algorithms such as Weighted Least Squares (WLS), Maximum Likelihood Estimation (MLE), Kalman Filtering, and particle filters enhance positioning accuracy by optimising distance measurements and handling dynamic environments [4].

### 2.3 Accuracy and Performance Characteristics

**Static Accuracy:** In line-of-sight (LOS) conditions, UWB systems achieve median accuracy of 10–13 centimeters [2]. Accuracy degrades to approximately 19 centimeters when human shadowing occurs [2].

**Dynamic Accuracy:** When tracking moving objects, UWB accuracy is further degraded by 4 centimeters in typical conditions but remains bounded sufficiently to ensure safety (1–2 meter safety margins for human-robot collaboration) [2].

**Environmental Factors:** NLOS conditions caused by walls, machinery, and structural elements increase positioning error by 3–4 times compared to LOS scenarios [2], [5]. Concrete walls produce greater 2D positioning errors (approximately 40–54 centimeters) compared to plaster walls [5].

## 3. Process Monitoring Applications in Manufacturing

### 3.1 Monitoring Work Cell Duration

RTLS enables precise measurement of the time spent at individual work cells through automated data collection [6]. By attaching passive RFID tags to workstations and equipping workers with wearable RFID readers, the Method Time Measurement 4.0 (MTM4.0) system automatically records when workers enter and exit work cells [6].

Experimental validation demonstrates that this approach provides cycle times with high accuracy. For example, in a mechanical workshop experiment tracking drilling operations across multiple workstations, RTLS-based data acquisition captured precise timestamps for each operation [6]. Analysis of variance (ANOVA) confirmed the statistical significance of collected data (P-value = 0.00) [6], validating the reliability of RTLS measurements for work cell monitoring.

### 3.2 Measuring Inter-Cell Transfer Times

Transfer times between workstations represent a critical efficiency metric. RTLS tracks the movement path of materials, workers, or automated equipment as they traverse from one work cell to the next [1]. This capability enables identification of bottlenecks and delays in material flow.

A case study applying RTLS to track material flow in production processes integrated RTLS data with simulation software (Tecnomatix Plant Simulation) [3]. The system compared ideal material flow simulations against real-time RTLS-tracked movement, revealing specific zones where delays occurred [3]. This approach identified delays in filling and packaging processes caused by empty buffers, demonstrating how RTLS data pinpoints root causes of inefficiency [3].

### 3.3 Measuring Total Production Cycle Time

Comprehensive cycle time analysis benefits from integrating RTLS data across multiple operations. The Spaghetti Chart 4.0 framework automatically creates visualisations of production routes based on RTLS timestamps [6]. By tracking worker and material movements through RFID tags installed at key locations (machines, measurement tables, material boxes, control stations), practitioners can calculate:

- Cycle time per piece
- Total cycle time for batch operations
- Time spent on value-added versus non-value-added activities

Experimental results from a mechanical workshop implementing this approach showed cycle time reductions of 40–58 percent when facilities were reorganised based on RTLS insights [6]. In the baseline scenario with a job production method (one piece at a time), cycle time exceeded that of batch production methods when analysed using optimised facility layouts [6].

## 4. RTLS Implementation in Industrial Environments

### 4.1 System Architecture

Industrial RTLS implementations typically comprise five components [5]:

1. **Anchors:** Fixed reference nodes providing ranging signals to tags
2. **Tags:** Mobile transmitters attached to tracked objects
3. **Sink Nodes:** Hardware bridges (e.g., Raspberry Pi) connecting tags to network infrastructure
4. **Location Engine:** Software processing ranging data to compute positions
5. **Data Storage and Applications:** Databases and frontend applications (web, mobile) for real-time visualisation and analysis

Communication between system components flows through standardised protocols such as Message Queue Telemetry Transport (MQTT) [2], enabling seamless integration with existing manufacturing software infrastructure.

### 4.2 Anchor Configuration Optimisation

Anchor placement significantly impacts RTLS accuracy. Three primary anchor configurations have been evaluated [7]:

1. **Corner-Mounted Configuration:** Anchors positioned at room corners for maximum coverage
2. **Plane-Aligned Configuration:** Anchors aligned to room planes (X or Y axis)
3. **Wall-Centered Configuration:** Anchors positioned at the center of perimeter walls

Experimental testing shows that wall-centered configurations provide minimum positioning error (average error: 9.52 centimeters for X-component, 19.42 centimeters for Y-component) compared to corner-mounted alternatives [7]. This configuration reduces average variance and is recommended for new deployments [7].

As the number of anchors increases from three to six, 2D positioning accuracy improves; however, accuracy plateaus beyond six anchors [7]. For 2D tracking applications in LOS conditions, most configurations achieve accuracy better than 10 centimeters, making them suitable for manufacturing asset tracking [7].

### 4.3 Multi-Tag Environments

Industrial environments frequently require simultaneous tracking of numerous objects. Testing with up to 18 closely spaced tags reveals critical spacing thresholds [7]:

- **At 0.66 meter spacing:** Tags maintain accurate positioning without interference
- **At 0.10 meter spacing:** System performance degrades; average positioning errors increase to approximately 5.5 centimeters for X-direction and 10.3 centimeters for Y-direction [7]

Despite degraded performance at extremely close spacing, the system remains suitable for asset tracking applications [7]. Lower ranging frequencies (0.5 Hz) sometimes provide marginally better accuracy in dense tag environments, though with trade-offs in real-time responsiveness [7].

### 4.4 Battery Considerations

Battery management is critical for tag deployment sustainability. Testing of UWB tag batteries reveals that actual battery lifetime is approximately 25 percent of manufacturer predictions [7], requiring application of a 0.25 correction factor for practical planning [7].

For typical manufacturing scenarios with 0.2 Hz ranging frequency (location update every 5 seconds) and 6 hours daily ranging, realistic battery life extends to approximately 419 days (more than one year) for 1,100 mAh Li-Ion batteries [7]. Reducing ranging frequency to 0.017 Hz (location update every minute) extends battery life to approximately 890 days (2.5 years) [7].

## 5. Performance Metrics and KPIs

### 5.1 Key Performance Indicators for Manufacturing

RTLS-enabled process monitoring facilitates measurement of multiple manufacturing KPIs [1]:

1. **Transportation Time Reduction:** Tracking material movement identifies inefficient routes and enables layout optimisation
2. **Stock Reduction:** Real-time material location visibility enables just-in-time inventory practices
3. **Work Order Automatic Booking:** Geofencing triggers automatically log work orders when materials enter production zones
4. **Asset Utilisation:** Tracking tool usage across production areas reveals underutilised equipment
5. **Personnel Productivity:** Non-intrusive location tracking supports workflow analysis and safety monitoring
6. **Quality Related Timing:** Monitoring dwell time in specific zones supports quality control and traceability

### 5.2 Accuracy Requirements for Manufacturing Applications

Process monitoring applications have varying accuracy requirements [1]:

- **Material flow analysis:** 1–2 meter accuracy acceptable for identifying general material location
- **Work cell activity monitoring:** 10–20 centimeter accuracy required to distinguish between adjacent workstations
- **Safety applications (human-robot collaboration):** 1–2 meter safety margins recommended despite system accuracy of 10–19 centimeters [2]
- **Tool tracking:** 1 meter or better accuracy needed for tool inventory management in large facilities

UWB systems meet these requirements for most manufacturing applications, though accuracy degrades in NLOS scenarios [2], [5].

## 6. RTLS and Manufacturing Efficiency Improvements

### 6.1 Cycle Time Reduction

Documented case studies demonstrate significant cycle time improvements through RTLS-enabled process optimisation [6]:

- **Scenario 1 (Job Production, Original Layout):** Baseline cycle time established at 100 percent
- **Scenario 2 (Batch Production, Original Layout):** 45 percent cycle time reduction through batch grouping and tool consolidation
- **Scenario 3 (Job Production, Optimised Layout):** 44 percent cycle time reduction through facility layout reorganisation
- **Scenario 4 (Batch Production, Optimised Layout):** 58 percent cycle time reduction through combined batch production and layout optimisation

These improvements result from RTLS-driven insights into inefficient movement patterns and opportunities for process consolidation [6].

### 6.2 Work-in-Process Monitoring

RTLS enables real-time tracking of work-in-process (WIP) inventory through factories [1]. By establishing virtual geofences around production areas, RTLS automatically detects when materials enter, reside in, and exit specific zones. Integration with simulation software enables continuous comparison between ideal and actual material flows [3], highlighting delays and bottlenecks.

### 6.3 Safety and Ergonomic Benefits

Beyond efficiency, RTLS supports safety improvements through [1]:

- **Human Accident Detection:** Automated alerts when workers fall or remain stationary in unsafe locations [1]
- **Forklift Collision Avoidance:** Real-time position awareness enables collision prevention systems [1]
- **Social Distancing Monitoring:** Automatic alerts when workers violate predetermined distance thresholds [1]
- **Pandemic Response:** Facility layout optimisation based on RTLS data to minimise worker proximity in high-risk areas [6]

## 7. Cost Analysis and Economic Feasibility

### 7.1 System Implementation Costs

Low-cost UWB RTLS solutions have demonstrated economic viability [7]. Current system costs are approximately:

- **RTLS Board Cost:** $47AUD per tag
- **Battery Cost:** $11AUD per tag
- **Industrial Case (Injection Molded):** $3AUD per unit (for production lots of 1,000)
- **Supplier Markup:** $18AUD per tag (assumed)
- **Total Per-Unit Cost:** $79AUD

### 7.2 Return on Investment Considerations

RTLS implementation ROI depends on [1]:

1. **Quantifiable savings:** Cycle time reduction (as documented in manufacturing cases), inventory reduction, reduced tool search time
2. **System costs:** Hardware, installation, integration with existing MES/ERP systems
3. **Ongoing costs:** Battery replacement, system maintenance, software updates
4. **Risk factors:** System accuracy reliability, organisational change adoption

Industrial partners report that cycle time reductions of 40–58 percent more than justify RTLS investment in facilities with high labor costs and complex material flows [6].

## 8. Challenges and Limitations

### 8.1 Accuracy Limitations in Complex Environments

RTLS accuracy degrades significantly in NLOS scenarios [2], [5]. Concrete walls increase positioning error by 40–54 centimeters compared to optimal conditions [5]. This limitation may restrict RTLS deployment in facilities with extensive internal walls or metallic structures.

### 8.2 Multipath Propagation and Signal Reflection

Signal reflections from machinery, metal structures, and walls cause multipath interference [1]. While UWB is more resistant to multipath effects than narrowband technologies, performance still suffers in complex industrial environments [1], [3].

### 8.3 Privacy and Data Security Concerns

Tracking of personnel location raises privacy concerns that require careful organisational consideration [1]. Implementation requires coordination with worker unions, clear communication of data usage policies, and compliance with labor regulations [1].

### 8.4 System Configuration and Calibration

Accurate RTLS performance requires precise anchor positioning during installation [7]. Bias errors of 0.1–1.0 meter in anchor positions produce corresponding tag position errors, degrading system accuracy [7]. Manual calibration procedures add to implementation complexity and require skilled technicians.

### 8.5 Technology Integration Challenges

Integration of RTLS data with existing MES, ERP, and simulation software requires custom interfaces and API development [3]. Standardisation efforts are progressing, but proprietary system variations complicate interoperability [2].

## 9. Future Directions and Emerging Applications

### 9.1 Machine Learning Enhancement

Machine learning algorithms are being integrated with RTLS to improve positioning accuracy through [4]:

- **Fingerprint-based positioning:** Building radio maps that enable UWB systems to adapt to changing environmental conditions [4]
- **NLOS mitigation:** Algorithms that detect and compensate for non-line-of-sight propagation errors
- **Outlier detection:** Automatic identification and filtering of spurious position measurements

### 9.2 Integration with Digital Twins

Advanced manufacturing leverages RTLS data as a primary input to digital twin systems for [2]:

- **Real-time simulation validation:** Continuous comparison of physical and virtual production processes
- **Predictive maintenance:** Early detection of equipment or process degradation based on deviation from expected movement patterns
- **Dynamic optimisation:** Automatic adjustment of production parameters based on real-time process observations

### 9.3 5G-Based RTLS

Emerging 5G infrastructure offers advantages over conventional RF technologies [1]:

- **Reduced interference:** Licensed spectrum reduces susceptibility to interference from other wireless systems
- **Enhanced data rates:** Support for higher-frequency position updates and richer contextual data
- **Low latency:** Enables real-time control and safety-critical applications

### 9.4 Hybrid RTLS Approaches

Complementary RTLS technologies are combined to overcome individual limitations [2]:

- **UWB primary with camera vision backup:** UWB provides precise tracking; camera-based systems track personnel without wearable tags [2]
- **Multi-technology fusion:** Combining UWB, BLE, and Wi-Fi data enhances coverage and accuracy [2]

## 10. Conclusion

### 10.1 General Conclusion

Real-Time Location Systems, particularly UWB implementations, have matured into reliable technologies for manufacturing process monitoring. The capability to precisely measure work cell duration, inter-cell transfer times, and total production cycle times addresses fundamental requirements of Industry 4.0 manufacturing optimisation. Documented case studies demonstrate cycle time reductions of 40–58 percent through RTLS-enabled process analysis and facility optimisation.

Current UWB systems achieve 10–13 centimeter accuracy in favorable conditions, meeting accuracy requirements for most manufacturing applications. Economic analysis shows that low-cost RTLS solutions provide compelling ROI through documented efficiency improvements. However, performance degradation in NLOS environments and implementation complexity require careful site-specific assessment.

Integration with digital twins and machine learning represents the next generation of RTLS capability, enabling predictive optimisation and real-time process control. As standardisation progresses and 5G infrastructure deployment accelerates, RTLS is positioned to become a foundational technology for smart manufacturing.

### 10.2 Conclusion Factory of the Future

The Factory of the Future (FotF) strikes a balanced learning environment for testing RTLS implementation. The machinery and concrete pillars provide interference, but not an overwhelming amount. From testing the data is quite variable in the FotF and this is most likely due to the placement of anchors, based on the findings in the report, it's suggested to wall-center mount the anchors such that all areas of interest are covered and to increase the anchors up to 6 if possible due to the size of the FotF.

The Factory of the Future (FotF) provides a representative test environment for RTLS implementation that balances practical learning conditions with real-world complexity. The facility contains machinery and concrete structural pillars that introduce signal interference characteristic of industrial settings, though not to the extent that would preclude effective system deployment. Experimental testing within the FotF environment revealed considerable variability in positioning data, which the findings of the report attribute primarily to suboptimal anchor placement rather than fundamental environmental limitations.

Based on the findings presented throughout this review, particularly the anchor configuration research detailed in Section 4.2, implementation recommendations for the FotF include: 
1. Deploying anchors in wall-centered configurations rather than corner-mounted positions to minimise positioning error and reduce variance.
2. Increasing the anchor count to six units to provide adequate coverage given the facility's spatial dimensions. 

These modifications align with established best practices for UWB RTLS deployment in manufacturing environments and should significantly improve positioning accuracy and data consistency within the FotF facility for future data gathering.


---

## IEEE References

[1] S. Thiede, B. Sullivan, R. Damgrave, and E. Lutters, "Real-time locating systems RTLS in future factories technology review, morphology and application potentials," in *Procedia CIRP*, vol. 104, pp. 671–676, 2021. doi: 10.1016/j.procir.2021.11.113. [Online]. Available: https://doi.org/10.1016/j.procir.2021.11.113. [Accessed: Sep. 6, 2025].

[2] S. Valiollahi, I. Rodriguez, W. Zhang, H. Sharma, and P. Mogensen, "Experimental evaluation and modeling of the accuracy of real-time locating systems for industrial use," *IEEE Access*, vol. 12, pp. 75366–75395, May 2024. doi: 10.1109/ACCESS.2024.3405393. [Online]. Available: https://doi.org/10.1109/ACCESS.2024.3405393. [Accessed: Sep. 6, 2025].

[3] J. Slovak, P. Vasek, M. Simovec, M. Melicher, and D. Sismisova, "RTLS tracking of material flow in order to reveal weak spots in production process," in *Proc. 22nd Int. Conf. Process Control (PC)*, June 2019, pp. 234–238. doi: 10.1109/PC.2019.8815220. [Online]. Available: https://doi.org/10.1109/PC.2019.8815220. [Accessed: Sep. 6, 2025].

[4] M. F. R. Al-Okby, S. Junginger, T. Roddelkopf, and K. Thurow, "UWB-based real-time indoor positioning systems: a comprehensive review," *Appl. Sci.*, vol. 14, no. 23, p. 11005, Nov. 2024. doi: 10.3390/app142311005. [Online]. Available: https://doi.org/10.3390/app142311005. [Accessed: Sep. 6, 2025].

[5] J. Plangger, H. Ravichandran, M. Atia, and S. C. Rodin, "System design and performance analysis of indoor real-time localization using UWB infrastructure," in *Proc. 2023 IEEE Int. Syst. Conf. (SysCon)*, 2023, pp. 1–8. doi: 10.1109/SysCon53073.2023.10131059. [Online]. Available: https://doi.org/10.1109/SysCon53073.2023.10131059. [Accessed: Sep. 6, 2025].

[6] S. Q. D. Al-Zubaidi, E. Coli, and G. Fantoni, "Automating production process data acquisition towards spaghetti chart 4.0," *Int. J. Ind. Eng. Manag.*, vol. 13, no. 3, pp. 145–157, Sept. 2022. doi: 10.24867/IJIEM-2022-3-308. [Online]. Available: https://doi.org/10.24867/IJIEM-2022-3-308. [Accessed: Sep. 6, 2025].

[7] A. Volpi, R. Montanari, L. Tebaldi, and M. Mambrioni, "Low-cost real-time locating system solution development and implementation in manufacturing industry," *J. Sens. Actuator Netw.*, vol. 12, no. 4, p. 54, July 2023. doi: 10.3390/jsan12040054. [Online]. Available: https://doi.org/10.3390/jsan12040054. [Accessed: Sep. 6, 2025].

[8] D. Gnas et al., "Enhanced indoor positioning system using ultra-wideband technology and machine learning algorithms for energy-efficient warehouse management," *Energies*, vol. 17, no. 16, p. 4125, Aug. 2024. doi: 10.3390/en17164125. [Online]. Available: https://doi.org/10.3390/en17164125. [Accessed: Sep. 6, 2025].

[9] H. Halawa, H. Dauod, I. Lee, Y. Li, S. Yoon, and S. Chung, "Introduction of a real time location system to enhance warehouse safety and operational efficiency," *Int. J. Prod. Econ.*, vol. 224, p. 107541, 2020. doi: 10.1016/j.ijpe.2019.11.028. [Online]. Available: https://doi.org/10.1016/j.ijpe.2019.11.028. [Accessed: Sep. 6, 2025].