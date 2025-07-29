import 'package:flutter/material.dart';

final synthwaveTheme = ThemeData(
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
