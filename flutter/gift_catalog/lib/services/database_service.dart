import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import '../models/gift.dart';

class DatabaseService {
  static final DatabaseService _instance = DatabaseService._internal();
  factory DatabaseService() => _instance;
  DatabaseService._internal();

  Database? _db;

  Future<Database> get database async {
    if (_db != null) return _db!;
    _db = await _initDB();
    return _db!;
  }

  Future<Database> _initDB() async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, 'gift_catalog.db');

    return await openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE gifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            link TEXT,
            priority INTEGER,
            purchased INTEGER
          )
        ''');
      },
    );
  }

  Future<List<Gift>> getGifts() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'gifts',
      orderBy: 'priority ASC',
    );
    return maps.map((e) => Gift.fromMap(e)).toList();
  }

  Future<void> insertGift(Gift gift) async {
    final db = await database;
    await db.insert('gifts', gift.toMap());
  }

  Future<void> updateGift(Gift gift) async {
    final db = await database;
    await db.update('gifts', gift.toMap(), where: 'id = ?', whereArgs: [gift.id]);
  }

  Future<void> deleteGift(int id) async {
    final db = await database;
    await db.delete('gifts', where: 'id = ?', whereArgs: [id]);
  }
}
