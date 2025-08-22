import 'dart:convert';
import 'dart:io';

import 'package:path/path.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

Future<void> main() async {
  sqfliteFfiInit();

  final dbFactory = databaseFactoryFfi;
  final jsonFile = File('assets/html_files.json');
  // Use absolute path for the database file
  final dbFile = File(join(Directory.current.path, 'assets', 'html_files.db'));

  if (await dbFile.exists()) {
    await dbFile.delete();
    print('Deleted existing database.');
  }

  final List<dynamic> filePaths = jsonDecode(await jsonFile.readAsString());

  final db = await dbFactory.openDatabase(dbFile.path);
  print('Database opened at: ${dbFile.path}');

  await db.execute('''
    CREATE TABLE files (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      path TEXT NOT NULL
    )
  ''');
  print('Table "files" created.');

  final batch = db.batch();
  for (final path in filePaths) {
    batch.insert('files', {'path': path});
  }
  await batch.commit(noResult: true);

  print('Inserted \${filePaths.length} file paths into the database.');

  await db.close();
  print('Database closed.');
}