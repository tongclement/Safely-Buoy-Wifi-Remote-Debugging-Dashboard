import 'dart:async';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:fl_chart/fl_chart.dart';
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}
class KpiDisplay extends StatelessWidget {
  final String label;
  final String value;

  const KpiDisplay({Key? key, required this.label, required this.value}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Text(label, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
        Text(value, style: TextStyle(fontSize: 18)),
      ],
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final String telemetryUrl = 'http://192.168.4.1';
  List<FlSpot> currentheadingData = [];
  List<FlSpot> targetheadingData = [];
  List<FlSpot> currentvelocityData = [];
  List<FlSpot> targetvelocityData = [];
  List<FlSpot> motorData = [];
  double time = 0;
  // Declare KPI state variables
  double currentHeading = 0.0;
  double targetHeading = 0.0;
  double currentVelocity = 0.0;
  double targetVelocity = 0.0;
  double motorPowerSetting = 0.0;
  double distanceToHome = 0.0;

  @override
  void initState() {
    super.initState();
    Timer.periodic(Duration(seconds: 1), (timer) {
      fetchTelemetryData();
      time += 1;
    });
  }

  Future<void> fetchTelemetryData() async {
    final response = await http.get(Uri.parse(telemetryUrl));
    final telemetry = json.decode(response.body);

    setState(() {
      currentheadingData
          .add(FlSpot(time, double.parse(telemetry['Current Hdg'].toString())));
      targetheadingData
          .add(FlSpot(time, double.parse(telemetry['Target Hdg'].toString())));
      currentvelocityData
          .add(FlSpot(time, double.parse(telemetry['Current vel'].toString())));
      targetvelocityData
          .add(FlSpot(time, double.parse(telemetry['Target vel'].toString())));
      motorData.add(FlSpot(
          time, double.parse(telemetry['Current Motor Setting'].toString())));


      // Update KPI state variables
      currentHeading = double.parse(telemetry['Current Hdg'].toString());
      targetHeading = double.parse(telemetry['Target Hdg'].toString());
      currentVelocity = double.parse(telemetry['Current vel'].toString());
      targetVelocity = double.parse(telemetry['Target vel'].toString());
      motorPowerSetting = double.parse(telemetry['Current Motor Setting'].toString());
      distanceToHome = double.parse(telemetry['Distance To Home'].toString());

    });
  }

  Future<void> estop() async {
    await http.get(Uri.parse('$telemetryUrl/estop'));
  }

  Future<void> turnOn() async {
    await http.get(Uri.parse('$telemetryUrl/on'));
  }

  Future<void> saveToCsv() async {
    // This is a placeholder for the save to CSV functionality.
    // Flutter does not have a direct way to save to CSV in the backend.
    // You might want to send the data to a server that handles the CSV creation.
  }

  LineChartData getLineChartData(List<FlSpot> spots) {
    return LineChartData(
      gridData: FlGridData(show: true),
      titlesData: FlTitlesData(show: true),
      borderData: FlBorderData(show: true),
      lineBarsData: [
        LineChartBarData(
          spots: spots,
          isCurved: true,
          //colors: [Colors.blue],
          barWidth: 5,
          isStrokeCapRound: true,
          dotData: FlDotData(show: false),
          belowBarData: BarAreaData(show: false),
        ),
      ],
    );
  }

  LineChartData twolinesgetLineChartData(List<FlSpot> spots1,spots2, [String? type]) {
    //type is optional, only used to set hdg graph to 0-360
    return LineChartData(
      minY: type == "hdg" ? 0 : null, // Conditional minY based on type
      maxY: type == "hdg" ? 360 : null, // Conditional maxY based on type

      gridData: FlGridData(show: true),
      titlesData: FlTitlesData(show: true),
      borderData: FlBorderData(show: true),
      lineBarsData: [
        LineChartBarData(
          spots: spots1,
          isCurved: true,
          //colors: [Colors.blue],
          barWidth: 5,
          isStrokeCapRound: true,
          dotData: FlDotData(show: false),
          belowBarData: BarAreaData(show: false),
          color: Colors.blue
        ),
        LineChartBarData(
          spots: spots2,
          isCurved: true,
          //colors: [Colors.blue],
          barWidth: 5,
          isStrokeCapRound: true,
          dotData: FlDotData(show: false),
          belowBarData: BarAreaData(show: false),
          color: Colors.green
        ),
      ],
    );
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Real-Time Buoy Dashboard'),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        children: <Widget>[
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              ElevatedButton(
                onPressed: estop,
                child: Text('E-Stop'),
              ),
              ElevatedButton(
                onPressed: turnOn,
                child: Text('Turn On'),
              ),
              ElevatedButton(
                onPressed: saveToCsv,
                child: Text('Save to CSV'),
              ),
            ],
          ),
          // KPI display row
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              KpiDisplay(label: "Current Heading", value: "$currentHeading"),
              KpiDisplay(label: "Target Heading", value: "$targetHeading"),
            ],
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              KpiDisplay(label: "Current Velocity", value: "$currentVelocity m/s"),
              KpiDisplay(label: "Target Velocity", value: "$targetVelocity m/s"),
            ],
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              KpiDisplay(label: "Motor Power", value: "$motorPowerSetting%"),
              KpiDisplay(label: "Distance to Home", value: "$distanceToHome m"),
            ],
          ),


          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: LineChart(twolinesgetLineChartData(currentheadingData,targetheadingData,"hdg")),
            ),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: LineChart(twolinesgetLineChartData(currentvelocityData,targetvelocityData)),
            ),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: LineChart(getLineChartData(motorData)),
            ),
          ),
        ],
      ),
    );
  }
}
