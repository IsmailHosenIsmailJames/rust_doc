import 'dart:collection';
import 'package:fluentui_system_icons/fluentui_system_icons.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:rust_doc/main.dart';
import 'package:rust_doc/src/resources/files.dart';
import 'package:rust_doc/src/screens/drawer.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';

class InAppWebViewExampleScreen extends StatefulWidget {
  const InAppWebViewExampleScreen({super.key});

  @override
  InAppWebViewExampleScreenState createState() =>
      InAppWebViewExampleScreenState();
}

class InAppWebViewExampleScreenState extends State<InAppWebViewExampleScreen> {
  final GlobalKey webViewKey = GlobalKey();

  InAppWebViewController? webViewController;
  InAppWebViewSettings settings = InAppWebViewSettings(
    isInspectable: kDebugMode,
    mediaPlaybackRequiresUserGesture: false,
    allowsInlineMediaPlayback: true,
    iframeAllow: "camera; microphone",
    iframeAllowFullscreen: true,
  );

  PullToRefreshController? pullToRefreshController;

  late ContextMenu contextMenu;
  String url = "";
  double progress = 0;
  Widget initWiget = const Center(child: CircularProgressIndicator());

  void initLastWebUrl() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    String initUrl =
        prefs.getString("last_url_doc") ??
        "file:///android_asset/flutter_assets/assets/html/index.html";
    makeAppBarTitle(initUrl);
    setState(() {
      initWiget = InAppWebView(
        key: webViewKey,
        // initialFile: initUrl,
        initialUrlRequest: URLRequest(url: WebUri(initUrl)),
        // initialUrlRequest:
        // URLRequest(url: WebUri(Uri.base.toString().replaceFirst("/#/", "/") + 'page.html')),
        // initialFile: "assets/index.html",
        initialUserScripts: UnmodifiableListView<UserScript>([]),
        initialSettings: settings,
        contextMenu: contextMenu,
        pullToRefreshController: pullToRefreshController,
        onWebViewCreated: (controller) async {
          webViewController = controller;
        },
        onLoadStart: (controller, url) async {
          setState(() {
            this.url = url.toString();
          });
          final SharedPreferences prefs = await SharedPreferences.getInstance();
          if (url != null) {
            await prefs.setString("last_url_doc", url.toString());
          }
          makeAppBarTitle(url.toString());
        },
        onPermissionRequest: (controller, request) async {
          return PermissionResponse(
            resources: request.resources,
            action: PermissionResponseAction.GRANT,
          );
        },
        shouldOverrideUrlLoading: (controller, navigationAction) async {
          var uri = navigationAction.request.url!;

          if (![
            "http",
            "https",
            "file",
            "chrome",
            "data",
            "javascript",
            "about",
          ].contains(uri.scheme)) {
            if (await canLaunchUrl(uri)) {
              // Launch the App
              await launchUrl(uri);
              // and cancel the request
              return NavigationActionPolicy.CANCEL;
            }
          }

          return NavigationActionPolicy.ALLOW;
        },
        onLoadStop: (controller, url) async {
          pullToRefreshController?.endRefreshing();
          setState(() {
            this.url = url.toString();
          });
        },
        onReceivedError: (controller, request, error) {
          pullToRefreshController?.endRefreshing();
        },
        onProgressChanged: (controller, progress) {
          if (progress == 100) {
            pullToRefreshController?.endRefreshing();
          }
          setState(() {
            this.progress = progress / 100;
          });
        },
        onUpdateVisitedHistory: (controller, url, isReload) {
          setState(() {
            this.url = url.toString();
          });
        },
        onConsoleMessage: (controller, consoleMessage) {},
      );
    });
  }

  @override
  void initState() {
    super.initState();
    contextMenu = ContextMenu(
      menuItems: [
        ContextMenuItem(
          id: 1,
          title: "Special",
          action: () async {
            await webViewController?.clearFocus();
          },
        ),
      ],
      settings: ContextMenuSettings(hideDefaultSystemContextMenuItems: false),
      onCreateContextMenu: (hitTestResult) async {},
    );

    pullToRefreshController =
        kIsWeb ||
                ![
                  TargetPlatform.iOS,
                  TargetPlatform.android,
                ].contains(defaultTargetPlatform)
            ? null
            : PullToRefreshController(
              settings: PullToRefreshSettings(color: Colors.blue),
              onRefresh: () async {
                if (defaultTargetPlatform == TargetPlatform.android) {
                  webViewController?.reload();
                } else if (defaultTargetPlatform == TargetPlatform.iOS ||
                    defaultTargetPlatform == TargetPlatform.macOS) {
                  webViewController?.loadUrl(
                    urlRequest: URLRequest(
                      url: await webViewController?.getUrl(),
                    ),
                  );
                }
              },
            );

    initLastWebUrl();
  }

  @override
  void dispose() {
    super.dispose();
  }

  String appBarTitile = "";

  void makeAppBarTitle(String url) {
    if (url.startsWith("file")) {
      List partsOfURL = url.split("/");
      List toBeShow = partsOfURL.sublist(6);
      String showString = toBeShow.toString();
      showString = showString
          .replaceAll(" ", "")
          .replaceAll("[", "")
          .replaceAll("]", "")
          .replaceAll(",", "/");
      setState(() {
        appBarTitile = showString;
      });
    } else {
      setState(() {
        appBarTitile = url;
      });
    }
    setState(() {
      showSearchBar = false;
      appBarSeacrchIcon = Icons.search;
    });
  }

  TextEditingController searchController = TextEditingController();
  TextEditingValue textEditingValue = const TextEditingValue();
  bool showSearchBar = false;
  IconData appBarSeacrchIcon = Icons.search;
  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, result) async {
        bool? canPop = await webViewController?.canGoBack();
        if (canPop == true) {
          webViewController?.goBack();
        } else {
          SystemNavigator.pop();
        }
      },
      child: Scaffold(
        drawer: MyAppDrawer(),
        appBar: AppBar(
          titleSpacing: 0,
          toolbarHeight: 43,
          title: Row(
            children: [
              IconButton(
                onPressed: () async {
                  final SharedPreferences prefs =
                      await SharedPreferences.getInstance();
                  String homePage =
                      prefs.getString("home_page_doc") ??
                      "file:///android_asset/flutter_assets/assets/html/index.html";
                  await webViewController?.loadUrl(
                    urlRequest: URLRequest(url: WebUri(homePage)),
                  );
                },
                icon: const Icon(FluentIcons.home_24_regular),
              ),
              Expanded(
                child: Autocomplete<String>(
                  optionsMaxHeight: 380,
                  fieldViewBuilder: (
                    context,
                    textEditingController,
                    focusNode,
                    onFieldSubmitted,
                  ) {
                    return SizedBox(
                      height: 38,
                      child: CupertinoSearchTextField(
                        controller: textEditingController,
                        focusNode: focusNode,
                        style: const TextStyle(color: Colors.grey),
                      ),
                    );
                  },
                  optionsBuilder: (TextEditingValue textEditingValue) {
                    if (textEditingValue.text == '') {
                      return const Iterable<String>.empty();
                    }
                    return allHTMLFilesPathSorted.where((String option) {
                      return option.toLowerCase().contains(
                        textEditingValue.text.toLowerCase(),
                      );
                    });
                  },
                  onSelected: (String selection) async {
                    webViewController?.loadUrl(
                      urlRequest: URLRequest(
                        url: WebUri(
                          "file:///android_asset/flutter_assets/assets/html/$selection",
                        ),
                      ),
                    );
                  },
                ),
              ),
              const SizedBox(width: 5),
              SizedBox(
                height: 30,
                width: 30,
                child: IconButton(
                  padding: EdgeInsets.zero,
                  onPressed: () async {
                    if (await webViewController!.canGoBack()) {
                      webViewController!.goBack();
                    }
                  },
                  icon: const Icon(Icons.arrow_back, size: 18),
                ),
              ),
              SizedBox(
                height: 30,
                width: 30,
                child: IconButton(
                  padding: EdgeInsets.zero,
                  onPressed: () async {
                    if (await webViewController!.canGoForward()) {
                      webViewController!.goForward();
                    }
                  },
                  icon: const Icon(Icons.arrow_forward, size: 18),
                ),
              ),
              SizedBox(
                height: 30,
                width: 40,
                child: PopupMenuButton(
                  padding: EdgeInsets.zero,
                  itemBuilder: (context) {
                    return [
                      PopupMenuItem(
                        child: const Row(
                          children: [
                            Icon(FluentIcons.home_24_regular),
                            SizedBox(width: 10),
                            Text('Set as home'),
                          ],
                        ),
                        onTap: () async {
                          final webUri = await webViewController?.getUrl();
                          String currentURL = webUri.toString();
                          final SharedPreferences prefs =
                              await SharedPreferences.getInstance();
                          await prefs.setString("home_page_doc", currentURL);
                          Fluttertoast.showToast(
                            msg: "Set this as your Home page done.",
                          );
                        },
                      ),
                      PopupMenuItem(
                        child: const Row(
                          children: [
                            Icon(Icons.restore),
                            SizedBox(width: 10),
                            Text('Reset home'),
                          ],
                        ),
                        onTap: () async {
                          webViewController?.loadUrl(
                            urlRequest: URLRequest(
                              url: WebUri(
                                "file:///android_asset/flutter_assets/assets/html/index.html",
                              ),
                            ),
                          );

                          final SharedPreferences prefs =
                              await SharedPreferences.getInstance();
                          await prefs.setString(
                            "home_page_doc",
                            "file:///android_asset/flutter_assets/assets/html/index.html",
                          );
                          Fluttertoast.showToast(msg: "Home page reset done.");
                        },
                      ),
                    ];
                  },
                ),
              ),
            ],
          ),
        ),

        body: SafeArea(
          child: Column(
            children: <Widget>[
              Expanded(
                child: Stack(
                  children: [
                    initWiget,
                    progress < 1.0
                        ? LinearProgressIndicator(value: progress)
                        : Container(),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
