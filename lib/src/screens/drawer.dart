import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:rust_doc/src/resources/files.dart';
import 'package:rust_doc/src/widgets/tree_view.dart';

class MyAppDrawer extends StatefulWidget {
  final InAppWebViewController? webViewController;
  const MyAppDrawer({super.key, this.webViewController});

  @override
  State<MyAppDrawer> createState() => _MyAppDrawerState();
}

class _MyAppDrawerState extends State<MyAppDrawer> {
  Map<String, dynamic> mapOfFolders =
      folderMap.values.first['children'] as Map<String, dynamic>;
  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        children: [
          const DrawerHeader(
            decoration: BoxDecoration(color: Colors.blue),
            child: Center(
              child: Column(
                children: [
                  SizedBox(
                    height: 70,
                    child: CircleAvatar(
                      radius: 40,
                      backgroundImage: AssetImage("assets/img/logo.png"),
                    ),
                  ),
                  Text(
                    "RUST DOC",
                    style: TextStyle(fontSize: 40, fontWeight: FontWeight.w900),
                  ),
                ],
              ),
            ),
          ),
          FolderTreeView(
            folderData: mapOfFolders,
            webViewController: widget.webViewController,
          ),
        ],
      ),
    );
  }
}
