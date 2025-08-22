import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:rust_doc/src/resources/files.dart';
import 'package:rust_doc/src/screens/rust_doc.dart';

final localhostServer = InAppLocalhostServer(
  documentRoot: 'assets',
  port: 9387,
);

Future main() async {
  WidgetsFlutterBinding.ensureInitialized();
  if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
    await InAppWebViewController.setWebContentsDebuggingEnabled(kDebugMode);
  }

  if (!kIsWeb) {
    await localhostServer.start();
  }

  allHTMLFilesPathSorted = List<String>.from(
    jsonDecode(await rootBundle.loadString('assets/html_files.json')),
  );

  folderMap = jsonDecode(await rootBundle.loadString('assets/folder_map.json'));

  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  MyAppState createState() => MyAppState();
}

class MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      themeMode: ThemeMode.dark,
      theme: ThemeData.light(),
      darkTheme: ThemeData.dark(),
      home: const InAppWebViewExampleScreen(),
    );
  }
}
