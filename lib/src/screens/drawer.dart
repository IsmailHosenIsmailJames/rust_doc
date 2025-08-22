import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:rust_doc/src/resources/files.dart';

class MyAppDrawer extends StatefulWidget {
  final InAppWebViewController? webViewController;
  const MyAppDrawer({super.key, this.webViewController});

  @override
  State<MyAppDrawer> createState() => _MyAppDrawerState();
}

class _MyAppDrawerState extends State<MyAppDrawer> {
  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView.builder(
        itemCount: listOfSurfaceFolders.length + 1,
        itemBuilder: (context, index) {
          if (index == 0) {
            return const DrawerHeader(
              decoration: BoxDecoration(color: Colors.blue),
              child: Center(
                child: Column(
                  children: [
                    SizedBox(
                      height: 80,
                      child: CircleAvatar(
                        radius: 40,
                        backgroundImage: AssetImage("assets/img/logo.png"),
                      ),
                    ),
                    Text(
                      "RUST DOC",
                      style: TextStyle(
                        fontSize: 40,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                  ],
                ),
              ),
            );
          } else {
            return Padding(
              padding: const EdgeInsets.only(
                left: 15,
                right: 15,
                top: 3,
                bottom: 3,
              ),
              child: TextButton.icon(
                onPressed: () {
                  widget.webViewController?.loadUrl(
                    urlRequest: URLRequest(
                      url: WebUri(
                        "file:///android_asset/flutter_assets/assets/html/${listOfSurfaceFolders[index - 1]}/index.html",
                      ),
                    ),
                  );
                  if (Scaffold.of(context).isDrawerOpen) {
                    Scaffold.of(context).closeDrawer();
                  }
                },
                icon: const Icon(Icons.folder),
                label: Row(
                  children: [
                    Text(
                      listOfSurfaceFolders[index - 1],
                      style: const TextStyle(fontSize: 22),
                    ),
                  ],
                ),
              ),
            );
          }
        },
      ),
    );
  }
}
