class Gift {
  int? id;
  String name;
  String description;
  double price;
  String link;
  int priority;
  bool purchased;

  Gift({
    this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.link,
    required this.priority,
    this.purchased = false,
  });

  Map<String, dynamic> toMap() => {
        'id': id,
        'name': name,
        'description': description,
        'price': price,
        'link': link,
        'priority': priority,
        'purchased': purchased ? 1 : 0,
      };

  factory Gift.fromMap(Map<String, dynamic> map) => Gift(
        id: map['id'],
        name: map['name'],
        description: map['description'],
        price: map['price'],
        link: map['link'],
        priority: map['priority'],
        purchased: map['purchased'] == 1,
      );
}
