db = db.getSiblingDB("sante_db");

db.createUser({
    user: "admin_user",
    pwd: "admin123",
    roles: [{ role: "dbAdmin", db: "sante_db" }]
});

db.createUser({
    user: "medecin",
    pwd: "medecin123",
    roles: [{ role: "readWrite", db: "sante_db" }]
});

db.createUser({
    user: "infirmiere",
    pwd: "infirmiere123",
    roles: [{ role: "read", db: "sante_db" }]
});

db.createUser({
    user: "migration",
    pwd: "migration123",
    roles: [{ role: "readWrite", db: "sante_db" }]
});