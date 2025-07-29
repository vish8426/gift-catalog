import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

final synthwaveTheme = ThemeData(
  useMaterial3: true,
  brightness: Brightness.dark,
  scaffoldBackgroundColor: const Color(0xFF0D0D0D),
  primaryColor: const Color(0xFF00FFFF),
  fontFamily: 'Consolas',
  textTheme: const TextTheme(
    bodyMedium: TextStyle(color: Colors.white),
  ),
  colorScheme: const ColorScheme.dark(
    primary: Color(0xFF00FFFF),
    secondary: Color(0xFFFF77FF),
    surface: Color(0xFF1A1A1A),
    onSurface: Colors.white,
    onPrimary: Colors.black,
    onSecondary: Colors.black,
  ),
);

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gift Catalog',
      theme: synthwaveTheme,
      home: const HomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gift Catalog'),
      ),
      body: const Center(
        child: Text(
          'Welcome to the Synthwave-themed Gift Catalog!',
          style: TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}
