
import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

class FolderTreeView extends StatelessWidget {
  final Map<String, dynamic> folderData;
  final InAppWebViewController? webViewController;
  final double indentation;

  const FolderTreeView({
    super.key,
    required this.folderData,
    this.webViewController,
    this.indentation = 0.0,
  });

  @override
  Widget build(BuildContext context) {
    return _buildTreeView(folderData, indentation);
  }

  Widget _buildTreeView(Map<String, dynamic> data, double currentIndentation) {
    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: data.length,
      itemBuilder: (context, index) {
        String key = data.keys.elementAt(index);
        return _buildTreeItem(key, data[key], currentIndentation);
      },
    );
  }

  Widget _buildTreeItem(
      String name, Map<String, dynamic> data, double currentIndentation) {
    bool hasChildren = data['children'] != null && data['children'].isNotEmpty;

    if (!hasChildren) {
      return Padding(
        padding: EdgeInsets.only(left: currentIndentation),
        child: ListTile(
          leading: const Icon(Icons.folder_open_outlined),
          title: Text(name),
          onTap: () {
            if (data['index_path'] != null) {
              webViewController?.loadUrl(
                urlRequest: URLRequest(
                  url: WebUri(
                    "http://localhost:9387/assets${data['index_path']}",
                  ),
                ),
              );
            }
          },
        ),
      );
    }

    return Padding(
      padding: EdgeInsets.only(left: currentIndentation),
      child: ExpansionTile(
        leading: const Icon(Icons.folder_zip_outlined),
        title: Text(name),
        children: [
          FolderTreeView(
            folderData: data['children'],
            webViewController: webViewController,
            indentation: 10.0,
          ),
        ],
        onExpansionChanged: (isExpanded) {
          if (isExpanded && data['index_path'] != null) {
            webViewController?.loadUrl(
              urlRequest: URLRequest(
                url: WebUri(
                  "http://localhost:9387/assets${data['index_path']}",
                ),
              ),
            );
          }
        },
      ),
    );
  }
}
